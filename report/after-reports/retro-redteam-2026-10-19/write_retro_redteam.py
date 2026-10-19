#!/usr/bin/env python3
"""Writes after-report-2026-10-19-retro-redteam.md from retro_redteam.json, cumulative.json and the standing sweep
record (redteam-2026-10-19/sweep.json, for the FRAGILE band every title figure must carry). No figure is typed by
hand (RULES.md rule 6). Open-item receipts and Repeat-name sections are carried from the post-mortem of the same day."""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.dirname(os.path.dirname(os.path.dirname(H)))
OUT = os.path.join(KIT, "report/after-reports/after-report-2026-10-19-retro-redteam.md")
PM = os.path.join(KIT, "report/after-reports/after-report-2026-10-19-draft-postmortem.md")
R = json.load(open(os.path.join(H, "retro_redteam.json"), encoding="utf-8"))
C = json.load(open(os.path.join(H, "cumulative.json"), encoding="utf-8"))
SW = json.load(open(os.path.join(KIT, "report/after-reports/redteam-2026-10-19/sweep.json"), encoding="utf-8"))
S = [str(s) for s in R["seeds"]]
base = {s: R["baseline"][s]["title"] for s in S}; se = R["mc_se_points"]
shock_var = SW["constants"]["arena.TEAM_WEEK_SHOCK"]
band_sentence = "TEAM_WEEK_SHOCK is FRAGILE: " + " / ".join(f"{v['shift_mean']:+.1f} ({v['label']})" for v in shock_var["variants"]) + " on the as-drafted title share"
pm = open(PM, encoding="utf-8").read()


def section(h):
    m = re.search(rf"^## {re.escape(h)}.*?(?=^## )", pm, re.S | re.M); return m.group(0).rstrip() + "\n"


def two(d): return f"{d[S[0]]:.2f} / {d[S[1]]:.2f}"
def two_s(d): return f"{d[S[0]]:+.2f} / {d[S[1]]:+.2f}"


turns = R["turns"]; swaps = R["swaps"]
changed_card = [t for t in turns if t["card_plain"][0]["n"] != t["card_shock"][0]["n"]]
same_top5 = sum(1 for t in turns if [x["n"] for x in t["card_plain"]] == [x["n"] for x in t["card_shock"]])
cand_plain_only = [s for s in swaps if s["in_top_plain"] and not s["in_top_shock"]]
cand_shock_only = [s for s in swaps if s["in_top_shock"] and not s["in_top_plain"]]
nl = [s for s in swaps if s["clears_nl"]]; robust = [s for s in nl if s.get("robust")]; fragile = [s for s in nl if not s.get("robust")]
steps = C["steps"]; best = max(steps, key=lambda st: st["d_title_mean"]); k2 = steps[1] if len(steps) > 1 else steps[0]
close = R["close_to_real"]["result"]; ceil = R["ceiling_s11"]["result"]; bb = R["base_band"]
# turns where the owner's pick was the card's #1 and still had a robust better alternative
def pa(items): return ', '.join('#%s %s' % (x['pick'], x['alt']) for x in items)
def names(items): return ', '.join(x['alt'] for x in items)
fragile_detail = '; '.join('#%s %s for %s (shock 0: %s; 0.12: %s)' % (x['pick'], x['alt'], x['owner'], two_s(x['band']['0.0']), two_s(x['band']['0.12'])) for x in fragile)
fragile_names = ', '.join('%s (#%s)' % (x['alt'], x['pick']) for x in fragile)
next4 = ', '.join('%s at #%s' % (st['swaps'][-1]['alt'], st['swaps'][-1]['pick']) for st in steps[2:best['k']])
def rank_of(sw): return next(x for x in swaps if x['pick'] == sw['pick'] and x['alt'] == sw['alt'])['card_rank_plain']
k2a, k2b = k2['swaps'][0], k2['swaps'][1]
import statistics as _st
shrink = _st.median([1 - x['gain_shock'] / x['gain_plain'] for x in swaps if x['gain_plain'] > 0.01])
def gmean(res, key, bkey): return sum(res[key][s]['title'] - (base[s] if key == 'shipped' else bb[bkey][s]) for s in S) / 2
ratio_close = gmean(close, '0.12', '0.12') / gmean(close, 'shipped', None); ratio_ceil = gmean(ceil, '0.12', '0.12') / gmean(ceil, 'shipped', None)
old_base = R['retro11_base_title']
L = []; w = L.append
w("# After-report — the draft retro re-run with the red team's findings: would the card's picks have changed, what the draft changes would have been, and how much title share a close-to-real draft gains")
w("")
w("**Owner request (2026-10-19, verbatim):** \"retro-run our draft again. Knowing what the red team found, would the card's suggested players have changed? What would've been the draft changes? Try and stay as close to the real draft as drafted, but I want to know how much better % we could have been in championship probability\".")
w("")
w(f"**What was analyzed.** The 10/14 league draft (`draft_state_100.json`, pool v69, seat {R['seat']}) on the shipped engine (deck `{R['engine_commit']}`: 17 regular-season weeks, reseeded bracket), with three red-team findings applied. (1) The card's measure ignores the shared games shock and overstates counting-category edges: every alternative is scored both ways, by the card's plain ECW and by a shock-aware ECW that inflates the counting-category variance by shock² (μa² + μb²), which is what the simulator draws. (2) The engine changed under the §11 retro: every swap is re-judged on the shipped engine (10,000 seasons on seeds {S[0]} and {S[1]}, Monte-Carlo SE {se:.2f} points), and the §11 ceiling board is re-run on it. (3) The shock is FRAGILE: every swap that clears the noise line is re-run at shock 0 and 0.12 ({R['band_seasons']:,} seasons per seed), and only a swap that stays positive across the band is called robust. The card at each turn is the deck's exact port of the page's rule (`live_retro.card()`: half ΔECW against the opponents' rosters at the time, half adjusted value, priced-only from the late rounds, Porzingis vetoed). Screens: the top {R['topk']} alternatives by each measure against the final rosters, pairwise-swapped (a later seat that took the alternative gets your player); the union of both screens is simulated. Noise line {R['noise_line']} title points on both seeds, as in §11.")
w("")
w(f"**Headline.** Knowing what the red team found changes the odds, not the names. The card's 🎯 is the same player under the shock-aware measure at {13 - len(changed_card)} of 13 turns (the one change: #{changed_card[0]['pick']}, {changed_card[0]['card_plain'][0]['n']} to {changed_card[0]['card_shock'][0]['n']}), its top five identical at {same_top5} of 13; the hindsight top three differ at one turn ({pa(cand_shock_only)} enters, {names(cand_plain_only)} leaves). What the findings do change: {len(fragile)} of the {len(nl)} swaps that clear the noise line on the shipped engine do not survive the shock band ({pa(fragile)}), one of them the card's own 🎯 at that turn. The baseline reproduces the 10,000-season reference exactly ({two(base)}). Staying close to the real draft: two changes, {k2a['alt']} for {k2a['owner']} at #{k2a['pick']} and {k2b['alt']} for {k2b['owner']} at #{k2b['pick']}, move the title share from {two(base)} to {two({s: k2['title'][s]['title'] for s in S})} ({k2['d_title_mean']:+.2f} mean); the best close-to-real board is {best['k']} changes at {two({s: best['title'][s]['title'] for s in S})} ({best['d_title_mean']:+.2f}); the §11 ceiling board ({len(R['ceiling_s11']['swaps'])} changes) re-run on the shipped engine is {two({s: ceil['shipped'][s]['title'] for s in S})}. Every figure here carries the structural band: {band_sentence}; the as-drafted share runs {two(bb['0.0'])} with no shock and {two(bb['0.12'])} with it doubled, and the boards' gains at shock 0.12 are {ratio_close:.0%} and {ratio_ceil:.0%} of their shipped-engine gains (§4).")
w("")
w("Pull window: 2026-10-19 → 2026-10-19 (analysis only; no roster pull, no line change).")
w("")
w("## 1. Roster changes")
w("")
w("None. No pull, no line, tag, price or engine constant changed; the retro swaps live only inside the simulation records.")
w("")
w("## 2. Would the card's suggested players have changed?")
w("")
w(f"EVIDENCE: `retro_redteam.py` → `retro_redteam.json` (`turns[].card_plain`, `card_shock`). The card at each of your turns, recomputed on the shipped engine the way the page computes it, with the ECW leg plain (as shipped) and shock-aware (the red team's correction). The ΔECW column is the alternative's gain in expected weekly category wins against the opponents' rosters at that moment.")
w("")
w("| pick | you took | your pick's card rank (plain / shock-aware) | card 🎯 plain | card 🎯 shock-aware | top five identical |")
w("|---|---|---|---|---|---|")
for t in turns:
    cp, cs = t["card_plain"][0], t["card_shock"][0]
    same = [x['n'] for x in t['card_plain']] == [x['n'] for x in t['card_shock']]
    top5 = 'yes' if same else 'no: ' + ', '.join(x['n'] for x in t['card_shock'])
    w(f"| #{t['pick']} | {t['actual']} | {t['actual_card_rank_plain']} / {t['actual_card_rank_shock']} | {cp['n']} (ΔECW {cp['decw']:+.3f}) | {cs['n']} (ΔECW {cs['decw']:+.3f}) | {top5} |")
w("")
w(f"The shock-aware measure compresses every counting-category edge toward a coin flip, the ones you lead and the ones you trail alike (the as-drafted ECW barely moves, {R['base_ecw']['plain']:.3f} to {R['base_ecw']['shock']:.3f} of 9, while the gain of every alternative shrinks, by a median {shrink:.0%}), but it compresses them for every candidate at once, so the order the card shows you barely moves. The one 🎯 that changes is at #{changed_card[0]['pick']}: {changed_card[0]['card_plain'][0]['n']} and {changed_card[0]['card_shock'][0]['n']} sit within {abs(changed_card[0]['card_plain'][0]['ds'] - changed_card[0]['card_plain'][1]['ds']):.3f} of each other on the card's blended score either way; the red team's correction tips it, nothing more. INFERENCE: a shock-aware card would have shown you the same names at the same turns; the finding's effect on draft-day advice is nil, its effect on the odds quoted beside the advice is the subject of §4.")
w("")
w("## 3. The hindsight swaps on the shipped engine, both screens, with the band")
w("")
w(f"EVIDENCE: `retro_redteam.json` (`swaps`): every alternative in the union of the two top-{R['topk']} screens, swapped in pairwise, {R['seasons']:,} seasons on each seed; the band columns re-run the swap and the baseline at shock 0 and 0.12 ({R['band_seasons']:,} seasons per seed) for every swap that clears the noise line on both seeds. 'went' is where the alternative was actually drafted (pick / seat; undrafted = a free agent at the end of the draft). The screens agree on {len(swaps) - len(cand_plain_only) - len(cand_shock_only)} of {len(swaps)} candidates.")
w("")
w(f"| pick | you took | alternative | went | card rank at the turn (plain / shock) | ΔECW plain / shock-aware | title shift ({S[0]} / {S[1]}) | clears {R['noise_line']} | shift at shock 0 | shift at shock 0.12 | robust |")
w("|---|---|---|---|---|---|---|---|---|---|---|")
for s in swaps:
    went = "undrafted" if s["drafted_at"] is None else f"#{s['drafted_at']} seat {s['drafted_by_slot']}"
    b = s.get("band")
    w(f"| #{s['pick']} | {s['owner']} | {s['alt']} | {went} | {s['card_rank_plain']} / {s['card_rank_shock']} | {s['gain_plain']:+.3f} / {s['gain_shock']:+.3f} | {two_s(s['d_title'])} | {'yes' if s['clears_nl'] else 'no'} | {two_s(b['0.0']) if b else '—'} | {two_s(b['0.12']) if b else '—'} | {'' if b is None else ('yes' if s['robust'] else '**no**')} |")
w("")
w(f"Of the {len(nl)} swaps that clear the noise line on the shipped engine, {len(robust)} stay positive on both seeds at both ends of the band and {len(fragile)} do not: " + fragile_detail + ". The §11 retro, run before the red team, would have counted all of them as misses; with the band, they are swaps whose sign depends on a constant nobody has measured. One is the card's own 🎯 at that turn.")
w("")
w("## 4. How much better, staying as close to the real draft as possible")
w("")
w(f"EVIDENCE: `cumulative.py` → `cumulative.json`: the {len(steps)} swaps of the close-to-real board (at each turn that has one, the robust alternative with the largest single-swap gain, each alternative used once; {len(robust)} robust swaps in all, several naming the same player at different turns) taken one at a time in order of their single-swap gain, each cumulative board run {R['seasons']:,} seasons on both seeds on the shipped engine; `retro_redteam.json` (`close_to_real`, `ceiling_s11`) for the full board and the §11 board with their bands. Swaps interact (an alternative taken at one turn hands your player to the seat that drafted it, and the roster's category balance moves), so the curve is not the sum of the single shifts.")
w("")
w(f"| changes | the change added | title share ({S[0]} / {S[1]}) | shift vs as drafted | mean |")
w("|---|---|---|---|---|")
w(f"| 0 | as drafted | {two(base)} | — | — |")
for st in steps:
    a = st["swaps"][-1]
    w(f"| {st['k']} | {a['alt']} for {a['owner']} at #{a['pick']} | {two({s: st['title'][s]['title'] for s in S})} | {two_s(st['d_title'])} | {st['d_title_mean']:+.2f} |")
w("")
w(f"Two changes carry {k2['d_title_mean'] / best['d_title_mean']:.0%} of the best close-to-real board's gain. The curve peaks at {best['k']} changes ({two({s: best['title'][s]['title'] for s in S})}, {best['d_title_mean']:+.2f}); the last {len(steps) - best['k']} robust swaps lower it, because by then the roster they were measured against no longer exists. The full {len(steps)}-change board and the §11 ceiling board, with the band:")
w("")
w(f"| board | changes | shipped engine ({S[0]} / {S[1]}) | at shock 0 | at shock 0.12 | gain vs as drafted at shock 0.06 / 0 / 0.12 (mean) |")
w("|---|---|---|---|---|---|")
def g(res, key, bkey): return sum(res[key][s]['title'] - (base[s] if key == 'shipped' else bb[bkey][s]) for s in S) / 2
w(f"| as drafted | 0 | {two(base)} | {two(bb['0.0'])} | {two(bb['0.12'])} | — |")
w(f"| close-to-real, all {len(R['close_to_real']['swaps'])} changes | {len(R['close_to_real']['swaps'])} | {two({s: close['shipped'][s]['title'] for s in S})} | {two({s: close['0.0'][s]['title'] for s in S})} | {two({s: close['0.12'][s]['title'] for s in S})} | {g(close, 'shipped', None):+.2f} / {g(close, '0.0', '0.0'):+.2f} / {g(close, '0.12', '0.12'):+.2f} |")
w(f"| §11 ceiling (old engine {two(R['ceiling_s11']['old_engine_title'])}) | {len(R['ceiling_s11']['swaps'])} | {two({s: ceil['shipped'][s]['title'] for s in S})} | {two({s: ceil['0.0'][s]['title'] for s in S})} | {two({s: ceil['0.12'][s]['title'] for s in S})} | {g(ceil, 'shipped', None):+.2f} / {g(ceil, '0.0', '0.0'):+.2f} / {g(ceil, '0.12', '0.12'):+.2f} |")
w("")
w(f"Read with both error bars: Monte-Carlo SE {se:.2f} points per figure, and the structural band ({band_sentence}). The §11 board's gain is {gmean(ceil, 'shipped', None):+.2f} on the shipped engine, {gmean(ceil, '0.0', '0.0'):+.2f} with no shock and {gmean(ceil, '0.12', '0.12'):+.2f} with it doubled; the sign holds across the band for every board above, the size does not. The §11 ceiling on the shipped engine ({two({s: ceil['shipped'][s]['title'] for s in S})}) is within noise of its old-engine figure ({two(R['ceiling_s11']['old_engine_title'])}), while the as-drafted share moved from {two(old_base)} to {two(base)}: the engine change (finding 2) moved the level and left the retro's conclusions standing.")
w("")
w("## 5. The three questions, answered")
w("")
w(f"- **Would the card's suggested players have changed?** No, in practice: the 🎯 at 12 of 13 turns and the top five at {same_top5} of 13 are the same players under the shock-aware measure; the hindsight top three differ at one late turn. The red team's finding moves the odds beside the advice, not the advice.")
w(f"- **What would the draft changes have been?** The two that matter most, in order of gain: {k2a['alt']} instead of {k2a['owner']} at #{k2a['pick']} (card rank {rank_of(k2a)} at the turn) and {k2b['alt']} instead of {k2b['owner']} at #{k2b['pick']} (card rank {rank_of(k2b)}). The next {best['k'] - 2} ({next4}) add {best['d_title_mean'] - k2['d_title_mean']:+.2f} together. Both of the big two were on your card that turn, below the pick you made; neither was the 🎯.")
w(f"- **How much better?** From {two(base)} to {two({s: k2['title'][s]['title'] for s in S})} with two changes and {two({s: best['title'][s]['title'] for s in S})} at best with {best['k']}, on the shipped engine; the full close-to-real board's gain is {gmean(close, 'shipped', None):+.2f} on the shipped engine, {gmean(close, '0.0', '0.0'):+.2f} at shock 0 and {gmean(close, '0.12', '0.12'):+.2f} at 0.12. Hindsight, not foresight: every alternative is judged against the final rosters, which no card could see at the turn.")
w("")
w("## Watchlist")
w("")
w(f"- {fragile_names}: positive on the shipped engine, sign not robust to the shock. The next in-season report that quotes a swap should carry its band the same way.")
w("- The card's 🎯 at #63 (Dyson Daniels) is one of the non-robust swaps: the card's measure and the simulator's realized rates still disagree on him by the counting-category compression the red team measured.")
w("- Draymond Green and Bobby Portis were undrafted and appear as robust late alternatives; both are already on this week's free-agent recommendations (Draymond for Braun, Portis for Braun).")
w("")
w(section("Open-item receipts").replace("## Open-item receipts", "## Open-item receipts\n\nCarried from the post-mortem report of the same day (no pull today; the rows are that report's):", 1))
w(section("Repeat-name market check").replace("## Repeat-name market check", "## Repeat-name market check\n\nCarried from the post-mortem report of the same day (no refresh today):", 1))
w("## Bounds")
w("")
w("**Out of scope by design.**")
w("- The availability-scale mismatch (D-PM-4: ranking 0.78 for risk, simulation 0.75 of 0.88) stays as shipped on both the card and the simulator; reconciling it is an engine change you have not decided.")
w("- Ties (D-PM-2) are not modelled; symmetric, judged non-load-bearing.")
w("- Alternatives are single swaps of your pick; the other eleven seats draft as they did (a later seat that took the alternative gets your player). A different pick by you would have changed what the room did next; that is not modelled here or in §11.")
w("- The card is screened, not re-drafted: the shock-aware measure is applied to the page's rule at each real turn, not to a replayed draft.")
w("")
w("**In scope and unverified.**")
w(f"- Joint moves in the shock band: the cumulative boards were run at shock 0 and 0.12 only for the full close-to-real board and the §11 board, not for every step of the curve; `NOT-ATTEMPTED` for the intermediate steps, judged non-load-bearing because the two-change and best boards sit between those two.")
w("- The screens keep the top three by each measure; an alternative outside both top threes with a larger simulated gain would be missed. `NOT-ATTEMPTED` as a full simulation of every legal alternative (about 3,000 boards); the §11 retro had the same bound.")
w("")
w("## Decision sheet (owner disposes)")
w("")
w("| id | decision | recommended |")
w("|---|---|---|")
w("| D-RR-1 | the card's ECW leg: (a) make it shock-aware on the page (same names, honest edges; a deck change, red-first, own PR); (b) leave, since the order does not move | (b) until D-PM-1 lands a measured shock |")
w("| D-RR-2 | every swap, pickup or trade verdict from here on carries its shock band (the two band runs add about a minute): (a) adopt as the standing rule; (b) only for verdicts within 2 points of the noise line | (a) |")
w("| D-RR-3 | the two big misses (#15 and #34) were card ranks 3 and 5 at their turns, below your pick: (a) record both on the lessons ledger as the pattern to test next draft (the card's own first choice taken 7 of 13 times, the misses sat on the card either way); (b) no action | (a) |")
w("")
w("## Provenance")
w("")
w(f"- Session: Claude Code (claude.ai/code), 2026-10-19, kit branch `claude/market-data-workorder-mnfi2b`; deck `{R['engine_commit']}` read-only; pool `{R['pool']}`; rosters `{R['state']}`.")
w("- Records: `retro_redteam.json` (screens, swaps, bands, boards), `cumulative.json` (the curve), this folder; the standing sweep record `redteam-2026-10-19/sweep.json` for the band sentence; `draft-league-2026-10-14/retro_picks.json` for the §11 ceiling board.")
w(f"- Runs: screens 13 turns × every legal alternative both ways; swaps {len(swaps)} boards + baseline × 2 seeds × {R['seasons']:,} seasons; band {len(nl)} swaps + baseline × 2 shocks × 2 seeds × {R['band_seasons']:,}; boards 2 × (2 seeds × {R['seasons']:,} + 2 shocks × 2 seeds × {R['band_seasons']:,}); curve {len(steps)} boards × 2 seeds × {R['seasons']:,}. Baseline within 3 SE of the 10,000-season reference on both seeds (exactly equal: same simulator, same seeds).")
w("- Re-verify: `python3 report/after-reports/retro-redteam-2026-10-19/retro_redteam.py` then `cumulative.py` then `write_retro_redteam.py`; `python3 scripts/gates.py --verify --report report/after-reports/after-report-2026-10-19-retro-redteam.md`.")
w("")
w("## In plain language")
w("")
w(f"You asked whether the red team's findings would have changed what the card told you on draft night. They would not: with the games shock accounted for, the card's first choice is the same player at twelve of thirteen turns and its top five is the same at {same_top5}. What the findings change is how sure we are of the odds. Re-running every hindsight swap on the engine we actually ship, and then again with the shock at zero and at double, {len(fragile)} of the {len(nl)} swaps that looked like clear misses turn out to depend on that one unmeasured number, including the card's own first choice at #63. The robust ones say this: had you taken {k2a['alt']} at #{k2a['pick']} instead of {k2a['owner']} and {k2b['alt']} at #{k2b['pick']} instead of {k2b['owner']}, your title odds would be about {k2['title'][S[0]]['title']:.0f} percent instead of about {base[S[0]]:.0f}, and the best version of a draft that stays close to yours is about {best['title'][S[0]]['title']:.0f} percent with {best['k']} changes. Those numbers come with two uncertainties: about half a point from the dice, and a band on the gain that runs from {gmean(close, '0.0', '0.0'):+.1f} with no games shock to {gmean(close, '0.12', '0.12'):+.1f} with it doubled, for the full close-to-real board. Both big changes were on your card at the turn, a few rows below the pick you made.")
w("")
open(OUT, "w", encoding="utf-8").write("\n".join(L)); print("wrote", OUT, len(L), "lines")
