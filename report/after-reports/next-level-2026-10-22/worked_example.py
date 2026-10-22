#!/usr/bin/env python3
"""Worked example for the proposal's first item (owner 2026-10-22: "can this tool also analyze what categorical
contributions the free agents can provide (plus remaining games for the week) to help win my weekly matchup?").

ILLUSTRATIVE INPUTS ONLY: the team totals and the two free agents below are made-up round numbers, not any real
player or this week's matchup. What is real is the arithmetic: the per-category win probability is the kit's own
co_gm._pcat (normal approximation on the difference of two weekly totals), the per-game spread is the deck's measured
arena.SEASON_CV (2025-26 game logs, D-ZS-3) and the percentage spread uses arena.PCT_MIX_INFL, as team_week_model does.

The point it shows: in a league that scores every category separately (scoringTypeRaw "head"), the week's value of
an add is the change in expected categories won, the sum over categories of the change in P(win), and that sum is
exact by linearity, so each category's share can be shown and the shares add to the total.

    python3 report/after-reports/next-level-2026-10-22/worked_example.py --deck <deck at 048efb6>
"""
import argparse
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--deck", required=True)
    a = ap.parse_args()
    os.environ["DECK_REPO"] = a.deck
    sys.path.insert(0, os.path.join(KIT, "scripts"))
    sys.path.insert(0, os.path.join(a.deck, "arena"))
    sys.path.insert(0, os.path.join(a.deck, "scripts"))
    import arena  # noqa: E402
    import co_gm  # noqa: E402
    cv = arena.SEASON_CV

    # the matchup state with three days left (illustrative): to-date totals are known; only the remaining games vary.
    # final mean = to date + remaining mean; variance = remaining games' variance only (to date is fixed).
    me = {"PTS": (560.0, 1600.0), "BLK": (22.0, 9.0)}
    opp = {"PTS": (500.0, 1600.0), "BLK": (24.0, 9.0)}
    # FG% (illustrative): known made/attempted to date, plus remaining attempts at the team's rate
    fg = dict(me_known=(170.0, 360.0), me_rem_att=60.0, me_rate=0.475, opp_final=0.470, opp_var=0.00012)

    def p_win(m, o, c):
        return co_gm._pcat(({c: m[0]}, {c: m[1]}), ({c: o[0]}, {c: o[1]}), c)

    def add(state, line, games):
        """the state after adding a player's line for his playable games: mean and per-game variance from SEASON_CV."""
        out = dict(state)
        for c, x in line.items():
            if c in out:
                mu, var = out[c]
                out[c] = (mu + games * x, var + games * (x * cv[c]) ** 2)
        return out

    def fg_state(extra_att=0.0, extra_rate=0.0):
        mk, at = fg["me_known"]
        rem_mk = fg["me_rem_att"] * fg["me_rate"] + extra_att * extra_rate
        total_at = at + fg["me_rem_att"] + extra_att
        pct = (mk + rem_mk) / total_at
        var_mk = (arena.PCT_MIX_INFL ** 2) * (fg["me_rem_att"] * fg["me_rate"] * (1 - fg["me_rate"])
                                               + extra_att * extra_rate * (1 - extra_rate))
        return pct, var_mk / total_at ** 2

    def report(name, line, games, fga, fg_rate):
        base = {c: p_win(me[c], opp[c], c) for c in me}
        new_state = add(me, line, games)
        new = {c: p_win(new_state[c], opp[c], c) for c in me}
        b_fg = co_gm._pcat(({"FG%": fg_state()[0]}, {"FG%": fg_state()[1]}), ({"FG%": fg["opp_final"]}, {"FG%": fg["opp_var"]}), "FG%")
        n_pct, n_var = fg_state(games * fga, fg_rate)
        n_fg = co_gm._pcat(({"FG%": n_pct}, {"FG%": n_var}), ({"FG%": fg["opp_final"]}, {"FG%": fg["opp_var"]}), "FG%")
        base["FG%"], new["FG%"] = b_fg, n_fg
        deltas = {c: new[c] - base[c] for c in base}
        print(f"{name}: {games} playable games, per game {line} on {fga} FGA at {fg_rate:.3f}")
        for c in ("PTS", "BLK", "FG%"):
            print(f"   {c:4s} P(win) {base[c]:.3f} -> {new[c]:.3f}   change {deltas[c]:+.3f}")
        total = sum(deltas.values())
        print(f"   expected categories won, these three: change {total:+.3f} (= the sum of the three changes above)")
        return total

    print("ILLUSTRATIVE numbers (made up): me PTS 560 vs 500, BLK 22 vs 24, FG% to date 170/360 with 60 attempts left")
    print(f"SEASON_CV PTS {cv['PTS']}, BLK {cv['BLK']}; PCT_MIX_INFL {arena.PCT_MIX_INFL}\n")
    s = report("Free agent S (scorer)", {"PTS": 18.0, "BLK": 0.3}, 3, 15.0, 0.420)
    r = report("Free agent R (rim protector)", {"PTS": 7.0, "BLK": 2.0}, 3, 5.0, 0.600)
    print(f"\nR over S: {r - s:+.3f} expected categories this week")


if __name__ == "__main__":
    main()
