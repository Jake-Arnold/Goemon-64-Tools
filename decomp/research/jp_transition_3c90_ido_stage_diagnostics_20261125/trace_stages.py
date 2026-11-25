#!/usr/bin/env python3
"""Trace stock IDO 5.3 without changing native linked code; raw traces private."""
import argparse, hashlib, json, os, re, subprocess, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
W=Path(os.environ.get('GOEMON_WORK','/tmp/jp3c90')).resolve()
U=W/'mnsg-japan'; L=W/'live/Goemon-64-Tools'; O=HERE/'out'; T=HERE/'private_traces'
T.mkdir(exist_ok=True)
sys.path.insert(0,str(L/'decomp/research/transition_final_20261124'))
import isolated_jp_helpers as jp
BASE='160587eb162d957128c8c7dac62439ae5efc3942'
NAME='func_80003090_3C90'
CC=U/'tools/ido-5.3/cc'
LEDGER=L/'decomp/COMPILER_QUIRKS.md'
assert (W/'archive/COMMIT.txt').read_text().strip()==BASE
assert jp.run(['git','rev-parse','HEAD'],U).strip()==jp.PIN
assert not jp.run(['git','status','--porcelain','--untracked-files=no'],U).strip()
assert jp.digest(CC.read_bytes())==jp.CC_SHA
assert jp.digest((U/'config/japan_0/baserom.decompressed.z64').read_bytes(),'sha1')==jp.ROM_SHA
assert jp.digest((U/'config/japan_0/baserom.z64').read_bytes(),'sha1')==jp.RETAIL_SHA

def inspect(name):
    src=HERE/'source'/(name+'.c'); obj=T/(name+'.o'); log=T/(name+'.log')
    ledger=LEDGER.read_text(); assert 'source-line grouping' in ledger and 'redundant' in ledger
    cmd=[str(CC),'-v','-Wc,-d',*jp.FLAGS,'-o',str(obj),str(src)]
    p=subprocess.run(cmd,cwd=U,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,check=True)
    log.write_text(p.stdout)
    normal=json.loads((O/(name+'.json')).read_text())
    linked=jp.link(obj,NAME,0x80003090,T,U)
    assert jp.digest(linked)==normal['linked_sha256'],name
    assert jp.rels(obj,U)==jp.rels(O/(name+'.o'),U),name
    build=p.stdout.split('Tree dump after Build',1)[1].split('Tree dump after Translate',1)[0]
    pointer=re.search(r'str dtype=A mtype=R[^\n]*?offset=(\d+)',build)
    assert pointer and int(pointer[1])%4==0
    emit=[line for line in p.stdout.splitlines() if line.startswith('emit_')]
    loads=[(i,tuple(map(int,re.search(r'zlbu xr(\d+)\s+241110 xr(\d+)',line).groups()))) for i,line in enumerate(emit) if re.search(r'zlbu xr(\d+)\s+241110 xr(\d+)',line)]
    assert len(loads)==3,loads
    first=loads[1][0]; end=next(i for i in range(first,len(emit)) if re.search(r'zsb xr\d+\s+241110 xr\d+',emit[i]))
    first_arm=emit[first:end+1]
    masks=[int(re.search(r'zand xr(\d+)',s)[1]) for s in first_arm if 'zand xr' in s]
    words=[int.from_bytes(linked[i:i+4],'big') for i in range(0,len(linked),4)]
    result={**normal,'trace_flags':['-v','-Wc,-d',*jp.FLAGS], 'trace_linked_sha256':jp.digest(linked),'trace_and_normal_linked_equal':True,'trace_and_normal_relocations_equal':True,'optimized_build_pointer_register':int(pointer[1])//4,'state_byte_load_registers':[{'destination':d,'base':b} for _,(d,b) in loads],'first_arm_codegen_mask_destinations':masks,'final_andi_instruction_count':sum((w>>26)==0xc for w in words),'shared_mismatch_generated_word':linked[0xc4:0xc8].hex(),'trace_sha256':jp.digest(log.read_bytes()),'compiler_outcome':'EXISTING_QUIRK_REPRODUCED' if name.endswith('first_explicit_masked') else 'NO_NEW_COMPILER_FINDING'}
    return result

def uopt_diagnostic(level):
    src=HERE/'source'/(NAME+'_baseline.c'); obj=T/f'uopt{level}.o'
    ledger=LEDGER.read_text(); assert 'source-line grouping' in ledger
    flags=[f'-Wo,-zdbug:{level}',*jp.FLAGS]
    p=subprocess.run([str(CC),*flags,'-o',str(obj),str(src)],cwd=U,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    (T/f'uopt{level}.log').write_text(p.stdout)
    listing=U/'uoptlist'
    if listing.exists(): listing.replace(T/f'uopt{level}.list')
    return {'level':level,'flags':flags,'source_sha256':jp.digest(src.read_bytes()),'exit_code':p.returncode,'wrapper_ecvt_assertion':'wrapper_ecvt' in p.stdout and 'Assertion' in p.stdout,'object_exists':obj.exists(),'compiler_outcome':'NO_NEW_COMPILER_FINDING','scope':'diagnostic attempt, not production candidate'}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--uopt-diagnostics',action='store_true');args=parser.parse_args()
    rows=[inspect(p.stem) for p in sorted((HERE/'source').glob(NAME+'_*.c'))]
    diagnostics=[uopt_diagnostic(i) for i in (4,5,6)] if args.uopt_diagnostics else []
    result={'status':'RESEARCH_ONLY','base_commit':BASE,'source_archive':14956254355,'pinned_upstream':jp.PIN,'compiler_sha256':jp.CC_SHA,'region':'japan_0','original_rom_sha1':jp.ROM_SHA,'original_retail_sha1':jp.RETAIL_SHA,'compiler_ledger_sha256':jp.digest(LEDGER.read_bytes()),'variants':rows,'uopt_diagnostics':diagnostics,'canonical_delta':0,'mixed_owner':'NOT_RUN','full_candidate_G2':'NOT_RUN','full_candidate_CI':'NOT_RUN'}
    (HERE/'evidence'/'stage_summary.json').write_text(json.dumps(result,indent=2)+'\n')
    for r in rows:print(r['variant'],r['matching_words'],r['relocations_matching'],r['optimized_build_pointer_register'],r['state_byte_load_registers'][-1],r['first_arm_codegen_mask_destinations'],r['final_andi_instruction_count'])
    print(diagnostics)
if __name__=='__main__': main()
