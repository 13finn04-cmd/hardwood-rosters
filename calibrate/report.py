import json,statistics as st
exec(open('calib.py').read().split("S=run(base,'sim_r0.json')")[0].replace("base=json.load(open('../college-2026.json'))","base=json.load(open('../college-2026.json'))"))
new={str(p[0]):p for t in json.load(open('calibrated.json'))['teams'] for p in t['p']}
S0=json.load(open('sim_r0.json'));SF=json.load(open('sim_final.json'))
m0,p0=errs(S0);mf,pf=errs(SF)
rot=[pid for pid in pf if T[pid]['min']>=15]
for lab,P in (('before',p0),('after',pf)):
  print(lab,'rotation(>=15mpg) n=%d'%len(rot),{k:round(st.mean(abs(P[x][1][k]-T[x][k]) for x in rot if P[x][1][k] is not None and T[x].get(k) is not None),3) for k in KEYS})
dif=[max(abs(a-b) for a,b in zip(orig[k][11:27],new[k][11:27])) for k in new]
print('max field change',max(dif),'players changed',sum(1 for d in dif if d))
print('ovr moves: |d|>=6:',sum(1 for k in new if abs(new[k][11]-orig[k][11])>=6))
def show(pid):
  t=T[pid];o=orig[pid];n=new[pid];a=p0[pid][1];b=pf[pid][1]
  f=lambda s:' '.join('%s %.1f'%(k,s[k]) if k not in('fg','tp','ft') else '%s %s'%(k,'-' if s[k] is None else '%.0f'%(100*s[k])) for k in ['min','pts','reb','ast','tpm','fg','tp','ft'])
  print('%s %s OVR %d->%d | real: %s\n   sim before: %s\n   sim after:  %s'%(o[1],o[2],o[11],n[11],f(t),f(a),f(b)))
d=json.load(open('../college-2026.json'))
prov=[t for t in d['teams'] if t['t'][1]=='Providence'][0]
for p in prov['p']:
  if str(p[0]) in pf and T[str(p[0])]['min']>=10: show(str(p[0]))
print('---stars')
stars=sorted([k for k in pf],key=lambda k:-T[k]['pts'])[:5]
for k in stars: show(k)
