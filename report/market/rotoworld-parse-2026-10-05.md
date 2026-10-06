# Rotoworld draft kit v2 — parse report, 2026-10-05

Source: the owner's upload of 2026-10-06 (Rotoworld / NBC Sports 2026-27 Fantasy Basketball Draft Kit v2; the PDF's modification date is 2026-10-05). Raw layer `rotoworld-raw-2026-10-05.txt` (pdfplumber text, profile pages cropped into two columns). The kit carries no projected stat lines: the profiles' lines are 2025-26 actuals.

| measure | value |
|---|---|
| cheat sheets parsed | points 200, 8-cat 200, 9-cat 200, dynasty 300 (ranks contiguous in each) |
| distinct names across the four sheets | 315 |
| profiles parsed | 141 (guards 50, forwards 50, centers 41) |
| profiles with a 2025-26 line | 131; without one (rookies, players who sat the season): 10 — Tyrese Haliburton (G5), Kyrie Irving (G19), Damian Lillard (G36), Fred VanVleet (G39), Darryn Peterson (G44), Cameron Boozer (F21), AJ Dybantsa (F35), Caleb Wilson (F36), Hannes Steinbach (C33), Aday Mara (C41) |
| 9-cat names without a profile | 62 of 200 |
| profiled names outside the 9-cat 200 | 3: Mark Williams, Ryan Kalkbrenner, Aday Mara |
| dynasty sheet's team differs from the 9-cat/points/8-cat team | 1: Day’Ron Sharpe (BKN vs dynasty CHI) |

_Inputs: rotoworld-raw-2026-10-05.txt sha256 d0f23fabc14bc626 3955 lines · as of commit cfbdf02 (2026-10-06) · by rotoworld_pdf_market.py_
