#!/usr/bin/env python3
"""Deck render check (owner 2026-10-21, "Build fixes, A and B", decision B): open a built Season Deck page in headless
Chromium and PASS only when the page draws itself. Reading the page's text cannot do this: the tab bar and every pane
are drawn by the page's script, so on 10/21 a page whose script threw in the Movers pane carried all six pane ids and
showed no tabs (after-report-2026-10-21-board-test.md §3).

PASS needs all of:
  - no uncaught script error, on load or on clicking any tab;
  - exactly the six tabs, in order: Today, Trade Analyzer, Free Agents, Board, Movers, Week;
  - every pane present with content, and each tab showing its own pane when clicked.
The page is opened offline (every http/https request is aborted), so a blocked web font is not an error; only the
page's own script is judged. If no browser can start, the result is UNAVAILABLE, which callers treat as a failure:
an unchecked page is never published.

    python3 scripts/deck_render_check.py report/season/deck_<date>.html
Prints 'DECK RENDER: PASS — ...' and exits 0, or 'DECK RENDER: FAIL — ...' / 'DECK RENDER: UNAVAILABLE — ...' and exits 1.
"""
import glob
import os
import re
import sys

TABS = ["Today", "Trade Analyzer", "Free Agents", "Board", "Movers", "Week", "League"]  # 2026-10-23: League (owner, Build 1)
PANES = ["today", "trade", "fa", "board", "movers", "week", "league"]


def _executables():
    """Browsers to try, in order: DECK_CHROMIUM, Playwright's own default (None), then the builds installed under
    PLAYWRIGHT_BROWSERS_PATH, newest first. The pip package can be newer than the installed browsers (2026-10-21:
    playwright 1.64 wants build 1248, /opt/pw-browsers holds 1194), so the installed builds are named explicitly."""
    out = [os.environ["DECK_CHROMIUM"]] if os.environ.get("DECK_CHROMIUM") else []
    out.append(None)
    root = os.environ.get("PLAYWRIGHT_BROWSERS_PATH") or "/opt/pw-browsers"
    found = (glob.glob(os.path.join(root, "chromium_headless_shell-*", "*", "headless_shell"))
             + glob.glob(os.path.join(root, "chromium_headless_shell-*", "*", "chrome-headless-shell"))
             + glob.glob(os.path.join(root, "chromium-*", "chrome-linux", "chrome")))
    def build(path):
        m = re.search(r"-(\d+)" + re.escape(os.sep), path)
        return int(m.group(1)) if m else 0
    return out + sorted((p for p in found if os.access(p, os.X_OK)), key=build, reverse=True)


def _launch(p):
    tried = []
    for exe in _executables():
        try:
            b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
            return b, exe or "playwright default", tried
        except Exception as e:  # noqa: BLE001 — every launch failure is recorded and the next browser tried
            tried.append(f"{exe or 'playwright default'}: {str(e).splitlines()[0][:160]}")
    return None, None, tried


_AVAILABLE = None


def available():
    """(True, browser) when a browser starts here, else (False, why); probed once per process."""
    global _AVAILABLE
    if _AVAILABLE is None:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as e:
            _AVAILABLE = (False, f"playwright not importable: {e}")
            return _AVAILABLE
        with sync_playwright() as p:
            b, exe, tried = _launch(p)
            if b is not None:
                b.close()
            _AVAILABLE = (True, exe) if b is not None else (False, "no browser started: " + "; ".join(tried))
    return _AVAILABLE


def render(html_path):
    """Open the page and report what it drew: tab labels, page errors, each pane's text and whether clicking its tab
    shows it. Returns dict(status='UNAVAILABLE', reasons=[...]) when no browser starts."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        return dict(status="UNAVAILABLE", reasons=[f"playwright not importable: {e}"])
    with sync_playwright() as p:
        b, exe, tried = _launch(p)
        if b is None:
            return dict(status="UNAVAILABLE", reasons=["no browser started"] + tried)
        errors = []
        try:
            pg = b.new_page()
            pg.on("pageerror", lambda e: errors.append(str(e)))
            pg.route(re.compile(r"^https?://"), lambda route: route.abort())
            pg.goto("file://" + os.path.abspath(html_path), wait_until="load", timeout=30000)
            tabs = pg.eval_on_selector_all("#tabs button", "bs => bs.map(b => b.textContent.trim())")
            panes = {k: pg.evaluate("id => { const e = document.getElementById(id); return e ? e.textContent : null }",
                                    "pane-" + k) for k in PANES}
            shown = {}
            for i, label in enumerate(tabs):
                pg.click(f"#tabs button:nth-child({i + 1})", timeout=10000)
                shown[label] = pg.evaluate("() => [...document.querySelectorAll('section.pane')]"
                                           ".filter(s => !s.hidden).map(s => s.id)")
            return dict(status=None, tabs=tabs, errors=errors, panes=panes, shown=shown, browser=f"{b.version} ({exe})")
        except Exception as e:  # noqa: BLE001 — a page that cannot be opened or driven fails the check, loudly
            errors.append(f"render error: {str(e).splitlines()[0][:200]}")
            return dict(status=None, tabs=[], errors=errors, panes={}, shown={}, browser=f"{b.version} ({exe})")
        finally:
            b.close()


def judge(r):
    """The PASS rule over a render() result: (status, reasons)."""
    if r.get("status") == "UNAVAILABLE":
        return "UNAVAILABLE", r["reasons"]
    reasons = [f"page error: {e}" for e in r["errors"]]
    if r["tabs"] != TABS:
        reasons.append(f"tabs {r['tabs']} (want {TABS})")
    for k in PANES:
        if r["panes"].get(k) is None:
            reasons.append(f"pane-{k} missing")
        elif not r["panes"][k].strip():
            reasons.append(f"pane-{k} empty")
    for label, k in zip(TABS, PANES):
        if label in r["shown"] and r["shown"][label] != ["pane-" + k]:
            reasons.append(f"tab {label} shows {r['shown'][label]}")
    return ("PASS" if not reasons else "FAIL"), reasons


def check(html_path):
    r = render(html_path)
    status, reasons = judge(r)
    return dict(r, status=status, reasons=reasons)


def line(res, name):
    if res["status"] == "PASS":
        return f"DECK RENDER: PASS — {name}: {len(res['tabs'])} tabs, 0 page errors, every pane drawn ({res['browser']})"
    return f"DECK RENDER: {res['status']} — {name}: " + "; ".join(res["reasons"])


def main():
    if len(sys.argv) != 2:
        print(__doc__); return 2
    res = check(sys.argv[1])
    print(line(res, os.path.basename(sys.argv[1])))
    return 0 if res["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
