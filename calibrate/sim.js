// Headless harness: runs Hardwood Empire's own _simAIGame on a roster pack.
// usage: node sim.js pack.json out.json [gamesPerTeam] [seedRounds]
const {chromium}=require('/Users/finnconnor/hardwood-empire/node_modules/playwright');
const fs=require('fs');
const [,,packPath,outPath,GPT='30']=process.argv;
(async()=>{
 const b=await chromium.launch({headless:true,args:['--mute-audio']});
 const pg=await b.newPage();
 await pg.addInitScript(()=>{const M=HTMLMediaElement.prototype;M.play=function(){this.muted=true;return Promise.resolve();};
  const fake=()=>new Proxy(function(){},{get:(t,k)=>k==='then'?undefined:fake(),apply:()=>fake(),construct:()=>fake()});
  window.AudioContext=window.webkitAudioContext=function(){return fake();};});
 await pg.goto('file:///Users/finnconnor/hardwood-empire/www/index.html');
 await pg.waitForTimeout(3500);
 const pack=JSON.parse(fs.readFileSync(packPath,'utf8'));
 const res=await pg.evaluate(({pack,GPT})=>{
  _PACK_PF_IDX={};pack.pf.forEach((n,i)=>_PACK_PF_IDX[n]=i);
  var _saved=_ROSTER_PACK;_ROSTER_PACK=pack;
  var ci=pack.tf.indexOf('conference');
  var teams=pack.teams.map(T=>{var r=T.p.map(P=>{var p=_packBuildPlayer(P);p._eid=String(P[0]);return p;});return {name:String(T.t[1]),conf:T.t[ci],roster:r,coach:null};});
  _ROSTER_PACK=_saved;
  var acc={};
  function add(box){box.forEach(x=>{if(x.dnp)return;var e=x.p._eid,a=acc[e]||(acc[e]=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]);
    var v=[1,x.min,x.pts,x.reb,x.ast,x.stl,x.blk,x.tpm,x.fgm,x.fga,x.tpa,x.ftm,x.fta,x.tov||0];for(var i=0;i<14;i++)a[i]+=v[i]||0;});}
  function clear(t){t.roster.forEach(p=>{p._injGamesLeft=0;});}
  function shuffle(a){for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t;}return a;}
  var byConf={};teams.forEach(t=>(byConf[t.conf]=byConf[t.conf]||[]).push(t));
  var N=+GPT, confR=Math.round(N*0.6);
  for(var r=0;r<N;r++){
    var pairs=[];
    if(r<confR){var left=[];Object.values(byConf).forEach(L=>{L=shuffle(L.slice());while(L.length>1)pairs.push([L.pop(),L.pop()]);if(L.length)left.push(L[0]);});
      shuffle(left);while(left.length>1)pairs.push([left.pop(),left.pop()]);}
    else{var L=shuffle(teams.slice());while(L.length>1)pairs.push([L.pop(),L.pop()]);}
    pairs.forEach(([A,B])=>{var g=_simAIGame(A,B);add(g.boxW);add(g.boxL);clear(A);clear(B);});
  }
  return acc;
 },{pack,GPT});
 fs.writeFileSync(outPath,JSON.stringify(res));
 await b.close();
})();
