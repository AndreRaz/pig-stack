#!/usr/bin/env python3
from __future__ import annotations

import argparse
import io
import json
import re
import sys
import tokenize
from pathlib import Path

SCRIPT_DIR = str(Path(__file__).resolve().parent)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import generate_registry


FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.DOTALL)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SLASH_SKILL_RE = re.compile(r"`/([a-z][a-z0-9-]+)`")
PROMPT_SLASH_SKILL_RE = re.compile(r"(?:^|\s)/([a-z][a-z0-9-]+)\b")
MAX_SKILL_WORDS = 750
MAX_SKILL_EST_TOKENS = 1000
REQUIRED_SKILL_SECTIONS = (
    "## Activation Contract",
    "## Hard Rules",
    "## Decision Gates",
    "## Execution Steps",
    "## Output Contract",
)
FORBIDDEN_STRINGS = (
    "cursor-team-kit",
    "poteto-mode",
    "poteto-agent",
    "claude-opus-5-5",
    "claude-fable-5-2",
    "gemini-4-carbon",
)
RESERVED_SKILL_NAMES = frozenset(
    {
        "swarm",
        "plugin",
        "automation",
        "agy-customizations",
        "antigravity-guide",
        "generative_ui",
        "run-workflow",
        "swarm_monitor",
    }
)
NON_SKILL_SLASH_PATHS = frozenset({"tmp", "dev", "etc", "var", "usr", "home", "opt"})
OPT_IN_MARKERS = ("opt-in", "user asks", "user invokes", "suggest", "backlog", "explicitly")


def parse_doc(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("missing or malformed YAML frontmatter")
    meta: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.startswith(" "):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            meta[key.strip()] = val.strip()
    return meta, match.group(2)


def strip_quotes(val: str) -> str:
    if len(val) >= 2 and val[0] == val[-1] and val[0] in ('"', "'"):
        return val[1:-1]
    return val


def check_manifests(root: Path, errors: list[str], skill_names: set[str]) -> None:
    manifest_paths = (
        root / "plugin.json",
        root / ".cursor-plugin" / "plugin.json",
        root / ".claude-plugin" / "plugin.json",
    )
    versions: set[str] = set()
    names: set[str] = set()
    for path in manifest_paths:
        if not path.exists():
            errors.append(f"missing manifest: {path.relative_to(root)}")
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        names.add(str(data.get("name", "")))
        versions.add(str(data.get("version", "")))
        logo = data.get("logo")
        if logo and not (root / logo).exists():
            errors.append(f"{path.relative_to(root)}: missing logo target {logo}")
        for prompt in data.get("suggestedPrompts", []):
            if not isinstance(prompt, str):
                continue
            for ref in PROMPT_SLASH_SKILL_RE.findall(prompt):
                if ref not in NON_SKILL_SLASH_PATHS and ref not in skill_names:
                    errors.append(f"{path.relative_to(root)}: unknown skill reference '/{ref}' in suggestedPrompts")
    if names != {"pig-stack"}:
        errors.append(f"manifest names mismatch: {sorted(names)}")
    if len(versions) != 1 or "" in versions:
        errors.append(f"manifest versions mismatch: {sorted(versions)}")


def check_skills(root: Path, errors: list[str]) -> tuple[set[str], set[str]]:
    skill_files = sorted((root / "skills").glob("*/SKILL.md"))
    skill_names: set[str] = set()
    disabled_skills: set[str] = set()
    if not skill_files:
        errors.append("no skills found under skills/*/SKILL.md")
        return skill_names, disabled_skills

    for skill_md in skill_files:
        rel = skill_md.relative_to(root).as_posix()
        text = skill_md.read_text(encoding="utf-8")
        try:
            meta, body = parse_doc(text)
        except ValueError as exc:
            errors.append(f"{rel}: {exc}")
            continue

        expected_name = skill_md.parent.name
        name = strip_quotes(meta.get("name", ""))
        if name != expected_name:
            errors.append(f"{rel}: frontmatter name {name!r} != directory {expected_name!r}")
        if name:
            skill_names.add(name)
        if name in RESERVED_SKILL_NAMES:
            errors.append(f"{rel}: skill name {name!r} collides with a built-in runtime skill")
        if strip_quotes(meta.get("disable-model-invocation", "")).lower() == "true":
            disabled_skills.add(name)

        raw_desc = meta.get("description", "")
        if not (raw_desc.startswith('"') and raw_desc.endswith('"')):
            errors.append(f"{rel}: description must be single-line double-quoted")
        desc = strip_quotes(raw_desc)
        if not desc.startswith("Trigger:"):
            errors.append(f"{rel}: description must start with 'Trigger:'")
        if len(desc) > 250:
            errors.append(f"{rel}: description exceeds 250 chars ({len(desc)})")

        for field in ("license", "metadata"):
            if field not in meta:
                errors.append(f"{rel}: missing frontmatter field {field}")

        positions: list[int] = []
        for section in REQUIRED_SKILL_SECTIONS:
            idx = body.find(section)
            if idx == -1:
                errors.append(f"{rel}: missing section {section}")
            else:
                positions.append(idx)
        if len(positions) == len(REQUIRED_SKILL_SECTIONS) and positions != sorted(positions):
            errors.append(f"{rel}: required sections out of order")

        word_count = len(body.split())
        if word_count > MAX_SKILL_WORDS:
            errors.append(f"{rel}: body exceeds {MAX_SKILL_WORDS}-word budget ({word_count} words)")
        est_tokens = (len(body) + 3) // 4
        if est_tokens > MAX_SKILL_EST_TOKENS:
            errors.append(f"{rel}: body exceeds {MAX_SKILL_EST_TOKENS}-token cap (~{est_tokens} tokens)")

    return skill_names, disabled_skills


def check_agents(root: Path, errors: list[str]) -> int:
    agent_files = sorted((root / "agents").glob("*.md"))
    if not agent_files:
        errors.append("no agents found under agents/*.md")
        return 0
    for agent_md in agent_files:
        rel = agent_md.relative_to(root).as_posix()
        text = agent_md.read_text(encoding="utf-8")
        try:
            meta, body = parse_doc(text)
        except ValueError as exc:
            errors.append(f"{rel}: {exc}")
            continue
        if strip_quotes(meta.get("name", "")) != agent_md.stem:
            errors.append(f"{rel}: name does not match filename stem")
        if "## Output Contract" not in body:
            errors.append(f"{rel}: missing ## Output Contract")
    return len(agent_files)


def check_links_and_forbidden(root: Path, errors: list[str]) -> None:
    md_files = [
        p
        for p in root.rglob("*.md")
        if ".git" not in p.parts and ".atl" not in p.parts
    ]
    for md in sorted(md_files):
        rel = md.relative_to(root).as_posix()
        text = md.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_STRINGS:
            if forbidden in text:
                errors.append(f"{rel}: forbidden legacy reference {forbidden!r}")
        for raw_target in LINK_RE.findall(text):
            target = raw_target.split("#", 1)[0].strip()
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            if "<" in target or ">" in target:
                continue
            resolved = (md.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{rel}: broken link target {raw_target!r}")


def check_skill_references(
    root: Path,
    skill_names: set[str],
    disabled_skills: set[str],
    errors: list[str],
) -> None:
    md_files = [
        p
        for p in root.rglob("*.md")
        if ".git" not in p.parts and ".atl" not in p.parts
    ]
    for md in sorted(md_files):
        rel = md.relative_to(root).as_posix()
        text = md.read_text(encoding="utf-8")
        for ref in SLASH_SKILL_RE.findall(text):
            if ref in NON_SKILL_SLASH_PATHS:
                continue
            if ref not in skill_names:
                errors.append(f"{rel}: unknown skill reference '/{ref}'")

    route_targets: list[Path] = []
    for skill_md in sorted((root / "skills").glob("*/SKILL.md")):
        if skill_md.parent.name not in disabled_skills:
            route_targets.append(skill_md)
    route_targets.extend(sorted((root / "skills" / "pig-mode" / "playbooks").glob("*.md")))
    route_targets.extend(sorted((root / "skills" / "pig-mode" / "references").glob("*.md")))

    for path in route_targets:
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        try:
            _, body = parse_doc(text)
        except ValueError:
            body = text
        for line_no, line in enumerate(body.splitlines(), start=1):
            low = line.lower()
            for disabled in sorted(disabled_skills):
                if f"`{disabled}`" in line or f"`/{disabled}`" in line:
                    if not any(marker in low for marker in OPT_IN_MARKERS):
                        errors.append(
                            f"{rel}:{line_no}: auto-route to model-disabled skill {disabled!r} without opt-in qualifier"
                        )


def check_unslop_dashes(root: Path, errors: list[str]) -> None:
    for folder in ("skills", "agents", "rules"):
        base = root / folder
        if not base.exists():
            continue
        for md in sorted(base.rglob("*.md")):
            text = md.read_text(encoding="utf-8")
            if "—" in text or "–" in text:
                errors.append(f"{md.relative_to(root).as_posix()}: banned em/en dash violates unslop")


def check_registry(root: Path, errors: list[str]) -> None:
    registry_path = root / ".atl" / "skill-registry.md"
    if not registry_path.exists():
        errors.append("missing .atl/skill-registry.md; run python3 scripts/generate_registry.py")
        return
    expected = generate_registry.render_registry(root)
    if registry_path.read_text(encoding="utf-8") != expected:
        errors.append(".atl/skill-registry.md is out of date; run python3 scripts/generate_registry.py")


def check_python_comment_ban(root: Path, errors: list[str]) -> None:
    for folder in ("scripts", "tests"):
        base = root / folder
        if not base.exists():
            continue
        for py_file in sorted(base.glob("*.py")):
            text = py_file.read_text(encoding="utf-8")
            try:
                tokens = list(tokenize.generate_tokens(io.StringIO(text).readline))
            except tokenize.TokenError as exc:
                errors.append(f"{py_file.relative_to(root)}: tokenize error: {exc}")
                continue
            for token in tokens:
                if token.type != tokenize.COMMENT:
                    continue
                line_no = token.start[0]
                if line_no == 1 and token.string.startswith("#!"):
                    continue
                errors.append(f"{py_file.relative_to(root)}:{line_no}: banned comment line")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    skill_names, disabled_skills = check_skills(root, errors)
    check_manifests(root, errors, skill_names)
    check_agents(root, errors)
    check_links_and_forbidden(root, errors)
    check_skill_references(root, skill_names, disabled_skills, errors)
    check_unslop_dashes(root, errors)
    check_registry(root, errors)
    check_python_comment_ban(root, errors)
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate pig-stack plugin structure and links")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args(argv)

    root = args.root.resolve()
    errors = validate(root)
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    skill_count = len(list((root / "skills").glob("*/SKILL.md")))
    agent_count = len(list((root / "agents").glob("*.md")))
    print(f"PASS: 3 manifests, {skill_count} skills, {agent_count} agents, 0 errors")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
