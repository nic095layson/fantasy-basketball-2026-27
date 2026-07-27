# Method change 2026-07-27 — streaming-credit availability

**What changed.** `rank_engine.py` availability adjustment:
`z_total × GP/82` → `z_total × (GP/82 + (1 − GP/82) × 0.20)` for positive
values; negative per-game values are no longer multiplied by the GP fraction
at all. Punt-column ordering mirrors the same rule. PROMPT.md §4.2 amended
to match.

**Why (two defects, one fix).**
1. *Linear GP/82 contradicted the system's own calibrated law.* The deck
   plane's 0.78 risk multiplier is arena-calibrated deliberately ABOVE
   realized game-count ratios "because missed games are partly replaceable
   via streaming" (scripts/hoops.py, owner ruling 2026-07-12). The draft-kit
   was the only subsystem pricing a missed game as a total loss. STREAM_R
   is derived from that anchor: solve a + (1−a)·r = 0.78 at the risk-class
   GP centroid a ≈ 0.72 → r ≈ 0.20. No new free parameter was invented.
2. *Linear GP/82 rewarded absence for negative-value rows.* Multiplying a
   negative z-total by a small GP fraction shrinks it toward zero: a 15-GP
   Achilles-rehab season (DiVincenzo) ranked #93, ahead of ~100 playable
   players. scripts/hoops.py has always guarded this ("never boosts
   negatives"); the kit now matches.

**External trigger.** A 2026-07-27 Yahoo expert top-50 (9-cat) exposed the
kit's injury-star divergence pattern; introspection traced it to the model
inconsistency above. Expert proximity was NOT the criterion — the same
expert list is internally inconsistent on recovery stars (Achilles-return
Haliburton 13th vs ACL-return Kyrie 48th) — internal consistency with the
arena-calibrated law was.

**Effect (220 rows, deterministic, regenerated twice):** 65 moves ≥3 ranks;
7 moves ≥10. Entered top-200: AJ Green, Ron Holland. Exited: Gradey Dick,
Jalen Wilson (two-way). Largest: DiVincenzo 93→159, Middleton 170→186,
LeBron 121→132 (relative displacement — low z-total earns little credit),
Kawhi 34→26, Embiid 29→22, Tatum 19→17, AD 9→8, Bridges 125→115. Healthy
top-7 unchanged.

**Not changed.** The deck plane keeps its tag-based 0.78 law (already
calibrated); z-scores, pool, and punt math untouched.
