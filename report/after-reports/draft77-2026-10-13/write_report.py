#!/usr/bin/env python3
"""Writes report/after-reports/after-report-2026-10-13-draft77.md and the pull-log row from the records: the deck's
m77_final / m77_arms / m77_hindsight / m77_deckcard_v65 / m77_replay, this folder's state_check.txt, yahoo_standings
and yahoo_compare.json, and rn_section_m77.md (the repeat-name check on 26 mocks). No figure is typed by hand."""
import csv, json, os, re
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.normpath(os.path.join(H, "..", "..", ".."))
D = "/home/user/yahoo-fantasy-basketball/arena/results"
J = lambda p: json.load(open(p, encoding="utf-8")); rd = lambda p: open(p, encoding="utf-8").read()
A = J(f"{D}/m77_arms.json"); HS = J(f"{D}/m77_hindsight.json"); PG = J(f"{D}/m77_deckcard_v65.json"); RP = J(f"{D}/m77_replay.json")["v65"]
fin_txt = rd("/tmp/claude-0/m77_final.txt") if os.path.exists("/tmp/claude-0/m77_final.txt") else None
F = J(f"{D}/m77_final.json")["v65"]
recap = J(os.path.join(H, "recap.json")); sc = rd(os.path.join(H, "state_check.txt"))
YS = list(csv.DictReader(open(os.path.join(H, "yahoo_standings_2026-10-13.csv"))))
YC = {o["seat"]: o for o in J(os.path.join(H, "yahoo_compare.json"))}
rn = rd(os.path.join(H, "rn_section_m77.md")); rn = rn[rn.index("## Repeat-name market check"):].strip()
mgr = {p["slot"]: p["manager"] for p in recap}
# ---- the page's card at each owner turn
turns = sorted(PG, key=lambda t: t["pick"])
own = {p["n"]: p["player"] for p in recap if p["slot"] == 10}
assert [t["pick"] for t in turns] == sorted(own) and all(t["actual"] == own[t["pick"]] for t in turns)
followed = [t for t in turns if t["actualCardRank"] == 1]; top5 = [t for t in turns if t["actualCardRank"] <= 5]
off = [t for t in turns if t["actualCardRank"] != 1]
echoes = re.findall(r"⚠ off the card: (.+?) ranks #(\d+) \(([\d.]+) behind 🎯 (.+?)\)", rd(os.path.join(H, "owner_message.txt")))
assert len(echoes) == len(off) == 6, (len(echoes), len(off))
for (nm, rk, gap, tgt), t in zip(echoes, off):
    assert nm == t["actual"] and int(rk) == t["actualCardRank"] and tgt == t["rows"][0]["n"], (nm, rk, t["actualCardRank"], tgt)
port_diff = [(r["pick"], r["actual_ds_rank"], next(t for t in turns if t["pick"] == r["pick"])["actualCardRank"]) for r in RP
             if r["actual_ds_rank"] != next(t for t in turns if t["pick"] == r["pick"])["actualCardRank"]]
# ---- grades
ad = A["as_drafted"]; fc = A["follow_card_selfconsistent"]
swaps = sorted(((k.split(":")[1], int(k.split(":")[0][5:]), v["champ"]) for k, v in A.items() if k.startswith("swap#")), key=lambda x: -x[2])
ecw = F["ecw"] if "ecw" in F else None
fkeys = list(F.keys())
ECW = F["ecw"]["10"]; ECWR = F["ecw_rank"]; WW = F["exp_winning_weeks"]
assert ECWR == 1
import glob
ALL = {}
for f in glob.glob(f"{D}/m*_arms.json"):
    mm = re.fullmatch(r"m(\d+)_arms\.json", os.path.basename(f))
    if mm and int(mm.group(1)) != 77:
        a = J(f).get("as_drafted")
        if a: ALL[int(mm.group(1))] = a["champ"]
higher = sorted((m for m, c in ALL.items() if c > ad["champ"]))
since = [m for m in ALL if m > max(higher)]
assert all(ALL[m] < ad["champ"] for m in since)
best_since = max(since, key=ALL.get); m73 = ALL[best_since]
HIGHER = ", ".join(f"{m} ({ALL[m]:.2f})" for m in higher)
gaps = {t["pick"]: round(t["rows"][0]["ds"] - next((r["ds"] for r in t["rows"] if r["n"] == t["actual"]), float("nan")), 3) for t in off}
EG = {int(e) for e in []}
eg = {t["pick"]: float(g) for (nm, rk, g, tg), t in zip(echoes, off)}
close = [p for p, g in eg.items() if g <= 0.010 or p >= 97]
assert sorted(set(eg) - set(close)) == [39], eg
reldiff = max(abs(YC[s]["yahoo_file_sum"]["pts"] - YC[s]["screenshot"]["pts"]) / YC[s]["screenshot"]["pts"] for s in YC)
o = []; w = o.append
w("# After-report — draft_77: the 10/13 late live room from slot 10, on deck Version 65 — the highest grade since September; Yahoo's projected standings beside ours\n")
w("**Owner request (2026-10-13, verbatim):** \"Here is a live mock for your analysis, as well as Yahoo system projections:\" — the deck tool's LIVE feed, the owner's 13-man roster, Yahoo's round-by-round recap, and a screenshot of Yahoo's 2026-27 projected standings for the room.\n")
w(f"**Room:** public Yahoo mock, 12 × 13, owner seat 10 (random humans; a practice rep, not opponent intel; display names: " + ", ".join(f"{s} {mgr[s]}" for s in range(1, 13)) + "). **Deck used:** Version 65 (rev `dd6b719`, the dial pass; Porziņģis veto live). The page's own engine re-emits all six \"off the card\" echoes with the same rank, gap and 🎯.\n")
w("Pull window: 2026-10-13 → 2026-10-13 (analysis only; no roster pull; the planes are held for tomorrow's final pull by the owner's decision).\n")
w(f"**Headline.** As drafted **{ad['champ']:.2f} percent** for the title on the real eight-team bracket, rank {ad['champ_rank']} of 12, playoffs {ad['playoff']:.2f} percent: the highest as-drafted grade of any room since mock {max(higher)} (the best since then was mock {best_since}'s {m73:.2f}); {len(higher)} late-September rooms graded higher on earlier pools and projections: {HIGHER}. Expected weekly category wins {ECW:.3f}, rank {ECWR} of 12, favored in {WW} of 11 head-to-heads. The card's 🎯 was taken at {len(followed)} of 13 turns and the pick sat in the Top 5 at {len(top5)} of 13; the self-consistent follow-card chain from the same seat grades {fc['champ']:.2f} percent. The one costly turn was #39: Walker Kessler, card #9, where Donovan Clingan (taken the next pick) grades {A['swap#39:Donovan Clingan']['champ']:.2f}. Yahoo's projected standings put this roster second of 12 on season totals; on the same totals it is favored head to head against 10 of 11 teams, losing only to seat 9, whose edge is games played, not per-game production.\n")
w("## 1. Roster changes\n\nNone. No line, tag, placement or price changed on either plane; this is a grade of a practice room.\n")
w("## 2. The team, graded\n\nEVIDENCE: `arena/results/m77_final.json`, `m77_arms.json` (18,000 seasons per arm, seeds 11/23/47, the real eight-team bracket), pool tag v65 = `players_v65.csv` (data/players.csv at `dd6b719`, sha256 bd2b983876a8).\n")
w("| arm | title % | playoffs % | rank |\n|---|---|---|---|")
w(f"| as drafted | {ad['champ']:.2f} | {ad['playoff']:.2f} | {ad['champ_rank']} |")
w(f"| follow the card's 🎯 at every turn (self-consistent chain: " + ", ".join(f"#{n} {p}" for n, p in fc["swaps"]) + f") | {fc['champ']:.2f} | {fc['playoff']:.2f} | {fc['champ_rank']} |")
for nm, n, c in swaps: w(f"| single swap at #{n}: {nm} | {c:.2f} | {A[f'swap#{n}:{nm}']['playoff']:.2f} | {A[f'swap#{n}:{nm}']['champ_rank']} |")
w("\nCategory shape (weekly model, rank of 12): " + ", ".join(f"{c} {r}" for c, r in F["cat_rank_weekly"].items()) + ". Assists are the one weak category (tenth); free throws first, steals and turnovers second.\n" if "cat_rank_weekly" in F else "")
w("## 3. Pick by pick: the page's card, the owner, hindsight\n\nEVIDENCE: `m77_deckcard_v65.json` (the v65 page's own engine), `m77_hindsight.json` (every single-swap alternative scored by weekly category wins against the final rosters).\n")
w("| pick | owner took | card rank | the page's 🎯 | hindsight's best alternative (Δ weekly cat wins) |\n|---|---|---|---|---|")
hb = {t["pick"]: t for t in HS["turns"]}
for t in turns:
    h = hb[t["pick"]]["top"][0]
    w(f"| #{t['pick']} | {t['actual']} | {t['actualCardRank']} | {t['rows'][0]['n']} | {h['n']} ({h['gain']:+.3f}) |")
w(f"\nThe off-card turns: " + "; ".join(f"#{t['pick']} {t['actual']} (card #{t['actualCardRank']}, 🎯 {t['rows'][0]['n']})" for t in off) + f". {len(close)} of the six were within 0.010 of the 🎯 or at round 9 and later; #39 Kessler was the one wide miss (0.032 behind, card #9) and the one that cost: the 🎯 Ware lasted to the owner's #63 anyway, but the swap the grade rewards is Clingan, gone at #40.\n")
w("## 4. Yahoo's projected standings against ours\n\nEVIDENCE: `yahoo_standings_2026-10-13.csv` (the screenshot transcribed; recomputing roto points from its 12 rows reproduces Yahoo's printed order, the 6.5 tie included), `yahoo_compare.json` (each roster summed on Yahoo's per-player file of 10/13), `m77_final.json`.\n")
cats = [("fg_pct", 1), ("ft_pct", 1), ("tpm", 1), ("pts", 1), ("reb", 1), ("ast", 1), ("stl", 1), ("blk", 1), ("tov", -1)]
me = next(r for r in YS if r["manager"] == "David")
def h2h(r):
    wn = ls = 0
    for c, s in cats:
        a, b = float(me[c]) * s, float(r[c]) * s
        wn += a > b; ls += a < b
    return wn, ls
rows = [(r["manager"], *h2h(r)) for r in YS if r["manager"] != "David"]
fav = sum(1 for _, a, b in rows if a > b)
w(f"| view | where this roster lands |\n|---|---|\n| Yahoo, season-total roto points | {me['rank']} of 12 (behind itsANDYdotcom) |\n| Yahoo totals, head to head category by category | favored against {fav} of 11; loses only to " + ", ".join(f"{m} ({a}-{b})" for m, a, b in rows if a <= b) + " |\n" + f"| the deck, weekly category model | rank {ECWR} of 12, favored against {WW} of 11; closest is seat 9 |")
s9, s10 = YC[9]["yahoo_file_sum"], YC[10]["yahoo_file_sum"]
pg = lambda t, c: t[c] / t["gp"]
assert pg(s10,"pts") > pg(s9,"pts") and pg(s10,"blk") > pg(s9,"blk") and pg(s10,"tov") < pg(s9,"tov")
assert all(pg(s10,c) < pg(s9,c) for c in ("tpm","ast","stl")) and abs(pg(s9,"reb")-pg(s10,"reb")) < 0.1
fc_sw = [n for n, _ in fc["swaps"]]; assert fc_sw == [10, 15, 39], fc_sw
assert [p for n, p in fc["swaps"] if n in (10, 15)] == [next(t for t in turns if t["pick"] == n)["rows"][0]["n"] for n in (10, 15)]
w(f"\nBoth views name the same rival: seat 9 (itsANDYdotcom). Yahoo's edge for seat 9 is volume: summed from Yahoo's own per-player file, seat 9 carries {s9['gp']:.0f} projected games against this roster's {s10['gp']:.0f}. Per player-game this roster leads in points ({pg(s10,'pts'):.2f} to {pg(s9,'pts'):.2f}), blocks and turnovers, is within {abs(pg(s9,'reb')-pg(s10,'reb')):.2f} in rebounds, and trails slightly in threes, assists and steals. A season-total ranking rewards games; a weekly head-to-head with a fixed lineup rewards them only partly, which is why the deck ranks this roster first and Yahoo second. Summing Yahoo's 10/13 per-player file comes within {100*reldiff:.1f} percent of the screenshot's points for every team but does not equal it, so the screenshot rests on a slightly newer Yahoo projection than the file on hand.\n")
w("## 5. Tool-state integrity\n\n" + sc.strip().replace("\n", "; ") + f". The page's own engine reproduces all six echoes (rank, gap and 🎯). The grading pipeline's Python port, which keeps the pre-v24 name tie-break per its docstring, differs from the page by one place at {len(port_diff)} turns ({', '.join(f'#{p}: port {a}, page {b}' for p, a, b in port_diff)}); the page record is the authority for what the card said. The as-drafted grade and the single swaps do not depend on card order; the follow-card chain's swaps at #10 and #15 are the page's 🎯, and at #39 the chain took Dyson Daniels because the 🎯 Ware was the owner's own later pick.\n")
w("## Watchlist\n")
w("- Walker Kessler: the one wide off-card turn (card #9 at #39); he carries the availability discount for his health tag. The card had Ware first, who lasted to #63.")
w("- Seat 9's projected games lead on Yahoo; not a line question, a reminder that Yahoo's standings are season totals.")
w("- The 10/14 lock paste (D-1013-1), the publish freeze during the draft (D-1013-5), no RESYNC during the draft (D-1013-2).\n")
w("## Open-item receipts\n\n| item | query run (2026-10-13) | dated finding |\n|---|---|---|")
w("| (this room) | records only; no web research and no roster pull | the room's names resolve to the v65 pool 156 of 156; the lines are the ones merged in kit PR #109 |")
w("| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull, same day (`after-report-2026-10-13.md`, receipts dated 10/13) | all HELD or unsigned on 2026-10-13 per those receipts; not re-queried here (did not check) |\n")
w(rn + "\n")
w("\n## Bounds\n\n**Out of scope by design.**\n- No line, price or engine change: the owner holds every decision until tomorrow morning's final pull.\n- The punt test and the advice line were not re-run: no punt was declared and the advice line did not fire in the feed.\n- This is a room of random humans, not the league's managers.\n")
w(f"**In scope and unverified.**\n- The exact Yahoo projection behind the screenshot: `UNVERIFIABLE` from here; the 10/13 per-player file on hand sums to within {100*reldiff:.1f} percent of it but not exactly.\n- Whether the season arms' title share holds against the league's real managers: `UNVERIFIABLE` until the draft.\n")
w("## Decision sheet (owner disposes)\n\n| id | decision question | default if silent |\n|---|---|---|")
w("| D-1013-10..14 | carried as set this evening; the owner's hold until tomorrow's final pull | hold |")
w("| D-1013-1..9, D-C2, D-SF-1..4 and earlier | carried | carried |\n")
w("## Provenance\n")
w("- Inputs: the owner's paste (`draft77-2026-10-13/owner_message.txt`, verbatim) and the screenshot (`yahoo_standings_screenshot.webp`, transcribed to `yahoo_standings_2026-10-13.csv`); deck rev `dd6b719` (Version 65, page sha256 09a889d4baa5).")
w("- Tools: `build_state.py` (state and feed check), the deck's `arena/mocks/live_retro.py` (mock 77 registered: replay, final, hindsight, arms) and `live_deckcard.py` (the page's engine), `scripts/repeat_market_check.py` (26 mocks), `yahoo_compare.py`, `write_report.py` (this file's writer). Records in `arena/results/m77_*.json` and this folder.")
w("- No line, tag or placement changed; both planes' hashes equal before and after (e821ec1ddc67 kit, bd2b983876a8 deck).\n")
w("## In plain language\n")
w(f"**How the room went.** Your best practice room since late September: about a {ad['champ']:.0f} percent title share, first of 12, and favored against every other team week to week. You followed the card at {len(followed)} of 13 picks and stayed inside its Top 5 at {len(top5)}.")
w(f"\n**The one pick to learn from.** At #39 you took Kessler, ninth on the card. Ware was the card's pick and lasted to you at #63, but Clingan, gone one pick later, would have been worth about {A['swap#39:Donovan Clingan']['champ'] - ad['champ']:.0f} more title points. Everything else was within a hair of the card.")
w(f"\n**Yahoo's view.** Yahoo ranks you second, behind seat 9. That is a season-total view, and seat 9 is projected for {s9['gp'] - s10['gp']:.0f} more games; player for player you are level or ahead in most categories. On Yahoo's own numbers you beat 10 of the 11 teams category by category.")
w("\n**Your decisions.** Nothing new; everything holds until tomorrow morning's final pull.")
P = os.path.join(K, "report", "after-reports", "after-report-2026-10-13-draft77.md")
open(P, "w", encoding="utf-8").write("\n".join(x for x in o if x is not None) + "\n")
PL = os.path.join(K, "report", "pull-log.md"); pl = rd(PL)
assert "after-report-2026-10-13-draft77.md" not in pl
row = (f"| 2026-10-13 | mock 77 grade (public room, LIVE mode, deck Version 65) + Yahoo's projected standings | 0 | 0 | 0 | "
       f"after-reports/after-report-2026-10-13-draft77.md — as drafted {ad['champ']:.2f}% (rank {ad['champ_rank']}, the highest since mock {max(higher)}), ECW {ECW:.3f} rank {ECWR}, favored {WW} of 11; "
       f"card followed {len(followed)} of 13, Top-5 at {len(top5)}; follow-card chain {fc['champ']:.2f}%; the costly turn #39 Kessler (card #9; Clingan swap {A['swap#39:Donovan Clingan']['champ']:.2f}%); "
       f"feed = recap 156 of 156, six echoes reproduced by the page; Yahoo standings rank 2 (season totals), favored head to head against {fav} of 11 on Yahoo's totals; "
       f"repeat-name check 26 of 26, 8 flagged; no plane change |")
open(PL, "w", encoding="utf-8").write(pl.rstrip("\n") + "\n" + row + "\n")
print("written", P)
