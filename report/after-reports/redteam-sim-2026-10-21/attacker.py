#!/usr/bin/env python3
"""A-9 attacker: weekly H2H 9-cat simulator re-implemented from SPEC.md alone.

Usage: python3 -I attacker.py <fixture.json> <attacker_out.json> [seed] [N]
Standard library only.
"""
import json
import math
import random
import sys

CATS = ["FG%", "FT%", "3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO"]
COUNTING = ["3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO"]
COL = {"3PTM": "tpm", "PTS": "pts", "REB": "reb", "AST": "ast",
       "ST": "stl", "BLK": "blk", "TO": "tov"}
CV = {"PTS": 0.30, "REB": 0.35, "AST": 0.40, "3PTM": 0.55,
      "ST": 0.70, "BLK": 0.75, "TO": 0.50}

CHOICES = [
    "S1 tag: note.lower(), then cut at the first character c with c.isspace() or c == '(' (Python str.isspace = Unicode whitespace); no strip of leading whitespace; in this fixture every cut lands on an ASCII space or '('.",
    "S1 tag: punctuation left in the tag is kept, so 'inj-risk;' fails rule 4 (does not end with '-risk', does not equal 'inj-risk') and lands on rule 6 (contains 'risk') = 0.75; 'out-retired;' still starts with 'out-' = 0.0; 'acl-recovery-jan26' fails rule 3 and lands on rule 5 = 0.0.",
    "S1 tag: notes that begin with a date ('10/8: ...', '9/30: ...') have the date as their tag, which matches no rule, so a = 0.88 regardless of any injury wording later in the note (taken literally: everything after the cut is prose).",
    "S1 tags such as 'unsigned', 'waived', 'traded' do not start with 'out-' and get 0.88 (rule 1 tests the prefix only, not the prose meaning).",
    "S2 hash: k and salt reduced mod 2^32 before imul (all fixture values are small non-negative ints); the string is hashed exactly as it appears in the JSON (no Unicode normalization), as UTF-16LE code units (surrogate pairs would be two units).",
    "S3 games: sequential if/elif on u: u<0.08 -> 2, elif u<0.63 -> 3, elif u<0.98 -> 4, else 5.",
    "S3 day pick: the 'sum of W over the days still available' and the cumulative walk are both float sums in ascending day order; strict r < cumulative; fallback to the last available day only if no day qualifies.",
    "S3 every player listed in the roster takes part in the daily fill (a = 0 players draw games but never play, so they get w = 1.0 and contribute 0 to S4 because g = 0).",
    "S3 'played' counts every played game whether or not the player started; slots are reset every day of every trial; the z_sum-desc/name-asc order uses Python string comparison (code point order) for name ties.",
    "S3 specific slots are scanned in the listed order PG, SG, G, SF, PF, F, C, C (eligibility PG={PG}, SG={SG}, G={PG,SG}, SF={SF}, PF={PF}, F={SF,PF}, C={C}); then Util, Util.",
    "S4 every roster player is summed (no lineup cap beyond w); arithmetic evaluated left to right as written, squares computed as t*t (not pow), 1.15^2 as 1.15*1.15, gvar as (3.5*a)*(1-a).",
    "S4 FG%/FT%: the 'FGA = 1 if it is 0' substitution is applied to the team (weighted, games-scaled) attempt total, in both p and var.",
    "S5 pcat['A|B'][TO] = 1 - Phi(d) with d = (mu_A - mu_B)/sqrt(var_A+var_B), i.e. the probability A has fewer turnovers; Phi via math.erf; sqrt == 0 replaced by 1e-9.",
    "S5 pwins: summed over opponents in seat order, categories in S0 order, using the TO-flipped value, divided by 11.",
    "S6 RNG: Python random.Random(seed) (Mersenne Twister); normals via random.gauss; Normal(1, 0.06) read as mean 1, standard deviation 0.06; Normal(mean, sigma) with sigma the standard deviation.",
    "S6 TO is a counting category, so its mean IS multiplied by the games shock; FG% and FT% are not. sigma is never scaled by the shock.",
    "S6 sigma_c = sqrt(var_c) if that is > 0, else 1e-6.",
    "S6 per matchup draw order: s_a, s_b, then for each category in S0 order X_a then X_b (affects only the random stream, not the distribution).",
    "S6 an exact tie X_a == X_b (probability zero) counts as a win for neither in wins_a, so b is credited via 9 - wins_a.",
    "S6 weekly pairing: random.shuffle of the seat list ['1'..'12'] then pairs (0,1),(2,3),...,(10,11); standings are total category wins over the 17 regular weeks only.",
    "S6 seeding tie-break: each team gets an independent U(0,1) key each season; sort by (-record, key), equivalent to a uniformly random order among tied teams.",
    "S6 playoffs use the same matchup model as the regular season (fresh shocks and draws); the first-listed team (higher seed) advances on wins_a >= 5, otherwise the other team advances.",
    "S6 reseed: the four QF winners sorted by original seed s1<s2<s3<s4; semis s1 v s4 and s2 v s3 (higher seed first); final with the higher original seed listed first.",
    "S6 shares are fractions of N seasons (title count / N, playoff appearances / N), not percentages.",
]

W = (1.3, 0.7, 1.4, 0.8, 1.5, 0.9, 1.4)
SLOTS = [frozenset(["PG"]), frozenset(["SG"]), frozenset(["PG", "SG"]),
         frozenset(["SF"]), frozenset(["PF"]), frozenset(["SF", "PF"]),
         frozenset(["C"]), frozenset(["C"])]
N_SPECIFIC = len(SLOTS)  # 8; then 2 Util slots (indices 8, 9)
M32 = 0xFFFFFFFF


# ---------------------------------------------------------------- S1
def note_tag(note):
    low = note.lower()
    for i, ch in enumerate(low):
        if ch.isspace() or ch == "(":
            return low[:i]
    return low


def availability(note):
    t = note_tag(note)
    if t.startswith("out-"):
        return 0.0
    if "mild" in t:
        return 0.79
    if t.endswith("-recovery"):
        return 0.0
    if t.endswith("-risk") or t == "risk" or t == "inj-risk":
        return 0.75
    if "recovery" in t:
        return 0.0
    if "risk" in t:
        return 0.75
    return 0.88


# ---------------------------------------------------------------- S2
def imul(a, b):
    return (a * b) & M32


def hsh(s, k, salt):
    h = 2166136261 ^ imul(k & M32, 2654435761) ^ imul(salt & M32, 2246822519)
    data = s.encode("utf-16-le")
    for i in range(0, len(data), 2):
        c = data[i] | (data[i + 1] << 8)
        h ^= c
        h = imul(h, 16777619)
    h ^= h >> 15
    h = imul(h, 2246822507)
    h ^= h >> 13
    h = imul(h, 3266489909)
    h ^= h >> 16
    return h / 4294967296


# ---------------------------------------------------------------- S3
def start_weights(roster, K=32):
    starts = {p["player"]: 0 for p in roster}
    played = {p["player"]: 0 for p in roster}
    for k in range(K):
        by_day = [[] for _ in range(7)]
        for p in roster:
            name = p["player"]
            a = availability(p["note"])
            u = hsh(name, k, 1)
            if u < 0.08:
                n = 2
            elif u < 0.63:
                n = 3
            elif u < 0.98:
                n = 4
            else:
                n = 5
            avail = list(range(7))
            for j in range(n):
                total = 0.0
                for d in avail:
                    total += W[d]
                r = hsh(name, k, 10 + j) * total
                cum = 0.0
                pick = avail[-1]
                for d in avail:
                    cum += W[d]
                    if r < cum:
                        pick = d
                        break
                avail.remove(pick)
                if hsh(name, k, 20 + pick) < a:
                    played[name] += 1
                    by_day[pick].append(p)
        for d in range(7):
            order = sorted(by_day[d], key=lambda q: (-q["z_sum"], q["player"]))
            open_ = [True] * 10
            for q in order:
                pos = set(q["positions"])
                slot = None
                for i in range(N_SPECIFIC):
                    if open_[i] and (SLOTS[i] & pos):
                        slot = i
                        break
                if slot is None:
                    for i in (8, 9):
                        if open_[i]:
                            slot = i
                            break
                if slot is not None:
                    open_[slot] = False
                    starts[q["player"]] += 1
    w = {}
    for p in roster:
        name = p["player"]
        w[name] = starts[name] / played[name] if played[name] > 0 else 1.0
    return w


# ---------------------------------------------------------------- S4
def team_model(roster, w):
    mu = {c: 0.0 for c in CATS}
    var = {c: 0.0 for c in CATS}
    fgm = fga = ftm = fta = 0.0
    for p in roster:
        a = availability(p["note"])
        g = 3.5 * a
        gvar = 3.5 * a * (1 - a)
        wi = w[p["player"]]
        for c in COUNTING:
            x = p[COL[c]]
            mu[c] += wi * x * g
            t = x * CV[c]
            var[c] += wi * (t * t * g + x * x * gvar)
        fgm += wi * p["fg_pct"] * p["fga"] * g
        fga += wi * p["fga"] * g
        ftm += wi * p["ft_pct"] * p["fta"] * g
        fta += wi * p["fta"] * g
    for cat, made, att in (("FG%", fgm, fga), ("FT%", ftm, fta)):
        den = att if att != 0 else 1
        pr = made / den
        mu[cat] = pr
        var[cat] = 1.15 * 1.15 * max(pr * (1 - pr), 1e-4) / den
    return {c: [mu[c], var[c]] for c in CATS}


# ---------------------------------------------------------------- S5
def pcat(m, o):
    out = {}
    for c in CATS:
        s = math.sqrt(m[c][1] + o[c][1])
        if s == 0:
            s = 1e-9
        d = (m[c][0] - o[c][0]) / s
        P = 0.5 * (1 + math.erf(d / math.sqrt(2)))
        out[c] = 1 - P if c == "TO" else P
    return out


# ---------------------------------------------------------------- S6
def season_mc(seats, models, N, seed):
    rng = random.Random(seed)
    gauss = rng.gauss
    is_count = [c in COUNTING for c in CATS]
    is_to = [c == "TO" for c in CATS]
    MU = {}
    SG = {}
    for s in seats:
        MU[s] = [models[s][c][0] for c in CATS]
        SG[s] = [(math.sqrt(models[s][c][1]) if math.sqrt(models[s][c][1]) != 0 else 1e-6)
                 for c in CATS]
    idx = range(len(CATS))

    def matchup(a, b):
        sa = gauss(1.0, 0.06)
        sb = gauss(1.0, 0.06)
        mua, mub, sga, sgb = MU[a], MU[b], SG[a], SG[b]
        wins = 0
        for i in idx:
            if is_count[i]:
                ma = mua[i] * sa
                mb = mub[i] * sb
            else:
                ma = mua[i]
                mb = mub[i]
            xa = gauss(ma, sga[i])
            xb = gauss(mb, sgb[i])
            if is_to[i]:
                if xa < xb:
                    wins += 1
            else:
                if xa > xb:
                    wins += 1
        return wins

    def play(x, y):
        return x if matchup(x, y) >= 5 else y

    title = {s: 0 for s in seats}
    playoffs = {s: 0 for s in seats}
    for _ in range(N):
        rec = {s: 0 for s in seats}
        for _wk in range(17):
            order = list(seats)
            rng.shuffle(order)
            for i in range(0, 12, 2):
                a, b = order[i], order[i + 1]
                wa = matchup(a, b)
                rec[a] += wa
                rec[b] += 9 - wa
        key = {s: rng.random() for s in seats}
        ranked = sorted(seats, key=lambda s: (-rec[s], key[s]))
        top = ranked[:8]
        seed_of = {s: i for i, s in enumerate(top)}
        for s in top:
            playoffs[s] += 1
        qf = [(0, 7), (3, 4), (1, 6), (2, 5)]
        winners = [play(top[i], top[j]) for i, j in qf]
        winners.sort(key=lambda s: seed_of[s])
        f1 = play(winners[0], winners[3])
        f2 = play(winners[1], winners[2])
        x, y = sorted([f1, f2], key=lambda s: seed_of[s])
        champ = play(x, y)
        title[champ] += 1
    return ({s: title[s] / N for s in seats}, {s: playoffs[s] / N for s in seats})


# ---------------------------------------------------------------- main
def main():
    fixture_path, out_path = sys.argv[1], sys.argv[2]
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 20261021
    N = int(sys.argv[4]) if len(sys.argv) > 4 else 20000
    with open(fixture_path, encoding="utf-8") as fh:
        fx = json.load(fh)
    rosters = fx["rosters"]
    seats = sorted(rosters.keys(), key=int)

    out = {}
    out["availability"] = {n: availability(n) for n in fx["notes"]}
    out["hash"] = [[nm, k, salt, hsh(nm, k, salt)] for nm, k, salt in fx["hash_vectors"]]
    weights = {s: start_weights(rosters[s]) for s in seats}
    out["weights"] = weights
    models = {s: team_model(rosters[s], weights[s]) for s in seats}
    out["models"] = models
    pc = {}
    for A in seats:
        for B in seats:
            if A != B:
                pc[A + "|" + B] = pcat(models[A], models[B])
    out["pcat"] = pc
    pw = {}
    for A in seats:
        tot = 0.0
        opps = [B for B in seats if B != A]
        for B in opps:
            for c in CATS:
                tot += pc[A + "|" + B][c]
        pw[A] = tot / len(opps)
    out["pwins"] = pw
    t, p = season_mc(seats, models, N, seed)
    out["season"] = {"seasons": N, "seed": seed, "title": t, "playoffs": p}
    out["choices"] = CHOICES
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
