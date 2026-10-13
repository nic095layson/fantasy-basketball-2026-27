#!/usr/bin/env python3
"""Markdown tables for the MG after-report, built from the records (candidates, apply record, board diff, GP moves,
seed/final range files) — never typed. Usage: mg_report_tables.py <mg dir> <out.md>"""
import csv, json, re, sys, unicodedata, statistics as st
M, OUT = sys.argv[1:3]
J = lambda p: json.load(open(p, encoding="utf-8"))
C = J(M + "/out/candidates_2026-10-13.json")["candidates"]; A = J(M + "/out/apply_record_2026-10-13.json"); B = J(M + "/out/boarddiff_2026-10-13.json")
seed = J(M + "/out/seed_range_2026-10-13.json"); fin = J(M + "/out/range_mg_2026-10-13.json"); L = {r["key"]: r for r in J(M + "/out/lines_mg_2026-10-13.json")["rows"]}
gp = list(csv.DictReader(open(M + "/data/gp_moves_2026-10-13.csv", encoding="utf-8")))
norm = lambda s: " ".join(t for t in re.sub(r"[^a-z0-9 ]", " ", re.sub(r"[.'`,’-]", "", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower())).split() if t not in {"jr", "sr", "ii", "iii", "iv"})
ALI = {"nic claxton": "nicolas claxton", "alex sarr": "alexandre sarr", "kelly oubre": "kelly oubre"}
rows = {norm(r["player"]): r for r in B["rows"]}
kit = {("kit", x["player"]): x for x in A["rows"] if x["plane"] == "kit"}
def brow(name):
    n = norm(name); return rows.get(ALI.get(n, n)) or rows.get(n) or next((r for k, r in rows.items() if k.startswith(n.split()[0]) and n.split()[-1] in k), None)
out = []
out.append("### MG-1 minutes — the 15 triggered moves (both outlets on the same side by 1.5+)\n")
out.append("| player | why a candidate | WO-5 min | Hashtag 10/12 | Yahoo 10/06 implied | new min | pts before → after | deck rank | kit rank | range rule after |")
out.append("|---|---|---|---|---|---|---|---|---|---|")
for c in sorted([c for c in C if c["mg1"] == "MOVE"], key=lambda c: c["rank"]):
    k = kit.get(("kit", c["player"])); r = brow(c["player"]); n = norm(c["player"]); n = ALI.get(n, n)
    fe = fin.get(n, {}); se = seed.get(n, {})
    after = "re-fixed by R1 at %.1f (factor %.3f)" % (fe["minutes"], fe["factor"]) if fe.get("minutes") is not None and se.get("minutes") is None else ("new cell(s) kept on the method: " + ", ".join(sorted(set(fe.get("mechanisms", {})) - set(se.get("mechanisms", {})))) if set(fe.get("mechanisms", {})) - set(se.get("mechanisms", {})) else "—")
    actual_min = float(k["after"]["mpg"]) if k else c["new_minutes"]
    out.append(f"| {c['player']} | {', '.join(c['why'])} ({c['base']}, {c['base_g']} G) | {c['wo5_minutes']:.1f} | {c['hashtag_mpg']:.1f} | {c['yahoo_implied_minutes']:.1f} | {actual_min:.1f} | {k['before']['pts']} → {k['after']['pts']} | {r['deck_before'] if r else '—'} → {r['deck_after'] if r else '—'} | {r['kit_before'] if r else '—'} → {r['kit_after'] if r else '—'} | {after} |")
out.append("\n### MG-2 games — the 5 triggered moves (both outlets on the same side by 5+; kit column only)\n")
out.append("| player | kit GP before → after | Yahoo 10/06 | Hashtag 10/12 | kit rank | deck plane |"); out.append("|---|---|---|---|---|---|")
for g in gp:
    c = next(x for x in C if x["player"] == g["player"]); r = brow(g["player"])
    out.append(f"| {g['player']} | {g['gp_old']} → {g['gp_new']} | {int(c['yahoo_gp'])} | {int(c['hashtag_gp'])} | {r['kit_before'] if r else 'under 3'} → {r['kit_after'] if r else 'under 3'} | dated note only (availability is tag-based) |")
out.append("\n### The 32 holds\n")
out.append("| player | why a candidate | WO-5 min | Hashtag | Yahoo implied | minutes verdict | kit GP | Yahoo GP | Hashtag GP | games verdict |"); out.append("|---|---|---|---|---|---|---|---|---|---|")
for c in sorted([c for c in C if c["mg1"] != "MOVE" or c["mg2"] != "MOVE"], key=lambda c: c["rank"]):
    if c["mg1"] == "MOVE" and c["mg2"] == "MOVE": continue
    f = lambda v: "—" if v is None else (f"{v:.1f}" if isinstance(v, float) and not float(v).is_integer() else f"{int(v)}")
    out.append(f"| {c['player']} | {', '.join(c['why'])} | {c['wo5_minutes']:.1f} | {f(c['hashtag_mpg'])} | {f(c['yahoo_implied_minutes'])} | {'moved' if c['mg1']=='MOVE' else c['mg1'].replace('HOLD — ','hold: ')} | {c['kit_gp']} | {f(c['yahoo_gp'])} | {f(c['hashtag_gp'])} | {'moved' if c['mg2']=='MOVE' else c['mg2'].replace('HOLD — ','hold: ')} |")
MG = {c["player"] for c in C if c["mg1"] == "MOVE" or c["mg2"] == "MOVE"} | {"Kelly Oubre Jr."}
oth = [r for r in B["rows"] if r["player"] not in MG]
mv = lambda r, k: ((r.get(k + "_after") or 0) - (r.get(k + "_before") or 0)) if r.get(k + "_before") and r.get(k + "_after") else 0
out.append("\n### Collateral — players outside the pass who moved 3+ places (the pool's frame shifting)\n")
for k in ("deck", "kit"):
    m = [abs(mv(r, k)) for r in oth]
    out.append(f"- {k}: {sum(1 for x in m if x >= 3)} players moved 3+, {sum(1 for x in m if x >= 5)} moved 5+, {sum(1 for x in m if x >= 8)} moved 8+; the largest {max(m)} places; median {st.median([x for x in m if x >= 3]) if any(x >= 3 for x in m) else 0}.")
out.append("- The largest: " + "; ".join(f"{r['player']} deck {r['deck_before']}→{r['deck_after']}, kit {r['kit_before']}→{r['kit_after']}" for r in sorted(oth, key=lambda r: -max(abs(mv(r, 'deck')), abs(mv(r, 'kit'))))[:6]) + ".")
summ = dict(candidates=len(C), mg1=sum(c["mg1"] == "MOVE" for c in C), mg2=len(gp), deck_rows_changed=A["deck_rows_changed"], kit_rows_changed=A["kit_rows_changed"], values_changed=A["values_changed"],
            boarddiff=B["movers"], deck_movers=B["deck_movers"], kit_movers=B["kit_movers"])
open(OUT, "w", encoding="utf-8").write("\n".join(out) + "\n"); print(json.dumps(summ)); print("\n".join(out[:6]))
