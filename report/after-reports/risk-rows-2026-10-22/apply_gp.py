#!/usr/bin/env python3
"""Owner 2026-10-22, on the GAUNTLET report's decision 2 (the 7 risk-tagged rows at healthy-level GP, §4 of
after-report-2026-10-21-gauntlet.md): "Per row (Recommended)", then "Murphy 70 to 64" and "Wells 72 to 66" for the two
rows the table left as "-6, or keep", and "Keep GP, research tag" for De'Andre Hunter.

Applies the -6 convention (D-1010-2, "tag + kit GP -6") to six kit rows of report/projections-2026-27.csv and
nothing else: each old value is asserted first, so a row that moved since 10/21 stops the script instead of being
overwritten. Hunter is asserted unchanged at 70. The deck already discounts all seven at x0.78 (report §4).

    python3 report/after-reports/risk-rows-2026-10-22/apply_gp.py [--check]
--check only verifies the file is in the post-change state (exit 0) without writing."""
import csv, io, os, sys
KIT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
CSV = os.path.join(KIT, "report", "projections-2026-27.csv")
CHANGES = {"Alex Sarr": (72, 66), "Keegan Murray": (72, 66), "Zach Edey": (70, 64),
           "Jaren Jackson Jr": (68, 62), "Trey Murphy III": (70, 64), "Jaylen Wells": (72, 66)}
KEEP = {"De'Andre Hunter": 70}


def main():
    check = "--check" in sys.argv
    raw = open(CSV, encoding="utf-8", newline="").read()
    rows = list(csv.reader(io.StringIO(raw)))
    head = rows[0]; i_name, i_gp = head.index("name"), head.index("gp")
    seen = {}
    for r in rows[1:]:
        n = r[i_name]
        if n in CHANGES or n in KEEP:
            seen[n] = seen.get(n, 0) + 1
            gp = int(float(r[i_gp]))
            if n in KEEP:
                assert gp == KEEP[n], f"{n}: GP {gp}, expected {KEEP[n]} (unchanged)"
                continue
            old, new = CHANGES[n]
            if check:
                assert gp == new, f"{n}: GP {gp}, expected {new} after the change"
            else:
                assert gp == old, f"{n}: GP {gp}, expected {old} before the change (moved since 10/21?)"
                r[i_gp] = str(new)
    missing = [n for n in list(CHANGES) + list(KEEP) if seen.get(n) != 1]
    assert not missing, f"not exactly one row for: {missing}"
    if check:
        print(f"RISK ROWS: PASS — {len(CHANGES)} rows at their new GP, Hunter at 70"); return
    out = io.StringIO(); w = csv.writer(out, lineterminator="\r\n" if "\r\n" in raw else "\n"); w.writerows(rows)
    open(CSV, "w", encoding="utf-8", newline="").write(out.getvalue())
    print("RISK ROWS: written — " + ", ".join(f"{n} {o}->{nw}" for n, (o, nw) in CHANGES.items()))


if __name__ == "__main__":
    main()
