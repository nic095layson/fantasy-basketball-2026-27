#!/usr/bin/env python3
"""deck_render_check.py red-first tests (owner 2026-10-21, decision B): the checker is proven on known answers before
any build relies on it — a page that draws itself passes; a script error, a missing tab, an empty pane or a tab that
shows the wrong pane fails; no browser is UNAVAILABLE, never a pass.

    python3 scripts/test_deck_render_check.py
"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deck_render_check as DRC  # noqa: E402

RENDER_OK, RENDER_WHY = DRC.available()


def page(tabs=DRC.TABS, panes=DRC.PANES, throw="", empty=(), wrong=None):
    """A minimal deck-shaped page: a script draws the tab bar and fills each pane, like season_deck.py's shell."""
    sections = "".join(f'<section class="pane" id="pane-{k}" hidden></section>' for k in panes)
    defs = ",".join(f'["{k}","{label}"]' for k, label in zip(DRC.PANES, tabs))
    fill = ";".join(f'document.getElementById("pane-{k}").textContent="{k} content"' for k in panes if k not in empty)
    show_expr = f'(id==="{wrong[0]}"?"{wrong[1]}":id)' if wrong else "id"
    return f"""<title>t</title><nav id="tabs" role="tablist"></nav>{sections}
<script>
{fill};
{throw}
const defs=[{defs}], tabs=document.getElementById("tabs");
function show(id){{ const t={show_expr}; for(const [k] of defs){{ const e=document.getElementById("pane-"+k); if(e) e.hidden = k!==t; }} }}
for(const [id,label] of defs){{ const b=document.createElement("button"); b.textContent=label; b.onclick=()=>show(id); tabs.append(b); }}
show("today");
</script>"""


@unittest.skipUnless(RENDER_OK, RENDER_WHY)
class KnownAnswers(unittest.TestCase):
    def check(self, html):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "deck.html")
            with open(p, "w", encoding="utf-8") as f:
                f.write(html)
            return DRC.check(p)

    def test_a_page_that_draws_itself_passes(self):
        r = self.check(page())
        self.assertEqual(r["status"], "PASS", r["reasons"])
        self.assertEqual(r["tabs"], DRC.TABS)

    def test_a_script_error_fails_even_with_every_pane_id_in_the_html(self):
        # the 10/21 shape: the panes are in the HTML text, the script throws before the tab bar is drawn
        r = self.check(page(throw="null.toFixed();"))
        self.assertEqual(r["status"], "FAIL")
        self.assertTrue(any("page error" in x for x in r["reasons"]), r["reasons"])
        self.assertTrue(any(x.startswith("tabs []") for x in r["reasons"]), r["reasons"])

    def test_a_missing_tab_fails(self):
        r = self.check(page(tabs=DRC.TABS[:5], panes=DRC.PANES))
        self.assertEqual(r["status"], "FAIL")
        self.assertTrue(any(x.startswith("tabs ") for x in r["reasons"]), r["reasons"])

    def test_an_empty_pane_fails(self):
        r = self.check(page(empty=("week",)))
        self.assertEqual(r["status"], "FAIL")
        self.assertIn("pane-week empty", r["reasons"])

    def test_a_tab_that_shows_the_wrong_pane_fails(self):
        r = self.check(page(wrong=("movers", "board")))
        self.assertEqual(r["status"], "FAIL")
        self.assertTrue(any(x.startswith("tab Movers shows") for x in r["reasons"]), r["reasons"])

    def test_a_page_that_cannot_be_opened_fails_cleanly(self):
        r = DRC.check(os.path.join(tempfile.gettempdir(), "no-such-dir-deck", "deck.html"))
        self.assertEqual(r["status"], "FAIL")
        self.assertTrue(any("render error" in x for x in r["reasons"]), r["reasons"])

    def test_an_error_on_clicking_a_tab_fails(self):
        html = page().replace("b.onclick=()=>show(id)", 'b.onclick=()=>{ if(id==="week") undefined.x; show(id); }')
        r = self.check(html)
        self.assertEqual(r["status"], "FAIL")
        self.assertTrue(any("page error" in x for x in r["reasons"]), r["reasons"])


class Unavailable(unittest.TestCase):
    def test_no_browser_is_unavailable_never_a_pass(self):
        r = DRC.judge(dict(status="UNAVAILABLE", reasons=["no browser started"]))
        self.assertEqual(r, ("UNAVAILABLE", ["no browser started"]))

    def test_an_empty_browser_folder_is_unavailable(self):
        saved = {k: os.environ.get(k) for k in ("PLAYWRIGHT_BROWSERS_PATH", "DECK_CHROMIUM")}
        with tempfile.TemporaryDirectory() as empty:
            os.environ["PLAYWRIGHT_BROWSERS_PATH"] = empty
            os.environ.pop("DECK_CHROMIUM", None)
            try:
                r = DRC.check(os.path.join(empty, "deck.html"))
            finally:
                for k, v in saved.items():
                    if v is None:
                        os.environ.pop(k, None)
                    else:
                        os.environ[k] = v
        self.assertEqual(r["status"], "UNAVAILABLE", r["reasons"])
        self.assertIn("PASS", DRC.line(dict(status="PASS", tabs=DRC.TABS, browser="b"), "x"))
        self.assertTrue(DRC.line(r, "x").startswith("DECK RENDER: UNAVAILABLE"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
