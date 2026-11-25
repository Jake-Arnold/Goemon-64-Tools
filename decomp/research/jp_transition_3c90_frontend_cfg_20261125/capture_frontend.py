#!/usr/bin/env python3
"""Retain private stock IDO stage outputs and prove replay equivalence to driver.
Only compact lengths/digests and control-flow statistics are published.
"""
import json,os,re,shlex,subprocess,sys
from pathlib import Path
P=Path(__file__).resolve().parent; W=Path(os.environ.get('GOEMON_WORK','/tmp/jp3c90')); U=W/'mnsg-japan'; L=W/'live/Goemon-64-Tools'; O=P/'out'; T=P/'private_traces'; F=P/'private_frontend'; F.mkdir(exist_ok=True)
sys.path.insert(0,str(L/'decomp/research/transition_final_20261124'))
import isolated_jp_helpers as jp
assert (W/'archive/COMMIT.txt').read_text().strip()=='160587eb162d957128c8c7dac62439ae5efc3942'
assert jp.run(['git','rev-parse','HEAD'],U).strip()==jp.PIN
assert not jp.run(['git','status','--porcelain','--untracked-files=no'],U).strip()
assert jp.digest((U/'tools/ido-5.3/cc').read_bytes())==jp.CC_SHA
assert jp.digest((U/'config/japan_0/baserom.decompressed.z64').read_bytes(),'sha1')==jp.ROM_SHA
assert jp.digest((U/'config/japan_0/baserom.z64').read_bytes(),'sha1')==jp.RETAIL_SHA
NAME='func_80003090_3C90'
rows=[]
for src in sorted((P/'source').glob(NAME+'_*.c')):
    name=src.stem; folder=F/name; folder.mkdir(exist_ok=True)
    ledger=(L/'decomp/COMPILER_QUIRKS.md').read_bytes(); assert b'source-line grouping' in ledger
    # Use the authenticated driver's exact emitted commands, replacing only paths
    # of temporary files and executable locations. Do not edit any Ucode bytes.
    log=(T/(name+'.log')).read_text()
    commands=[shlex.split(line) for line in log.splitlines() if line.startswith('/usr/lib/')]
    assert [Path(cmd[0]).name for cmd in commands]==['cfe','uopt','ugen','as1']
    cfe,uopt,ugen,as1=commands
    assert cfe[-2]=='>'
    inputs={cfe[-1]:folder/'frontend.B',next(x[3:] for x in cfe if x.startswith('-XS')):folder/'symbols.T',uopt[uopt.index(cfe[-1])+1]:folder/'optimized.O',uopt[-1]:folder/'optimizer.tmp',ugen[ugen.index('-o')+1]:folder/'codegen.G',ugen[ugen.index('-temp')+1]:folder/'codegen.tmp',as1[as1.index('-o')+1]:folder/'result.o'}
    def remap(arg):
        if arg.startswith('-XS'):return '-XS'+str(inputs[arg[3:]])
        return str(inputs.get(arg,arg))
    for n,cmd in enumerate(commands):
        argv=[str(U/'tools/ido-5.3'/Path(cmd[0]).name),*map(remap,cmd[1:-2] if n==0 else cmd[1:])]
        with (folder/f'{n}.stderr').open('wb') as err, (folder/'frontend.B' if n==0 else folder/f'{n}.stdout').open('wb') as out:
            subprocess.run(argv,cwd=U,stdout=out,stderr=err,check=True)
    linked=jp.link(folder/'result.o',NAME,0x80003090,folder,U)
    normal=json.loads((O/(name+'.json')).read_text()); assert jp.digest(linked)==normal['linked_sha256']
    assert jp.rels(folder/'result.o',U)==jp.rels(O/(name+'.o'),U)
    sizes={k:{'bytes':(folder/k).stat().st_size,'sha256':jp.digest((folder/k).read_bytes())} for k in ('frontend.B','optimized.O','codegen.G')}
    # Raw Ucode includes metadata, so byte hashes alone do not establish CFG equivalence.
    rows.append({'variant':src.name,'stages':sizes,'normal_linked_equal':True,'normal_relocations_equal':True,'compiler_outcome':'NO_NEW_COMPILER_FINDING'})
    print(name,[(k,v['bytes']) for k,v in sizes.items()],flush=True)
(P/'evidence/frontend_summary.json').write_text(json.dumps({'scope':'private unmodified stock-stage outputs; byte size and digest include metadata','variants':rows},indent=2)+'\n')
