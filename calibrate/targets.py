import json,sqlite3,collections
d=json.load(open('../college-2026.json'))
ids={str(p[0]) for t in d['teams'] for p in t['p']}
c=sqlite3.connect('file:/Users/finnconnor/pc-model/data/league.sqlite?mode=ro',uri=True)
S={}
for season in ('2025-26','2026-27'):
  q=c.execute("""select b.player_id,count(*),sum(minutes),sum(pts),sum(orb+drb),sum(ast),sum(stl),sum(blk),sum(fg3m),sum(fgm),sum(fga),sum(fg3a),sum(ftm),sum(fta)
   from player_box b join games g using(game_id) where g.season=? and coalesce(g.exhibition,0)=0 and minutes>0 group by b.player_id""",(season,))
  S[season]={r[0]:r[1:] for r in q if r[0] in ids}
K=['min','pts','reb','ast','stl','blk','tpm']
T={}
for pid in ids:
  cur=S['2026-27'].get(pid); prv=S['2025-26'].get(pid)
  if not cur: continue
  g=cur[0]
  def pg(r): return [r[i]/r[0] for i in range(1,8)]
  def pct(r): return [r[8]/r[9] if r[9] else None, r[7]/r[10] if r[10] else None, r[11]/r[12] if r[12] else None]
  a=pg(cur); 
  if prv and prv[0]>=5:
    w=g/(g+8); b=pg(prv); a=[w*x+(1-w)*y for x,y in zip(a,b)]
    # percentages: pool makes/attempts with prior attempts down-weighted
    pc=[]
    for mi,ai in ((8,9),(7,10),(11,12)):
      mk=w*cur[mi]/g+(1-w)*prv[mi]/prv[0]; at=w*cur[ai]/g+(1-w)*prv[ai]/prv[0]
      pc.append(mk/at if at>0 else None)
  else: pc=pct(cur)
  T[pid]=dict(zip(K,a)); T[pid].update(g=g,fg=pc[0],tp=pc[1],ft=pc[2],fresh=not prv)
json.dump(T,open('targets.json','w'))
print(len(ids),len(T),sum(1 for v in T.values() if v['g']>=3))
