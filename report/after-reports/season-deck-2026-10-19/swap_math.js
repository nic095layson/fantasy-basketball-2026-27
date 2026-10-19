
function swapMath(inRows, outRows, cats){
  const d={}; let net=0;
  for(const c of cats){ let s=0;
    for(const r of inRows) s+=r.z[c]; for(const r of outRows) s-=r.z[c];
    d[c]=s; net+=s; }
  return {d:d, net:net};
}

const fs=require("fs"); const D=JSON.parse(fs.readFileSync("/tmp/swap_cases.json"));
let bad=0;
for(const c of D.cases){ const m=swapMath(c.inr,c.outr,D.cats);
  for(const cat of D.cats){ if(Math.abs(m.d[cat]-c.expected[cat])>1e-9) {bad++; console.log("MISMATCH",cat,m.d[cat],c.expected[cat]);} }
  if(Math.abs(m.net-c.net)>1e-9){bad++; console.log("NET MISMATCH",m.net,c.net);} }
console.log(bad===0? "SWAP MATH MIRROR: PASS - 3 cases, 27 cells + 3 nets equal python":"SWAP MATH MIRROR: FAIL "+bad);
