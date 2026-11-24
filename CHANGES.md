# Changes

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
