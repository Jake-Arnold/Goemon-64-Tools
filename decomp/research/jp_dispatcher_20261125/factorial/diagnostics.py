"""Compare IDO diagnostic codegen with ordinary compiled variants; raw logs stay private."""
import argparse, json, pathlib, re, subprocess
import reference_helpers as h
P=pathlib.Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--upstream',type=P,required=True);p.add_argument('--repo',type=P,required=True);p.add_argument('--normal',type=P,required=True);p.add_argument('--out',type=P,required=True);a=p.parse_args();u=a.upstream.resolve();out=a.out.resolve();out.mkdir(exist_ok=False);cc=u/'tools/ido-5.3/cc';ledger=a.repo/'decomp/COMPILER_QUIRKS.md';lh=h.digest(ledger.read_bytes());assert h.run(['git','rev-parse','HEAD'],u).strip()==h.PIN;assert h.digest(cc.read_bytes())==h.CC_SHA
rows=[]
for src in sorted((P(__file__).resolve().parent/'src').glob('func_*.c')):
    ledger.read_text();assert h.digest(ledger.read_bytes())==lh
    name=re.match(r'func_8000[0-9A-F]+_[0-9A-F]+',src.stem)[0];obj=out/(src.stem+'.o');log=out/(src.stem+'.log');normal=a.normal/(src.stem+'.o');e=json.loads(normal.with_suffix('.json').read_text());assert e['source_sha256']==h.digest(src.read_bytes())
    with log.open('w') as f:subprocess.run([str(cc),*h.FLAGS,'-v','-Wc,-d','-o',str(obj),str(src)],cwd=u,stdout=f,stderr=subprocess.STDOUT,check=True)
    b=h.link(obj,name,int(name.split('_')[1],16),out,u);assert h.digest(b)==e['linked_sha256'] and h.rels(obj,u)==h.rels(normal,u)
    trace=log.read_text(errors='replace');loads=[(int(x),int(y)) for x,y in re.findall(r'^emit_rab: zlbu xr(\d+)\s+241110 xr(\d+)',trace,re.M)];masks=[(int(x),int(y)) for x,y in re.findall(r'^emit_rri: zand xr(\d+) xr(\d+)\s+255$',trace,re.M)];adds=[(int(x),int(y)) for x,y in re.findall(r'^emit_rri: zaddu xr(\d+) xr(\d+)\s+1$',trace,re.M)]
    assert len(loads)==(3 if '3C90' in name else 1)
    rows.append({'variant':src.stem,'diagnostic_linked_sha256':h.digest(b),'diagnostic_relocations_exact':True,'byte_load_dest_base':loads,'mask255_dest_src':masks,'increment_dest_src':adds})
(out/'sanitized.json').write_text(json.dumps(rows,indent=2)+'\n');print('PASS',len(rows))
