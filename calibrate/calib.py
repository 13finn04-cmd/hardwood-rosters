import json,subprocess,copy,sys,statistics as st
ROUNDS=int(sys.argv[1]) if len(sys.argv)>1 else 8
GPT='60'
base=json.load(open('../college-2026.json'))
T=json.load(open('targets.json'))
O,INS,CRE,HDL,MID,TP,FT,PAS,PER,INT,STL,BLK,ORB,DRB,POT=11,12,13,14,15,16,17,18,19,20,21,22,23,24,27
LOCK={'Miles Byrd':85,'Devin Vanterpool':82}
rows={}
for t in base['teams']:
  for p in t['p']: rows[str(p[0])]=p
orig={k:list(v) for k,v in rows.items()}
def run(pack,out):
  json.dump(pack,open('work.json','w'),separators=(',',':'))
  subprocess.run(['node','sim.js','work.json',out,GPT],check=True)
  return json.load(open(out))
def stats(a):
  g=a[0]; return dict(min=a[1]/g,pts=a[2]/g,reb=a[3]/g,ast=a[4]/g,stl=a[5]/g,blk=a[6]/g,tpm=a[7]/g,
    fg=a[8]/a[9] if a[9] else None,tp=a[7]/a[10] if a[10] else None,ft=a[11]/a[12] if a[12] else None)
KEYS=['min','pts','reb','ast','stl','blk','tpm','fg','tp','ft']
SCALE=dict(min=4,pts=2,reb=1,ast=0.7,stl=0.3,blk=0.3,tpm=0.5,fg=0.04,tp=0.05,ft=0.06)
def errs(S):
  E={k:[] for k in KEYS};per={}
  for pid,t in T.items():
    if t['g']<3 or pid not in S: continue
    s=stats(S[pid]);sc=0;n=0
    for k in KEYS:
      if t.get(k) is None or s[k] is None: continue
      e=abs(s[k]-t[k]);E[k].append(e);sc+=e/SCALE[k];n+=1
    per[pid]=(sc/max(n,1),s)
  return {k:st.mean(v) for k,v in E.items()},per
def cl(x,lo=0,hi=99): return max(lo,min(hi,int(round(x))))
DAMP=[1.0]
def bump(p,i,d,lim=6): d=int(round(d*DAMP[0])); p[i]=cl(p[i]+max(-lim,min(lim,d)))
S=run(base,'sim_r0.json');mae0,per=errs(S)
print('R0',{k:round(v,3) for k,v in mae0.items()},flush=True)

def pava(y):
  # non-increasing isotonic fit
  bl=[[v,1] for v in y]
  i=0
  while i<len(bl)-1:
    if bl[i][0]<bl[i+1][0]:
      v=(bl[i][0]*bl[i][1]+bl[i+1][0]*bl[i+1][1])/(bl[i][1]+bl[i+1][1]);bl[i]=[v,bl[i][1]+bl[i+1][1]];del bl[i+1];i=max(0,i-1)
    else: i+=1
  out=[]
  for v,n in bl: out+= [v]*n
  return out
BIG=[]
for t in base['teams']:
  L=[p for p in t['p'] if str(p[0]) in T and (p[1]+' '+p[2]) not in LOCK]
  def tier(m): return 0 if m>=33 else 1 if m>=29 else 2 if m>=22 else 3 if m>=13 else 4
  L.sort(key=lambda p:(tier(T[str(p[0])]['min']),-p[O]))
  fit=pava([p[O] for p in L])
  for p,f in zip(L,fit):
    dlt=max(-10,min(10,int(round(f))-p[O]))
    if T[str(p[0])]['fresh']: dlt=max(0,dlt)   # keep Finn's ESPN-100 freshman floors
    if abs(dlt)>6: BIG.append((t['t'][1],p[1]+' '+p[2],p[O],p[O]+dlt,round(T[str(p[0])]['min'],1)))
    p[O]+=dlt
    if p[POT]<p[O]: p[POT]=p[O]
json.dump(BIG,open('big_ovr.json','w'))
print('iso: big moves',len(BIG),flush=True)
best={pid:(9e9,list(rows[pid])) for pid in per}
hist=[mae0]
for r in range(1,ROUNDS+1):
  DAMP[0]=1/(1+max(0,r-3)/3)
  for pid,(sc,s) in per.items():
    p=rows[pid];t=T[pid];name=p[1]+' '+p[2]
    d=lambda k:(t[k]-s[k]) if t.get(k) is not None and s[k] is not None else 0
    dm=d('min')
    if t['min']>=27 and dm<0: dm=0   # engine gives every top-5 starter 24-38 min; never demote a real starter
    if False:
      nv=p[O]+max(-2,min(2,round(dm/4)))
      p[O]=max(orig[pid][O]-10,min(orig[pid][O]+10,cl(nv)))
      if p[POT]<p[O]: p[POT]=p[O]
    bump(p,CRE,round(1.2*d('pts')))
    if p[CRE]>=97 and d('pts')>1: bump(p,INS,round(0.8*d('pts')),4); bump(p,MID,round(0.8*d('pts')),4)
    bump(p,TP,round(5*d('tpm')+40*d('tp')))
    if name=='Miles Byrd' and p[TP]<69: p[TP]=69
    bump(p,INS,round(70*d('fg')),5); bump(p,MID,round(35*d('fg')),4)
    bump(p,FT,round(90*d('ft')))
    bump(p,DRB,round(2.5*d('reb'))); bump(p,ORB,round(1.2*d('reb')),4)
    bump(p,PAS,round(3*d('ast'))); bump(p,HDL,round(1*d('ast')),3)
    bump(p,STL,round(12*d('stl'))); bump(p,BLK,round(10*d('blk')))
  S=run(base,f'sim_r{r}.json');mae,per=errs(S);hist.append(mae)
  for pid in per:
    if per[pid][0]<best[pid][0]: best[pid]=(per[pid][0],list(rows[pid]))
  print('R%d'%r,{k:round(v,3) for k,v in mae.items()},round(st.mean(x[0] for x in per.values()),3),flush=True)
for pid,(sc,row) in best.items(): rows[pid][:]=row
S=run(base,'sim_final.json');maeF,perF=errs(S)
print('FINAL',{k:round(v,3) for k,v in maeF.items()},round(st.mean(x[0] for x in perF.values()),3))
json.dump(base,open('calibrated.json','w'),separators=(',',':'))
json.dump({'before':mae0,'after':maeF},open('mae.json','w'))
