# Changes

## 2026-11-23: Sim calibration to real college stats (calibrate-1123)

Ratings tuned so the game's own AI-game sim (_simAIGame in www/index.html, run headless and muted,
60 games per team, 60% conference) gives each player per-game stats close to his real averages.
Target = 2026-27 so far, shrunk toward 2025-26 by g/(g+8) (pc-model league.sqlite box scores);
players without a prior season use 2026-27 only. 10 rounds of damped updates, best round kept per player.

- Minutes: the engine hands out minutes by OVR rank, so OVRs were re-ordered within each team by real
  minutes tier (team average OVR unchanged). Most moves are within +/-6; 65 moves of 7-10 (list in
  calibrate/big_ovr.json). True freshmen were never lowered (keeps the ESPN 100 floors).
- Skills: cre (points), 3pt (3PM/3P%), ins/mid (FG%), ft, drb/orb, pas/hdl, stl, blk.
- Locked: Miles Byrd 85 (3PT kept >= 69), Devin Vanterpool 82 (no 2026-27 games yet, untouched).
- Mean abs error, players with 3+ games (n=4207), before -> after: MIN 7.5->6.1, PTS 2.69->2.33,
  REB 1.31->0.69, AST 0.62->0.44, STL 0.40->0.29, BLK 0.23->0.19, 3PM 0.47->0.38, FG% 11.0->8.9,
  3P% 12.1->9.7, FT% 13.7->6.8 (percent points; rotation players 15+ mpg: FG% 6.2, 3P% 7.2, FT% 4.7).
- Engine limits: top scorers top out near 16-20 ppg (usage share), and only ~8 players per team get
  real minutes, so deep rotations and 25-ppg stars can't be matched by ratings alone.
- Harness: calibrate/ (sim.js, targets.py, calib.py, report.py).

## 2026-11-23: Tester feedback pass

Thanks to our Discord testers for this round.

- Kansas (HXCZK, Grok-assisted table): each listed KU player's ratings, athleticism and IQ set to the
  average of the pack value and his value (rounded). 15 players changed. Tre White and Melvin Council Jr.
  are in his list but not in our Kansas roster, so they were not added.
- Virginia (ClingingMars, overalls): OVR = average of pack and his overall; that player's skill ratings
  moved by the same amount (kept 0-99). 17 players.
- Freshmen too low (Ethan.L): stats-based ratings underrate freshmen with few games. Source: ESPN 100
  class of 2026 (free, espn.com recruiting player rankings). For true freshmen (no earlier college season
  in our data) OVR raised to at least a floor by rank (top 10: 80, 11-25: 77, 26-50: 74, 51-100: 71),
  skills moved by the same amount, and potential raised to at least floor + 12. 40 players changed;
  6 ranked recruits not found in the pack by name.
- DeWayne Brown II (Tennessee): checked real 2026-27 line (ESPN box scores): 11.0 pts, 9.6 reb in 5 games
  (2 double-doubles). Not averaging a double-double, so left at 82.
- Billy White III (SMU): 16-31 from three (51.6%) on 5.2 attempts a game this season, so 3-point set to 85.
- Joke requests (Juke Harris 99, Louisiana unable to shoot) ignored.

## 2026-11-23: Court Standard ratings + ESPN headshots

Source: Court Standard v0.6.346 (MXV3 + GU7 50/50 mix, games through 2026-11-21) and the
v0.6.346 player cards. Players matched by ESPN id (the pack's player id).

Counts
- Players in pack: 5,539 (365 teams, unchanged)
- Matched to a Court Standard grade: 5,120; ratings changed: 5,116
- Unmatched (left exactly as before): 419
- Photos added (ESPN headshot, verified 200 + real PNG): 1,657
- Photos replaced: 0 (every existing photo link still loads)

Mapping (same rule for every player)
- OVR: rank-preserving. Matched players are sorted by Court Standard OVR and given the pack's
  existing OVR values for that same set, in order. The pack keeps its scale; the order is ours.
- inside = finishing grade (rim), or 2PT grade if finishing has no grade
- creation = creation, handle = ball security, mid = midrange, 3-point = 3PT,
  free-throw = FT, passing = passing, steal, block, off-reb, def-reb = the matching skill grades
- perimeter-D and interior-D = Court Standard defensive grade (no separate split in our system)
- If a grade is missing but the player has a real season row (150+ minutes), that one field comes
  from his latest season stats: OVR + 8 x z-score (usage for creation, 3P% and 3PA rate for 3-point,
  2P% for inside, FT% for free-throw). Used for: creation 1,967, 3-point 373, inside 90, FT 7.
- Kept as before: athleticism, IQ, potential, durability, looks, name, position, year, everything else.
- The game re-nudges sub-ratings so they compute to the OVR, keeping this shape.
