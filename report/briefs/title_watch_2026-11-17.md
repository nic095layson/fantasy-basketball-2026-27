## Title watch — 2026-11-17

| | title share |
|---|---|
| 2026-11-16 | 14.6% |
| 2026-11-17 | 14.1% |
| change | -0.5 (band ±0.7) |

**Method change between the two runs.** The two figures were not made the same way:

- line method: the minutes ratio now applies to PTS, REB, AST (before: none)
- constant arena.TEAM_WEEK_SHOCK: 0.06 to 0.11
- constant arena.weekly_availability: {'healthy': 0.88, 'mild': 0.79, 'risk': 0.75, 'recovery': 0.0, 'out': 0.0} to {'healthy': 0.8, 'mild': 0.79, 'risk': 0.65, 'recovery': 0.0, 'out': 0.0}
- constant season_lines.SWITCH_CATS added

Within the band: the change is no larger than two runs of the same simulator differ by.
