# Kit script reproducibility (run 2026-09-29 on kit main 2963d3b; every regenerated file restored with git checkout afterwards)

## rank_engine.py
 report/top-200-2026-27.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
-*Generated 2026-09-28 by `rank_engine.py` from `projections-2026-27.csv`. Method: PROMPT.md §4.2 — per-game z-scores over an iterated top-180 pool, FG%/FT% impact-weighted by volume, TOV negative, ranked by availability-adjusted value: z-total × (GP/82 + (1−GP/82)×0.20) — the streaming-credit availability model; negatives never shrunk by absence. Punt column: build where the player gains the most ranks / loses the most.*
+*Generated 2026-09-29 by `rank_engine.py` from `projections-2026-27.csv`. Method: PROMPT.md §4.2 — per-game z-scores over an iterated top-180 pool, FG%/FT% impact-weighted by volume, TOV negative, ranked by availability-adjusted value: z-total × (GP/82 + (1−GP/82)×0.20) — the streaming-credit availability model; negatives never shrunk by absence. Punt column: build where the player gains the most ranks / loses the most.*

## slate.py (default ADP_FILE = consensus-2026-09-15.csv) vs committed seat-10-slate.md
diff lines: 38
1c1
< # Seat-10 slate — EXAMPLE, board 2026-09-21 · Yahoo ADP 2026-09-15
---
> # Seat-10 slate — EXAMPLE, board 2026-09-29 · Yahoo ADP 2026-09-15

## mock_draft_league_projection.py vs committed mock-draft-2026-08-24-analysis.md
David finish: #1; record [10, 1, 0]; strong ['STL', 'BLK', 'FG%', 'TOV']; weak ['PTS', 'AST']
 report/mock-draft-2026-08-24-analysis.md | 48 ++++++++++++++++----------------
 1 file changed, 24 insertions(+), 24 deletions(-)
-| 1 | David **← YOU** | 4 | 10-1-0 | 65 | +15.2 |
+| 1 | David **← YOU** | 4 | 10-1-0 | 64 | +15.0 |

## yahoo_market.py 2026-09-22 (reparse of the committed raw paste)
TRANSCRIPTION GATE: PASS (I1-I5)
JOIN: 318 pool players | matched to yahoo=297 | unmatched=21 (possible spelling variants 0) | yahoo-only names=3
GATE PASS — every pool player matched or recorded as a genuine absence.
 M report/market/consensus-2026-09-22.csv
 M report/market/disagreements-yahoo-2026-09-22.md
 M report/market/unmatched-yahoo-2026-09-22.md

## yahoo_market.py 2026-09-15
TRANSCRIPTION GATE: PASS (I1-I5)
JOIN: 318 pool players | matched to yahoo=288 | unmatched=30 (unexplained 10) | yahoo-only names=12
HARD GATE TRIP — unexplained unmatched pool players (add a verified alias or record as a genuine absence):
changed files: 0

## build_market.py 2026-08-24 (rebuild from committed raw snapshots)
 report/market/disagreements-2026-08-24.md | 278 +++++++++++++++---------------
 report/market/provenance.csv              |   3 -
 report/market/unmatched-2026-08-24.md     | 141 ++++++++++-----
 3 files changed, 236 insertions(+), 186 deletions(-)
provenance.csv rows lost on rebuild:
-yahoo,(owner paste — no direct fetch; sports egress blocked),2026-09-16,300,"
-yahoo-9cat-rankings,(owner paste — no direct fetch; sports egress blocked),20
-yahoo,(owner paste — no direct fetch; sports egress blocked),2026-09-22,300,"

## market_stats.py 2026-09-15 vs after-report-2026-09-16-market-analysis.md
report (2026-09-16, pool 235 rows): n=214 rho(XRank)=0.762 ; n=176 rho(ADP)=0.701
matched w/ XRank: 225 | rho(our, XRank) = 0.7842
matched w/ ADP  : 182 | rho(our, ADP)   = 0.7124
(today's pool: 318 rows)
