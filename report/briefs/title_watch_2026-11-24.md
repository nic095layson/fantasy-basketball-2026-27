## Title watch — 2026-11-24

| | title share |
|---|---|
| 2026-11-23 | 13.2% |
| 2026-11-24 | 14.8% |
| change | +1.6 (band ±0.7) |

**Method change between the two runs.** The two figures were not made the same way:

- constant season_lines.KIT_ROW_GP_QUANTILE added

**Like for like.** The same change on today's engine, one input at a time (each row is a run of the simulator; a step smaller than about ±0.7 is noise):

| step | change | title share after |
|---|---|---|
| the 2026-11-23 brief | | 13.2% |
| the engine and its constants, on the earlier run's inputs | +0.0 | 13.2% |
| rosters and results recorded since | +1.1 | 14.3% |
| the lines file (line method and the day's games) | +0.6 | 14.8% |

**The title share moved by more than the band.** What changed between the two runs:

- METHOD CHANGE: constant season_lines.KIT_ROW_GP_QUANTILE added; part or all of the move is the method, not the league.
- 7 kit merge(s): #290 from nic095layson/claude/new-session-koi1jp; #300 from nic095layson/claude/register-kit-row-gp; #301 from nic095layson/claude/deck-test-run-block; #302 from nic095layson/claude/runner-copy-and-gates-rule; #303 from nic095layson/claude/playbook-2026-11-23; #304 from nic095layson/claude/playbook-braun-lesson; #305 from nic095layson/claude/confidence-2026-11-23.
- 7 team(s) changed rosters: Looking Cool Joker!: added Anfernee Simons, dropped Aaron Nesmith; ANONG NANGIANNIS?!: added Terrence Shannon Jr, dropped Nolan Traore; Thompson Telepathy: added De'Andre Hunter, dropped Collin Sexton; Podz save the league: added Buddy Hield, Cameron Johnson, dropped Caleb Martin, Ja'Kobe Walter, Keaton Wagler, off IL Brandon Miller; ROOKS FTW: added Svi Mykhailiuk, dropped Jaxson Hayes; your team: added Collin Gillespie, dropped Andrew Wiggins; John's Cool Team: dropped Sam Hauser, off IL Jayson Tatum.

The walk above splits the move between the engine, the rosters and the lines; inside a step it does not split further.
