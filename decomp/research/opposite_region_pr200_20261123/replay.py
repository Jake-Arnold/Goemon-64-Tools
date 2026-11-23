#!/usr/bin/env python3
"""Replay isolated original-ROM C matches and negative controls; not G2."""
import argparse, hashlib, json, os, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from native_probe_helpers import get_original_splat_lines,native_compile,check_size,check_exact,sha256

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for opt in ('usa-rom','jp-rom','usa-splat','jp-splat','ido','objcopy','readelf','ledger','output'):
        p.add_argument('--'+opt,type=Path,required=True)
    p.add_argument('--jobs',type=int,default=5)
    a=p.parse_args(); root=Path(__file__).resolve().parent
    m=json.loads((root/'manifest.json').read_text()); regions={'usa':(a.usa_rom,a.usa_splat),'japan_0':(a.jp_rom,a.jp_splat)}
    roms={r:paths[0].read_bytes() for r,paths in regions.items()}
    for r,data in roms.items():
        assert len(data)==33554432 and hashlib.sha1(data).hexdigest()==m['original_sha1'][r],r
    assert sha256(a.ido.read_bytes())==m['ido_cc_sha256']
    assert len({(c['region'],c['rom_offset']) for c in m['candidates']})==len(m['candidates'])==m['research_isolated_count']
    def one(c):
        r,n,z=c['region'],c['name'],c['original_bytes']; off=c['rom_offset']; code=roms[r][off:off+z]
        assert sha256(code)==c['code_sha256'],n
        lines=get_original_splat_lines(regions[r][1]/c['owner'],n,off,c['vma'],z,code)
        with tempfile.TemporaryDirectory(prefix='goemon-native-') as tmp:
            out=Path(tmp); results=[]
            for label,src,sh in [('positive',c['source'],c['source_sha256']),('negative',c['negative_source'],c['negative_sha256'])]:
                assert sha256((root/src).read_bytes())==sh,n
                ledger=a.ledger.read_text(); assert ledger.strip()
                b,rel,syms=native_compile(a.ido,a.objcopy,a.readelf,root/src,out,os.environ.copy(),label)
                exact,why,diff,actual,expected=check_exact(b,code,rel,lines,z)
                size_ok,_=check_size(syms,n,z)
                results.append({'exact':exact and size_ok,'reason':why if size_ok else 'FUNC_EXTENT_MISMATCH','first_difference':diff if size_ok else 0,'relocation_count':len(actual)})
                if label=='positive':
                    assert exact and size_ok and [list(t) for t in actual]==c['native_relocations'],(n,why,diff)
                else: assert not (exact and size_ok),(n,'negative accepted')
            return {'region':r,'name':n,'rom_offset':off,'bytes':z,'positive':results[0],'negative':results[1]}
    with ThreadPoolExecutor(max_workers=a.jobs) as pool: records=list(pool.map(one,m['candidates']))
    a.output.mkdir(parents=True,exist_ok=True)
    report={'status':'PASS_ISOLATED_NATIVE_REPLAY_ONLY','matches':len(records),'negative_controls_rejected':len(records),'bytes':sum(x['bytes'] for x in records),'relocations':sum(x['positive']['relocation_count'] for x in records),'full_G2':'NOT_RUN','records':records}
    (a.output/'replay-results.json').write_text(json.dumps(report,indent=2)+'\n')
    print({k:v for k,v in report.items() if k!='records'})
if __name__=='__main__': main()
