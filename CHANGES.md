# Changes

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
