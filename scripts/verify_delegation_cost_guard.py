#!/usr/bin/env python3
"""Deterministic offline verifier for the delegation cost guard.

Validates:
1. SKILL.md stays under the 150-line contract ceiling.
2. Portable delegation text names tiers, not vendor models; model names live only in
   the host calibration resource, which both SKILL.md and GUIDE.md link.
3. No delegation text recommends the `max` effort setting.
4. Work is delegated per lane, not as a fresh subagent per task.
5. Waves need a stated count/tier/effort and the user's go-ahead; no automatic relaunch.
6. Review is risk-scaled instead of a mandatory reviewer per task.
7. The workflow anti-loop guard carries the same wave approval rule.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "delegation"
CALIBRATION = SKILL_DIR / "resources" / "host-cost-calibration.md"
MODEL_NAMES = re.compile(r"(?i)\b(haiku|sonnet|opus|gpt-[\w.]+|gemini[\w.-]*|o\d-mini)\b")


def portable_files() -> list[Path]:
    files = [SKILL_DIR / "SKILL.md", SKILL_DIR / "GUIDE.md"]
    files += sorted(p for p in (SKILL_DIR / "resources").glob("*.md") if p != CALIBRATION)
    return files


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_skill_line_ceiling():
    total = len(read(SKILL_DIR / "SKILL.md").splitlines())
    assert total < 150, f"SKILL.md exceeds 150-line ceiling: {total}"
    print(f"PASS: SKILL.md line budget ({total} < 150)")


def test_tiers_not_model_names():
    hits = [(p.name, m.group(0)) for p in portable_files() for m in MODEL_NAMES.finditer(read(p))]
    assert not hits, f"Vendor model names in portable delegation text: {hits}"
    assert CALIBRATION.is_file(), f"Missing {CALIBRATION}"
    for name in ("SKILL.md", "GUIDE.md"):
        assert "resources/host-cost-calibration.md" in read(SKILL_DIR / name), f"{name} must link calibration"
    print("PASS: portable text uses tiers; host calibration resource linked")


def test_no_max_effort():
    hits = [p.name for p in portable_files() if re.search(r"\|\s*`max`\s*\|", read(p))]
    assert not hits, f"`max` effort recommended in: {hits}"
    print("PASS: no `max` effort recommendation")


def test_lane_not_fresh_agent_per_task():
    hits = [p.name for p in portable_files() if re.search(r"(?i)fresh subagent per task", read(p))]
    assert not hits, f"Per-task fresh subagent still prescribed in: {hits}"
    for name in ("SKILL.md", "GUIDE.md"):
        assert re.search(r"(?i)\blane\b", read(SKILL_DIR / name)), f"{name} must define lanes"
    print("PASS: delegation unit is a lane")


def test_wave_approval_and_no_relaunch():
    for name in ("SKILL.md", "GUIDE.md"):
        text = read(SKILL_DIR / name)
        assert re.search(r"(?i)go-ahead", text), f"{name} lacks wave go-ahead gate"
        assert re.search(r"(?i)no automatic relaunch", text), f"{name} lacks no-relaunch rule"
    print("PASS: wave approval gate and no automatic relaunch")


def test_risk_scaled_review():
    text = read(SKILL_DIR / "SKILL.md")
    assert "Every task requires independent spec + quality review" not in text, "per-task reviewer still mandatory"
    assert re.search(r"(?i)risk-scaled review", text), "SKILL.md lacks risk-scaled review invariant"
    print("PASS: review is risk-scaled")


def test_anti_loop_guard():
    text = read(ROOT / "references" / "anti-loop.md")
    row = next(line for line in text.splitlines() if "Agent explosion" in line)
    assert re.search(r"(?i)go-ahead", row) and re.search(r"(?i)no automatic relaunch", row), (
        "anti-loop guard 10 lacks wave approval / no-relaunch rule"
    )
    print("PASS: anti-loop guard carries wave approval")


def main() -> int:
    tests = [v for k, v in globals().items() if k.startswith("test_")]
    failed = 0
    for test in tests:
        try:
            test()
        except AssertionError as exc:
            failed += 1
            print(f"FAIL: {test.__name__}: {exc}")
    print(f"{len(tests) - failed}/{len(tests)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
