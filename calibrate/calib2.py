# Outlier pass: focused calibration on the worst sim-vs-real players. usage: python3 calib2.py [rounds]
import json,subprocess,sys,statistics as st
exec(open('calib.py').read().split("S=run(base,'sim_r0.json')")[0].replace("int(sys.argv[1]) if len(sys.argv)>1 else 8","8"))
ROUNDS=int(sys.argv[1]) if len(sys.argv)>1 else 12
W=dict(pts=3,reb=3,ast=3,min=3,tpm=1,fg=1,tp=1,ft=1)
def run(pack,out):
  json.dump(pack,open('work.json','w'),separators=(',',':'))
  subprocess.run(['node','sim.js','work.json',out,GPT],check=True); return json.load(open(out))
def aerr(s,t):
  return {k:abs(s[k]-t[k]) for k in W if t.get(k) is not None and s[k] is not None}
def zsd(S):
  E={k:[] for k in W}
  for pid,t in T.items():
    if t['g']>=3 and pid in S:
      for k,v in aerr(stats(S[pid]),t).items(): E[k].append(v)
  return {k:st.pstdev(v) for k,v in E.items()}
def comb(s,t,SD):
  e=aerr(s,t); return sum(W[k]*e[k]/SD[k] for k in e)/sum(W[k] for k in e)
def lmae(S):
  return errs(S)[0]
S0=run(base,'o_r0.json'); SD=zsd(S0)
sc0={pid:comb(stats(S0[pid]),T[pid],SD) for pid in T if T[pid]['g']>=3 and pid in S0}
def big(s,t): return abs(s['pts']-t['pts'])>=5 or abs(s['reb']-t['reb'])>=3 or abs(s['ast']-t['ast'])>=2
sel=set(sorted(sc0,key=lambda k:-sc0[k])[:300])
sel|={pid for pid in sc0 if big(stats(S0[pid]),T[pid])}
sel={p for p in sel if (rows[p][1]+' '+rows[p][2]) not in LOCK or True}
print('selected',len(sel),flush=True)
start={k:list(v) for k,v in rows.items()}
mae0=lmae(S0); w0=sum(sc0[p] for p in sel)/len(sel)
print('R0 mae',{k:round(v,3) for k,v in mae0.items()},'worst-sel score',round(w0,3),flush=True)
teams={}
for t in base['teams']:
  teams[t['t'][1]]=[str(p[0]) for p in t['p']]
tof={pid:n for n,L in teams.items() for pid in L}
best={p:(sc0[p],list(rows[p])) for p in sel}
def lim_ok(p,i,v):  # no field change >25 vs start of pass
  return max(start[p][i]-25,min(start[p][i]+25,v))
def b2(pid,i,d,lim=10):
  p=rows[pid]; d=int(round(d*DAMP[0])); p[i]=cl(lim_ok(pid,i,p[i]+max(-lim,min(lim,d))))
Sc=S0
for r in range(1,ROUNDS+1):
  DAMP[0]=1/(1+max(0,r-4)/3)
  per={p:stats(Sc[p]) for p in sel}
  # minutes: shift OVR of selected players with big minute misses, then restore team mean using unselected non-fresh players
  if r<=6:
    for n,L in teams.items():
      dl=0;moved=[]
      for pid in L:
        if pid in sel:
          t=T[pid];s=per[pid];dm=t['min']-s['min']
          if abs(dm)>=4 and rows[pid][1]+' '+rows[pid][2] not in LOCK:
            old=rows[pid][O]; step=max(-3,min(3,round(dm/5)))
            new=cl(max(start[pid][O]-10,min(start[pid][O]+10,old+step)))
            if t['fresh']: new=max(new,start[pid][O])
            rows[pid][O]=new; dl+=new-old; moved.append(pid)
            if rows[pid][POT]<new: rows[pid][POT]=new
      if dl:
        oth=[q for q in L if q in T and q not in moved and not T[q]['fresh'] and (rows[q][1]+' '+rows[q][2]) not in LOCK]
        k=0
        while dl!=0 and oth and k<200:
          q=oth[k%len(oth)]; st_=-1 if dl>0 else 1
          if abs(rows[q][O]+st_-start[q][O])<=10: rows[q][O]+=st_; dl+=st_
          k+=1
  for pid in sel:
    p=rows[pid];t=T[pid];s=per[pid]
    d=lambda k:(t[k]-s[k]) if t.get(k) is not None and s[k] is not None else 0
    b2(pid,CRE,1.5*d('pts'),8)
    if p[CRE]>=97 and d('pts')>1: b2(pid,INS,d('pts'),6); b2(pid,MID,d('pts'),6)
    b2(pid,TP,5*d('tpm')+40*d('tp'),9)
    b2(pid,INS,70*d('fg'),7); b2(pid,MID,35*d('fg'),6)
    b2(pid,FT,90*d('ft'),9)
    b2(pid,DRB,3.2*d('reb'),9); b2(pid,ORB,1.6*d('reb'),6)
    b2(pid,PAS,4*d('ast'),9); b2(pid,HDL,1.2*d('ast'),4)
    b2(pid,STL,12*d('stl'),6); b2(pid,BLK,10*d('blk'),6)
    if rows[pid][1]+' '+rows[pid][2]=='Miles Byrd':
      rows[pid][O]=85; rows[pid][TP]=max(69,rows[pid][TP])
    if rows[pid][1]+' '+rows[pid][2]=='Devin Vanterpool': rows[pid][O]=82
  Sc=run(base,f'o_r{r}.json')
  for pid in sel:
    c=comb(stats(Sc[pid]),T[pid],SD)
    if c<best[pid][0]: best[pid]=(c,list(rows[pid]))
  print('R%d'%r,round(st.mean(comb(stats(Sc[p]),T[p],SD) for p in sel),3),{k:round(v,3) for k,v in lmae(Sc).items() if k in('min','pts','reb','ast')},flush=True)
for pid,(c,row) in best.items(): rows[pid][:]=row
# team OVR mean check
import copy
json.dump(base,open('calibrated2.json','w'),separators=(',',':'))
SF=run(base,'o_final.json')
maeF=lmae(SF)
print('FINAL',{k:round(v,3) for k,v in maeF.items()})
json.dump({'sel':sorted(sel),'start':{p:start[p] for p in sel},'sd':SD},open('o_meta.json','w'))
