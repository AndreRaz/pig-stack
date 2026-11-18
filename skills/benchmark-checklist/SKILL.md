---
name: benchmark-checklist
description: "Trigger: benchmark-checklist, /benchmark-checklist, vet benchmark, verify speedup. Audits performance numbers for limiters, tuning, errors, and repeatability."
license: MIT
metadata:
  author: pig-stack
  version: "1.0"
  layer: "2"
---

## Activation Contract

Load before trusting, reporting, or acting on any measured latency, throughput, memory, or speedup number.

## Hard Rules

- **Seven-gate audit:** Check (1) dominant limiter (via profiler outside timed run), (2) production-equivalent tuning on both sides, (3) physical/arithmetic ceiling sanity, (4) error/incorrect-output counts, (5) >= 5 alternating A/B runs (`A, B, A, B...`) reporting median + range, (6) end-to-end user impact share, and (7) proof work actually ran (no dead-code/lazy-eval/cache skip).
- **Fail closed to inconclusive:** If limiter, tuning, error count, or execution is unverified, report `inconclusive` with the missing check.
- **Ballpark exception:** Only if the user explicitly asked for a quick 1-run ballpark may steps 1-3 and 5-6 be skipped, still checking errors (4) and real execution (7) and labeling it "1-run ballpark".

## Decision Gates

| Observation | Verdict |
|---|---|
| Median gap exceeds run-to-run range AND all 7 checks pass | `faster` / `slower` (cite median, range, N, limiter) |
| Median gap <= run-to-run variation | `no measurable difference` |
| Side untuned, error count missing, or work skipped | `inconclusive` (name gap) |

## Execution Steps

1. State the exact claim being tested and inspect the benchmark script + system load (`uptime`, `nproc`).
2. Profile outside timed runs to identify the real bottleneck/limiter.
3. Run >= 5 alternating A/B iterations checking correctness/errors and end-to-end relevance.
4. Summarize with `Explain the Number` (`median`, `range`, `N`, `limiter`).

## Output Contract

Return: verdict (`faster | slower | no measurable difference | inconclusive`), metric before vs after (median, range, N), identified limiter, error count, and end-to-end share.
