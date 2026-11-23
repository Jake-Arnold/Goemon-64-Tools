#!/usr/bin/env python3
"""Replay 142 source-only isolated native matches; not a canonical G2 gate."""
import argparse, hashlib, io, json, os, re, tarfile, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from native_probe_helpers import get_original_splat_lines, native_compile, check_exact, check_size, sha256

ROOT=Path(__file__).resolve().parent
ARCHIVE_SHA='eacfcef3777e7bee43ac8bb8adb62c5101b234fa9f012dd704e96c9c8b9a77da'
INDEX_SHA='b6b04042cd5958755fbe1d1980baff502dbfb9a2aa607080108d5c2d0a82cd6c'
IDO_SHA='76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0'
ROM_SHA={'usa':'6ea0ed71032ce08fc2745f412d84936382197494','japan_0':'6f8745fecc3a5e7d4918c7a73353eb0726116ded'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for opt in ('usa-rom','jp-rom','usa-splat','jp-splat','ido','objcopy','readelf','ledger','output'):
        p.add_argument('--'+opt,type=Path,required=True)
    p.add_argument('--jobs',type=int,default=5); a=p.parse_args()
    blob=b''.join((ROOT/'source_parts'/f'part-{i:02d}.bin').read_bytes() for i in range(5))
    assert sha256(blob)==ARCHIVE_SHA
    raw=(ROOT/'candidate-index.txt').read_bytes(); assert sha256(raw)==INDEX_SHA
    rows=raw.decode().splitlines(); candidates=[]
    for r, line in zip(rows[::2], rows[1::2]):
        for tok in line.split():
            ident,z,k=tok.split(':'); v,off=ident.split('_'); candidates.append((r,'func_'+ident,int(v,16),int(off,16),int(z),int(k)))
    assert len(candidates)==len({(r,o) for r,n,v,o,z,k in candidates})==142
    assert sum(c[4] for c in candidates)==9580 and sum(c[5] for c in candidates)==594
    assert sha256(a.ido.read_bytes())==IDO_SHA
    regions={'usa':(a.usa_rom,a.usa_splat),'japan_0':(a.jp_rom,a.jp_splat)}
    roms={r:p[0].read_bytes() for r,p in regions.items()}
    for r,b in roms.items(): assert len(b)==33554432 and hashlib.sha1(b).hexdigest()==ROM_SHA[r]
    with tarfile.open(fileobj=io.BytesIO(blob),mode='r:gz') as t:
        files={x.name:t.extractfile(x).read() for x in t.getmembers() if x.isfile()}
    assert set(files)=={f'sources/{r}/{n}.c' for r,n,v,o,z,k in candidates}
    owners={}; targets={(r,n) for r,n,v,o,z,k in candidates}
    for r,(_,root) in regions.items():
        for path in root.rglob('*.s'):
            for n in re.findall(r'^nonmatching (\w+),',path.read_text(),re.M):
                if (r,n) in targets:
                    assert (r,n) not in owners,(r,n); owners[r,n]=path
    assert set(owners)==targets
    def one(c):
        r,n,v,o,z,k=c; code=roms[r][o:o+z]
        lines=get_original_splat_lines(owners[r,n],n,o,v,z,code)
        src=files[f'sources/{r}/{n}.c']; neg,num=re.subn(r'(\b'+re.escape(n)+r'\s*\([^;{}]*\)\s*\{)',r'\1 volatile int native_negative_control = 1;',src.decode(),count=1)
        assert num==1,n
        records=[]
        with tempfile.TemporaryDirectory(prefix='native142-') as tmp:
            out=Path(tmp)
            for label,data in [('positive',src),('negative',neg.encode())]:
                f=out/(label+'.c'); f.write_bytes(data); assert a.ledger.read_text().strip()
                b,rel,syms=native_compile(a.ido,a.objcopy,a.readelf,f,out,os.environ.copy(),label)
                exact,why,diff,actual,expected=check_exact(b,code,rel,lines,z); size_ok,_=check_size(syms,n,z)
                if label=='positive': assert exact and size_ok and len(actual)==k,(n,why,diff)
                else: assert not(exact and size_ok),n
                records.append({'source_sha256':sha256(data),'exact':exact and size_ok,'reason':why if size_ok else 'FUNC_EXTENT_MISMATCH','first_difference':diff if size_ok else 0,'relocations':actual})
        return {'region':r,'name':n,'vma':v,'rom_offset':o,'original_bytes':z,'owner':str(owners[r,n].relative_to(regions[r][1])),'code_sha256':sha256(code),'compiler_quirk_outcome':'NO_NEW_COMPILER_FINDING','positive':records[0],'negative':records[1]}
    with ThreadPoolExecutor(max_workers=a.jobs) as pool: result=list(pool.map(one,candidates))
    a.output.mkdir(parents=True,exist_ok=True)
    report={'status':'PASS_ISOLATED_NATIVE_REPLAY_ONLY','count':len(result),'negative_controls_rejected':len(result),'original_bytes':9580,'symbolic_relocations':594,'complete_G2':'NOT_RUN','candidates':result}
    (a.output/'checkpoint-replay.json').write_text(json.dumps(report,indent=2)+'\n')
    print({k:v for k,v in report.items() if k!='candidates'})
if __name__=='__main__':main()
