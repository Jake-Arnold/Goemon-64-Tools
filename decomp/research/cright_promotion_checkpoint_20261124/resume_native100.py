"""Resume an interrupted native100 compile only from an authenticated staged JP2428.

Use the independently generated original Splat layout matching the historical
native100 manifest's owner paths. The complete native100 gates are unchanged.
"""
from pathlib import Path
import argparse,json,hashlib
from decomp import native251_promotion as n
from decomp import japan_cright6_promotion as j


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--checkout',type=Path,required=True)
    p.add_argument('--reference',type=Path,required=True)
    p.add_argument('--work',type=Path,required=True)
    p.add_argument('--uv',default='uv');p.add_argument('--jobs',type=int,default=4)
    a=p.parse_args();co=a.checkout;bd=co/'build/japan_0';prior=a.work/'accepted2428-before-native100.elf'
    expected=json.loads((n.ROOT/'results/japan_0_2528_native100_g2_20261123.json').read_text())
    def require(ok,msg):
        if not ok:raise ValueError(msg)
    rom=n.original(co,'japan_0');require(n.original(a.reference,'japan_0')==rom,'wrong original Splat ROM')
    require(n.sha(prior.read_bytes())==expected['predecessor_elf_sha256'] and (bd/'mnsg.elf').read_bytes()==prior.read_bytes() and (bd/'mnsg.z64').read_bytes()==rom,'wrong staged predecessor')
    require(n.sha((co/'tools/ido-5.3/cc').read_bytes())==j.COMPILER_SHA,'wrong native IDO')
    stage=json.loads((bd/'promo251-stage.json').read_text());fs=n.rows('japan_0');n.verify_japan_rows(fs)
    require(not stage['blocked'] and len(stage['functions'])==100 and n.sha((co/'.splat/japan_0/mnsg.ld').read_bytes())==stage['linker_sha256'],'wrong interrupted stage')
    byname={f['name']:f for f in fs}
    require({f['name'] for f in stage['functions']}==set(byname),'wrong stage function set')
    for f in stage['functions']:
        require(all(f.get(k)==v for k,v in byname[f['name']].items()),'manifest drift '+f['name'])
        require(f['staged_path']=='src/promo251/'+f['name']+'.c','wrong staged path')
        # Prove independently generated original reference before recompiling.
        off=f['rom_offset'];size=f['original_bytes']
        n.get_original_splat_lines(a.reference/'asm/japan_0'/f['owner'],f['name'],off,f['vma'],size,rom[off:off+size])
    # Restart target compilation from pristine objects; never reuse an object
    # partially trimmed before the interrupted verification.
    for f in stage['functions']:(bd/(f['staged_path']+'.o')).unlink(missing_ok=True)
    for f in stage['fragments']:
        path=Path(f['path']);require(path.parent.as_posix()=='asm/japan_0' and path.name.startswith('promo251_') and path.suffix=='.s','wrong staged fragment path');(bd/(f['path']+'.o')).unlink(missing_ok=True)
    compiled=n.compile_pack(co,'japan_0',stage,a.reference,a.uv,a.jobs)
    require(compiled['positive_full_flags']==100 and not compiled['failures'],'native100 compile failed')
    g=n.opening.stable_globals(prior);fixes=[]
    for fn,sym,size in n.JP_ABS_FIXES:
        f=next(f for f in stage['functions'] if f['name']==fn)
        fixes.append({'function':fn,**n.restore_undefined_type(bd/(f['staged_path']+'.o'),sym,size,g)})
    audit=n.link_and_check(co,'japan_0',stage,prior,a.uv,a.jobs)
    require(all(audit[k] for k in ('rom_exact','func_exact','relocs_exact','globals_exact','ownership_exact')) and audit['new_ownership']==100,'native100 full original linked proof failed')
    actual=n.sha((bd/'mnsg.elf').read_bytes());require(actual==expected['candidate_elf_sha256'],'JP2528 canonical ELF fingerprint differs')
    print(json.dumps({'status':'PASSED_G2_LOCAL','before_C':2428,'after_C':2528,'candidate_elf_sha256':actual,'abs_metadata_fixes':fixes,'audit':audit},indent=2))

if __name__=='__main__':main()
