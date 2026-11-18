#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import generate_registry
import install
import validate_pig_stack


class PigStackVerificationTests(unittest.TestCase):
    def test_validate_repo_passes(self) -> None:
        errors = validate_pig_stack.validate(ROOT)
        self.assertEqual(errors, [])

    def test_registry_is_up_to_date(self) -> None:
        rendered = generate_registry.render_registry(ROOT)
        registry_path = ROOT / ".atl" / "skill-registry.md"
        self.assertTrue(registry_path.exists())
        self.assertEqual(registry_path.read_text(encoding="utf-8"), rendered)

    def test_validator_rejects_broken_link_and_comment(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp) / "pig-stack"
            install.install_target(ROOT, tmp_root, "copy", dry_run=False)
            broken_doc = tmp_root / "docs" / "broken.md"
            broken_doc.write_text("[missing](../nope.md)\n", encoding="utf-8")
            bad_script = tmp_root / "scripts" / "bad.py"
            bad_script.write_text("# banned comment\nprint('ok')\n", encoding="utf-8")

            errors = validate_pig_stack.validate(tmp_root)
            self.assertTrue(any("broken link target" in e for e in errors))
            self.assertTrue(any("banned comment line" in e for e in errors))

    def test_validator_rejects_token_cap_collision_and_bad_routes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp) / "pig-stack"
            install.install_target(ROOT, tmp_root, "copy", dry_run=False)

            swarm_dir = tmp_root / "skills" / "swarm"
            swarm_dir.mkdir(parents=True)
            oversized_body = " ".join(["x" * 20] * 220)
            (swarm_dir / "SKILL.md").write_text(
                "---\n"
                "name: swarm\n"
                'description: "Trigger: swarm. Colliding oversized skill."\n'
                "license: MIT\n"
                "metadata:\n"
                "  author: pig-stack\n"
                "---\n\n"
                "## Activation Contract\n\nLoad.\n\n"
                "## Hard Rules\n\n"
                f"{oversized_body}\n\n"
                "## Decision Gates\n\n| A | B |\n|---|---|\n| 1 | 2 |\n\n"
                "## Execution Steps\n\n1. Run `/missing-skill`.\n\n"
                "## Output Contract\n\nReturn ok.\n",
                encoding="utf-8",
            )

            pig_mode_md = tmp_root / "skills" / "pig-mode" / "SKILL.md"
            pig_mode_md.write_text(
                pig_mode_md.read_text(encoding="utf-8") + "\nRun `arena` immediately.\n",
                encoding="utf-8",
            )

            errors = validate_pig_stack.validate(tmp_root)
            self.assertTrue(any("collides with a built-in runtime skill" in e for e in errors))
            self.assertTrue(any("1000-token cap" in e for e in errors))
            self.assertTrue(any("unknown skill reference '/missing-skill'" in e for e in errors))
            self.assertTrue(any("auto-route to model-disabled skill 'arena'" in e for e in errors))

    def test_validator_comment_tokenizer_registry_and_dashes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp) / "pig-stack"
            install.install_target(ROOT, tmp_root, "copy", dry_run=False)

            inline_py = tmp_root / "scripts" / "inline_bad.py"
            inline_py.write_text("value = 1  # inline comment\n", encoding="utf-8")
            str_py = tmp_root / "scripts" / "string_ok.py"
            str_py.write_text('TEXT = """\n# markdown heading inside string\n"""\n', encoding="utf-8")

            reg_path = tmp_root / ".atl" / "skill-registry.md"
            reg_path.write_text("# stale registry\n", encoding="utf-8")

            ref_path = tmp_root / "skills" / "pig-mode" / "references" / "principles.md"
            ref_path.write_text(
                ref_path.read_text(encoding="utf-8") + "\nUse `pig-swarm` immediately — now.\n",
                encoding="utf-8",
            )

            errors = validate_pig_stack.validate(tmp_root)
            self.assertTrue(any("inline_bad.py:1: banned comment line" in e for e in errors))
            self.assertFalse(any("string_ok.py" in e for e in errors))
            self.assertTrue(any(".atl/skill-registry.md is out of date" in e for e in errors))
            self.assertTrue(any("auto-route to model-disabled skill 'pig-swarm'" in e for e in errors))
            self.assertTrue(any("banned em/en dash violates unslop" in e for e in errors))

    def test_installer_supports_symlink_and_copy_modes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fake_home = Path(tmp) / "home"
            fake_home.mkdir()

            rc_link = install.main(
                ["--target", "cursor", "--mode", "symlink", "--home", str(fake_home), "--source", str(ROOT)]
            )
            self.assertEqual(rc_link, 0)
            cursor_dest = fake_home / ".cursor" / "plugins" / "pig-stack"
            self.assertTrue(cursor_dest.is_symlink())
            self.assertEqual(cursor_dest.resolve(), ROOT)

            rc_copy = install.main(
                ["--target", "claude", "--mode", "copy", "--home", str(fake_home), "--source", str(ROOT)]
            )
            self.assertEqual(rc_copy, 0)
            claude_dest = fake_home / ".claude" / "plugins" / "pig-stack"
            self.assertTrue((claude_dest / ".claude-plugin" / "plugin.json").exists())
            self.assertTrue((claude_dest / "skills" / "pig-mode" / "SKILL.md").exists())

    def test_decision_log_helper_sanitizes_formula_and_tabs(self) -> None:
        log_sh = ROOT / "skills" / "show-me-your-work" / "scripts" / "log.sh"
        with tempfile.TemporaryDirectory() as tmp:
            tsv_path = Path(tmp) / "decisions.tsv"
            subprocess.run(
                [
                    "bash",
                    str(log_sh),
                    str(tsv_path),
                    "frame",
                    "=SUM(1,2)\ttabbed",
                    "+formula",
                    "commit\nabc",
                    "tests green",
                ],
                check=True,
            )
            lines = tsv_path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 2)
            fields = lines[1].split("\t")
            self.assertEqual(len(fields), 6)
            self.assertEqual(fields[2], "'=SUM(1,2) tabbed")
            self.assertEqual(fields[3], "'+formula")
            self.assertEqual(fields[4], "commit abc")


if __name__ == "__main__":
    unittest.main()
