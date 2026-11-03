# Setup banner redesign

Status: DONE
Plan Depth: STANDARD
Current Phase: Complete
Last Updated: 2026-11-03
Active Agent: Claude Code (context only)

## Executive Snapshot
Replace the 5x5 full-block "ANDINO AI RULES" wordmark with a small half-block
Andes-peak "A" icon on the left and a four-line info panel on the right, like the
Antigravity/Claude Code headers. Design accepted by the user after a 5-lens council
(peer review/synthesis done by the parent, not independent). Implemented and verified:
10 new banner tests + 17 UX tests pass; full suite has only the 12 pre-existing HEAD failures.

## Objective
`ai-rules setup` (interactive, TTY) opens with a polished, truthful header: icon,
product name + version, the command, AI tools found on PATH, and the working dir.

## Acceptance Criteria
- [ ] R1: Width >= 40 renders a 4-row icon (half blocks `▀▄█`) plus 4 info lines:
      `Andino AI Rules v<__version__>`, `ai-rules <command>`,
      `AI tools: <found joined by " · ">[ · N not on PATH]`, `<cwd with ~>`.
- [ ] R2: No rendered line exceeds the terminal width; overflow ends with `…`
      (`...` in ASCII mode); width < 40 gives one compact line.
- [ ] R3: Colors: icon only (snow cap + orange→red rows), title bold, other info dim;
      truecolor ANSI emitted, downsampling left to prompt_toolkit; color=False emits
      no escape sequences. NO_COLOR keeps disabling color.
- [ ] R4: ASCII mode (stdout cannot encode `▀▄█·…`) prints a pure-ASCII icon and text.
- [ ] R5: Host detection reuses `StaticHostAdapter.detect()` (`agy` for Antigravity);
      wording says "on PATH", never "installed"; detection errors never break setup
      (line becomes `AI tools: not checked`).
- [ ] R6: Unchanged gating: only `cmd_setup` when not `--non-interactive`, stdout is a
      TTY and TERM != dumb. Existing terminal UX tests keep passing.
- [ ] R7: Visual check of real collected info at 60/80/120 columns, dark and light
      terminal themes (rendered via Rich SVG export) before DONE.

## Scope
In: `src/ai_rules/banner.py`, new `tests/installer/test_banner.py`.
Out: other commands, `cli.py` call site (default `command="setup"` keeps it unchanged),
`platform/detect.py` (its `antigravity` probe is a separate concern), README,
release manifests, global installation, commits/pushes.

## User Decisions / Clarifications
- Style: small pixel icon left + info panel right. Info: version, active command,
  detected hosts, working dir. Scope: `ai-rules setup` only. Palette delegated to
  council → keep red/orange identity on the icon only; neutral text.
- Wording: "AI tools" instead of jargon "hosts" (Outsider lens).

## Baseline / Starting Evidence
- `banner.py::render_banner(width, *, color, block)` + `print_setup_banner()`; only
  caller `cli.py::cmd_setup` (`if not args.non_interactive: print_setup_banner()`).
- No banner tests exist (`grep banner tests/` empty).
- `hosts/adapters.py::StaticHostAdapter.detect()` → `HostDetection(status=PRESENT|UNKNOWN)`
  via `shutil.which` on `codex`/`claude`/`opencode`/`agy`;
  `build_host_adapters(load_catalog().hosts)`; catalog order codex, claude-code,
  opencode, antigravity-cli; display names Codex, Claude Code, OpenCode, Antigravity CLI.
- prompt_toolkit 3.0.53 `formatted_text/ansi.py` parses SGR 1, 2, `38;2`, `48;2` and
  its output re-encodes at the detected color depth (local source inspection).
- On this machine all of `agy codex claude opencode` resolve on PATH.

## Constraints & Invariants
No new dependency. Pure renderer has no I/O. Banner failure must not abort setup.

## Execution Board
| Phase | Status | Goal | Scope | Evidence / Result |
| --- | --- | --- | --- | --- |
| Phase 1 — Pure renderer (T1) | DONE | R1–R4 | banner.py, test_banner.py | 6 tests PASS |
| Phase 2 — Info collection + printing (T2) | DONE | R5, R6 | banner.py, adapters.py (ruling), test_banner.py | 10 banner + 17 UX tests PASS |
| Phase 3 — Visual verification (T3) | DONE | R7 | scratch renders only | SVG 60/80/120 dark/light + ASCII; real PowerShell run |

## Coverage
| Requirement / failure case | Task | Check |
| --- | --- | --- |
| R1 wide layout | T1 | `test_wide_layout_has_icon_and_info` |
| R2 width fit + compact | T1 | `test_lines_fit_width`, `test_narrow_is_one_line` |
| R3 color on/off | T1 | `test_color_and_plain_modes` |
| R4 ASCII | T1 | `test_ascii_mode_is_pure_ascii` |
| R1 tools wording variants | T1 | `test_tools_line_variants` |
| R5 adapter detection | T2 | `test_collect_uses_host_adapters` |
| R5 detection error | T2 | `test_print_survives_collection_error` |
| R6 non-TTY silent | T2 | `test_print_skips_non_tty` + test_terminal_ux suite |
| R7 visual | T3 | SVG screenshots inspected |

## Detailed Execution

### T1 — Pure icon + info renderer
Status: DONE
Readiness: READY
Requirements: R1–R4
Depends on: none
Owns: Replace `src/ai_rules/banner.py` (`_GLYPHS`, `render_banner`); Create `tests/installer/test_banner.py`
Interfaces: produces (proposed)
`BannerInfo(version: str, command: str, tools_found: tuple[str, ...], tools_missing: tuple[str, ...], cwd: str)` and
`render_banner(info: BannerInfo, width: int, *, color: bool = True, unicode: bool = True) -> str`
(returns `"\n" + rows + "\n"`). Old `render_banner(width, ...)` signature is removed (only caller is `print_setup_banner`).

Change Specification:
- Remove `_GLYPHS` and the old letter renderer.
- Icon: 10x8 pixel grid, two pixel rows per text row (4 text rows), `S` snow, `#` rock:

```python
_ICON = (
    "....SS....",
    "...SSSS...",
    "...####...",
    "..######..",
    "..##..##..",
    ".########.",
    ".##....##.",
    "##......##",
)
_SNOW = (215, 222, 232)
_TOP, _BOTTOM = (255, 130, 40), (174, 20, 38)   # rock rows 2..7, orange -> red
_ASCII_ICON = ("   /\\     ", "  /  \\    ", " / /\\ \\   ", "/_/  \\_\\  ")
```

  Plain glyph result (must match exactly, used in tests):
  `"   ▄██▄   "`, `"  ▄████▄  "`, `" ▄██▄▄██▄ "`, `"▄██    ██▄"`.
- Cell rule for (top, bottom) pixels: both off → space; both on, same color → `█`
  fg; both on, different colors → `▀` fg=top bg=bottom; top only → `▀` fg top;
  bottom only → `▄` fg bottom. With color, each non-space cell is
  `\x1b[38;2;r;g;bm` (+ `\x1b[48;2;r;g;bm` when bg) + glyph + `\x1b[0m`.
- Info segments (text, sgr); `BOLD="\x1b[1m"`, `DIM="\x1b[2m"`; sgr dropped when color=False:

```python
sep = " · " if unicode else ", "
tools = f"AI tools: {sep.join(info.tools_found)}" if info.tools_found else "AI tools: none on PATH"
if not info.tools_found and not info.tools_missing:
    tools = "AI tools: not checked"
elif info.tools_found and info.tools_missing:
    tools += f"{sep}{len(info.tools_missing)} not on PATH"
lines = [
    [("Andino AI Rules", BOLD), (f" v{info.version}", DIM)],
    [(f"ai-rules {info.command}", DIM)],
    [(tools, "")],
    [(info.cwd, DIM)],   # cwd shortened from the LEFT: "…" + tail
]
```

- Layout: row = `"  " + icon_cell_row + "   " + info_line`; text limit = `width - 15`.
  Truncate by visible length, ellipsis `"…"` (unicode) / `"..."` (ASCII).
  `width < 40` → single row `"  " + fit(f"Andino AI Rules v{v}{sep}{command}", width - 2)`
  (bold title when color). Strip trailing spaces of each row before reset codes.

Tests (`tests/installer/test_banner.py`, unittest, decisive assertions):

```python
import re, unittest
from ai_rules.banner import BannerInfo, render_banner
ANSI = re.compile(r"\x1b\[[0-9;]*m")
INFO = BannerInfo("0.1.0", "setup", ("Codex", "Claude Code", "OpenCode", "Antigravity CLI"), (), "~\\Projects\\demo")
def plain(s): return ANSI.sub("", s)
def rows(s): return [r for r in plain(s).split("\n") if r]

class BannerRenderTests(unittest.TestCase):
    def test_wide_layout_has_icon_and_info(self):
        r = rows(render_banner(INFO, 120, color=False))
        self.assertEqual(4, len(r))
        self.assertEqual("  " + "   ▄██▄   " + "   Andino AI Rules v0.1.0", r[0])
        self.assertTrue(r[1].endswith("ai-rules setup"))
        self.assertTrue(r[2].endswith("AI tools: Codex · Claude Code · OpenCode · Antigravity CLI"))
        self.assertTrue(r[3].startswith("  ▄██    ██▄") and r[3].endswith("~\\Projects\\demo"))
    def test_lines_fit_width(self):
        for w in (40, 60, 80):
            for line in rows(render_banner(INFO, w)):
                self.assertLessEqual(len(line), w)
        self.assertIn("…", plain(render_banner(INFO, 60)))
    def test_narrow_is_one_line(self):
        self.assertEqual(["  Andino AI Rules v0.1.0 · setup"], rows(render_banner(INFO, 39, color=False)))
    def test_color_and_plain_modes(self):
        colored = render_banner(INFO, 100)
        self.assertIn("\x1b[38;2;215;222;232m", colored)       # snow cap
        self.assertIn("\x1b[1mAndino AI Rules", colored)
        self.assertNotIn("\x1b", render_banner(INFO, 100, color=False))
    def test_ascii_mode_is_pure_ascii(self):
        out = render_banner(INFO, 60, color=False, unicode=False)
        self.assertTrue(out.isascii()); self.assertIn("/\\", out); self.assertIn("...", out)
    def test_tools_line_variants(self):
        some = BannerInfo("0.1.0", "setup", ("Codex",), ("Claude Code", "OpenCode"), "~")
        none = BannerInfo("0.1.0", "setup", (), ("Codex",), "~")
        unknown = BannerInfo("0.1.0", "setup", (), (), "~")
        self.assertIn("AI tools: Codex · 2 not on PATH", plain(render_banner(some, 120)))
        self.assertIn("AI tools: none on PATH", plain(render_banner(none, 120)))
        self.assertIn("AI tools: not checked", plain(render_banner(unknown, 120)))
```

Actions:
- [ ] Create test file above; run `python -m unittest tests.installer.test_banner -v` from
      repo root; expect ImportError on `BannerInfo` → that is setup-level RED, so first add
      a stub `BannerInfo` dataclass + old renderer untouched, rerun, expect assertion failures.
- [ ] Implement the renderer per the Change Specification.
- [x] Rerun focused tests; expect 6 PASS.
Ruling: plain mode draws `█` (not `▀`) for two-color cells — one color only without ANSI — local fix, no consumer impact.
Ruling: last icon pixel row `##......##` → `###....###` — the planned literal `▄██    ██▄` was mis-derived (old grid gives `▄█▀    ▀█▄`); a solid base keeps the agreed shape — cosmetic only.
Result / Evidence: RED = 6 errors on the old signature (after stub `BannerInfo`); after fixes
`python -m unittest tests.installer.test_banner` → Ran 6, OK (2026-11-03, Python 3.12, repo root).

### T2 — Collect real info and print safely
Status: DONE
Readiness: READY after T1 acceptance
Requirements: R5, R6
Depends on: T1
Owns: `src/ai_rules/banner.py` (`print_setup_banner`, new `collect_banner_info`, `_display_path`); `tests/installer/test_banner.py`
Interfaces: consumes `build_host_adapters`, `load_catalog`, `DetectionStatus`, `ai_rules.__version__`;
`print_setup_banner(command: str = "setup") -> None` keeps the cli call site unchanged.

Change Specification:

```python
def collect_banner_info(command: str = "setup") -> BannerInfo:
    from ai_rules import __version__
    from ai_rules.catalog import load_catalog
    from ai_rules.domain.statuses import DetectionStatus
    from ai_rules.hosts.adapters import build_host_adapters
    found, missing = [], []
    for adapter in build_host_adapters(load_catalog().hosts).values():
        target = found if adapter.detect().status == DetectionStatus.PRESENT else missing
        target.append(adapter.host.display_name)
    return BannerInfo(__version__, command, tuple(found), tuple(missing), _display_path(Path.cwd()))

def _display_path(path: Path) -> str:
    try:
        rel = path.relative_to(Path.home())
    except ValueError:
        return str(path)
    return "~" if rel == Path(".") else f"~{os.sep}{rel}"
```

`print_setup_banner(command="setup")`: keep the TTY / `TERM=dumb` early return;
`unicode` = whether `"▀▄█·…"` encodes with `sys.stdout.encoding or "utf-8"`;
`try: info = collect_banner_info(command) except Exception: info = BannerInfo(__version__, command, (), (), _display_path(Path.cwd()))`;
print `render_banner(info, shutil.get_terminal_size().columns, color="NO_COLOR" not in os.environ, unicode=unicode)`
via `prompt_toolkit.print_formatted_text(ANSI(...))` as today.

Tests to add:

```python
from unittest.mock import patch
import io
from ai_rules import banner, __version__

class BannerIOTests(unittest.TestCase):
    def test_collect_uses_host_adapters(self):
        with patch("ai_rules.hosts.adapters.shutil.which", side_effect=lambda c: f"/bin/{c}" if c in ("codex", "agy") else None):
            info = banner.collect_banner_info()
        self.assertEqual(("Codex", "Antigravity CLI"), info.tools_found)
        self.assertEqual(("Claude Code", "OpenCode"), info.tools_missing)
        self.assertEqual(__version__, info.version)
    def test_print_skips_non_tty(self):
        out = io.StringIO()
        with patch("sys.stdout", out):
            banner.print_setup_banner()
        self.assertEqual("", out.getvalue())
    def test_print_survives_collection_error(self):
        tty = io.StringIO(); tty.isatty = lambda: True
        with patch("sys.stdout", tty), patch.object(banner, "collect_banner_info", side_effect=RuntimeError), \
             patch("prompt_toolkit.print_formatted_text") as shown:
            banner.print_setup_banner()
        self.assertIn("AI tools: not checked", str(shown.call_args.args[0].value))
```

Actions:
- [ ] Add tests; run focused module; expect RED on missing `collect_banner_info`/new wording.
- [x] Implement; rerun focused module and
      `python -m unittest tests.installer.test_terminal_ux` (17 OK).
Ruling: catalog has a 5th host `antigravity-ide` with no PATH probe; counting it as "not on PATH" would be untrue.
Lifted the adapter's command map to `hosts/adapters.py::HOST_COMMANDS` (behavior unchanged) and the banner skips hosts
absent from it — scope grew by one file, pure refactor.
Added `test_display_path_uses_home_tilde` (10 banner tests total).
Integration gate: `python -m unittest discover -s tests -p "test_*.py"` from repo root —
no new failures versus the pre-change run (record both counts).
Result / Evidence: RED = 3 errors (`collect_banner_info`/`_display_path` missing), then 1 failure exposing the IDE host;
after the ruling `python -m unittest tests.installer.test_banner tests.installer.test_terminal_ux` → Ran 27, OK.
Full suite `python -m unittest discover -s tests -p "test_*.py"`: Ran 377, failures=11, errors=1, skipped=5 —
all in search_first / andino_reliability / thin_coordinator / first_party_bundles. Baseline at clean HEAD 5871af9
(detached worktree): Ran 367, the identical 12 failures/errors (sorted diff empty) — pre-existing, not caused by this change.

### T3 — Visual verification
Status: DONE
Readiness: READY after T2
Requirements: R7
Depends on: T2
Owns: scratchpad files only.
Actions:
- [ ] Script (scratchpad): `info = collect_banner_info()`; for w in 60, 80, 120:
      `Text.from_ansi(render_banner(info, w))` → `Console(record=True, width=w).print(...)` →
      `export_svg(theme=MONOKAI)` and a light theme (`DEFAULT_TERMINAL_THEME`); open the SVGs
      in the browser pane and screenshot.
- [ ] Inspect: icon reads as a peaked "A", rows aligned, no wrap, snow cap visible on dark,
      text readable on light. Fix in T1 scope if not; rerun T1/T2 tests.
- [x] Optional real-terminal evidence: run `ai-rules setup` in a terminal tab, read the
      header, cancel the prompt (no changes are made on cancel).
Result / Evidence: Rich SVG renders of real collected info at 60/80/120 cols, MONOKAI and default light theme,
plus 80-col ASCII/no-color, screenshotted in the browser pane: peaked "A" with snow cap, 4 rows aligned with 4 info
lines, no wrap, 60 cols truncates the tools line with `…`, snow cap visible on dark and faint-but-present on light.
`python -m ai_rules setup` in a PowerShell terminal tab printed the header then the host prompt; tab closed (no install).
Limit: legacy conhost and real light-theme terminals not observed directly.

## Review (self-review, no independent reviewer)
Spec: R1–R7 each map to an executed test or observation above. Standards: pure renderer has no I/O; banner errors
are contained; the adapters change is a no-behavior refactor. Not committed (no authorization).
Open, out of scope: `platform/detect.py` still probes `antigravity` instead of `agy`; 12 pre-existing suite failures.

## NEXT ACTION
None — task complete. Commit awaits user authorization.
