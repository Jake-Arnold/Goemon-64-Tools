#!/usr/bin/env python3
"""Recompile 28 JP C sources/negative controls with original IDO and ROM/ASM.

Isolated body verification is supplemental to decomp.japan_short28_promotion's
complete 32MiB ROM, ELF and complete relocation proofs. Publishes no ROM bytes.
"""
import argparse, hashlib, json, os
from pathlib import Path
from native_probe_helpers import (get_original_splat_lines, native_compile,
                                  check_exact, check_size)

def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    p=argparse.ArgumentParser(description=__doc__)
    for k in ('jp-rom','jp-splat','ido','objcopy','readelf','ledger','output'):
        p.add_argument('--'+k,type=Path,required=True)
    a=p.parse_args();here=Path(__file__).resolve().parent
    data=json.loads((here/'manifest.json').read_text());rows=data['functions']
    if (len(rows)!=28 or sum(r['size'] for r in rows)!=1980 or
        sum(r['native_relocation_count'] for r in rows)!=124):
        raise ValueError('Not 28 original Japanese functions')
    if sha(a.ido.read_bytes())!=data['ido_cc_sha256']:
        raise ValueError('IDO executable not pinned')
    rom=a.jp_rom.read_bytes()
    if len(rom)!=33554432 or hashlib.sha1(rom).hexdigest()!=data['original_rom_sha1']:
        raise ValueError('Original expanded JP ROM hash differs')
    a.output.mkdir(parents=True,exist_ok=False)
    results=[]
    for i,r in enumerate(rows):
        name=r['name'];start=r['rom_offset'];size=r['size']
        orig=rom[start:start+size]
        if sha(orig)!=r['original_code_sha256']:raise ValueError('Original code hash '+name)
        lines=get_original_splat_lines(a.jp_splat/r['original_asm_owner'],name,start,r['vma'],size,orig)
        src=here/r['source'];neg=here/r['negative_source']
        if sha(src.read_bytes())!=r['source_sha256'] or sha(neg.read_bytes())!=r['negative_sha256']:
            raise ValueError('Modified C / negative control source '+name)
        if b'NO_NEW_COMPILER_FINDING' not in a.ledger.read_bytes():
            raise ValueError('Missing current native compiler quirks classification')
        out=a.output/str(i).zfill(2);out.mkdir()
        body,relo,sym=native_compile(a.ido,a.objcopy,a.readelf,src,out,os.environ.copy(),'positive')
        good,reason,diff,actual,expected=check_exact(body,orig,relo,lines,size)
        symok,_=check_size(sym,name,size)
        if not good or not symok or len(actual)!=r['native_relocation_count']:
            raise ValueError('FAILED_NATIVE '+name+' '+reason+' '+str(diff))
        if b'NO_NEW_COMPILER_FINDING' not in a.ledger.read_bytes():
            raise ValueError('Quirks file changed before native negative control')
        bad,brelo,bsym=native_compile(a.ido,a.objcopy,a.readelf,neg,out,os.environ.copy(),'negative')
        ngood,nreason,nfirst,_,_=check_exact(bad,orig,brelo,lines,size)
        if ngood:raise ValueError('Negative control unexpectedly matched '+name)
        results.append({'name':name,'rom_offset':start,'vma':r['vma'],'size':size,
                        'source_sha256':r['source_sha256'],'native_relocations':len(actual),
                        'original_body_exact':True,'original_elf_size_exact':True,
                        'negative_diverges':True,'negative_mismatch_class':nreason,
                        'negative_first_mismatch':nfirst,'compiler_quirk_outcome':'NO_NEW_COMPILER_FINDING'})
        print('MATCHED',i+1,'/28',name,flush=True)
    evidence={'status':'ISOLATED_EXACT','region':'japan_0','verified_functions':len(results),
              'verified_original_bytes':sum(r['size'] for r in results),
              'verified_relocations':sum(r['native_relocations'] for r in results),
              'negative_controls_failed_as_expected':sum(r['negative_diverges'] for r in results),
              'complete_rom':'NOT_RUN_BY_THIS_SCRIPT','entries':results}
    (a.output/'results.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print('JP28_REPLAY_ISOLATED_NATIVE_PASS 28 1980 124 28_NEGATIVES',flush=True)
if __name__=='__main__':main()
