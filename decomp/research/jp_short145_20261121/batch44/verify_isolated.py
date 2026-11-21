#!/usr/bin/env python3
"""Read-only isolated matching-C source proof; not the full Japanese ROM/ELF gate."""
import argparse,hashlib,json,os,re,subprocess,sys,tempfile
from pathlib import Path

FLAG=['-c','-G','0','-non_shared','-Xfullwarn','-Xcpluscomm','-Iinclude','-Ilibultra/include','-Ilibultra/include/PR','-Isrc','-I.','-Wab,-r4300_mul','-woff','649,838,712','-D_LANGUAGE_C','-D_FINALROM','-DF3DEX_GBI','-D__sgi','-DNDEBUG','-O2','-mips2']

def run(argv,cwd,env):
 p=subprocess.run([str(a) for a in argv],cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=30)
 if p.returncode:raise RuntimeError(p.stdout[-2000:])
 return p.stdout

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--upstream',type=Path,required=True,help='pinned mnsg root with Japanese Splat assembly and IDO 5.3')
 p.add_argument('--expanded-rom',type=Path,required=True,help='original decompressed Japanese 32MiB ROM; local only')
 p.add_argument('--bundle',type=Path,default=Path(__file__).resolve().parent,help='directory containing manifest.json and sources/')
 p.add_argument('--objcopy',default='mips-linux-gnu-objcopy')
 p.add_argument('--readelf',default='readelf')
 p.add_argument('--lib-dir',default='',help='directory holding binutils shared libraries')
 p.add_argument('--limit',type=int,default=0)
 args=p.parse_args()
 expected=json.loads((args.bundle/'manifest.json').read_text())
 rom=args.expanded_rom.read_bytes()
 actual_sha=hashlib.sha1(rom).hexdigest()
 if len(rom)!=33554432 or actual_sha!=expected['original_japanese_expanded_rom_sha1']:
  raise SystemExit('Original expanded ROM SHA-1/length mismatch. No tests run.')
 env=os.environ.copy()
 if args.lib_dir:env['LD_LIBRARY_PATH']=str(args.lib_dir)+(os.pathsep+env['LD_LIBRARY_PATH'] if env.get('LD_LIBRARY_PATH') else '')
 cc=args.upstream/'tools/ido-5.3/cc'; records=expected['functions']
 if args.limit:records=records[:args.limit]
 failed=[];matched=0
 with tempfile.TemporaryDirectory(prefix='goemon-japan-isolated-') as tmp:
  root=Path(tmp)
  for i,rec in enumerate(records,1):
   try:
    name=rec['name']; f=args.bundle/'sources'/(name+'.c');c=f.read_bytes()
    if hashlib.sha256(c).hexdigest()!=rec['candidate_source_sha256']:raise ValueError('candidate source SHA-256 mismatch')
    obj=root/'candidate.o';binf=root/'candidate.bin'
    run([cc,*FLAG,'-o',obj,f],args.upstream,env)
    reltext=run([args.readelf,'-rW',obj],args.upstream,env)
    run([args.objcopy,'-O','binary','-j','.text',obj,binf],args.upstream,env)
    compiled=bytearray(binf.read_bytes())
    path=args.upstream/'asm/japan_0'/rec['disassembly_file']
    original_asm=path.read_text().split('glabel '+name+'\n')[1].split('endlabel '+name)[0]
    observed=[]
    for line in reltext.splitlines():
     m=re.match(r'\s*([0-9A-Fa-f]{8})\s+\S+\s+(R_MIPS_\S+)\s+\S+\s+(\S+)',line)
     if not m:continue
     off=int(m.group(1),16);typ=m.group(2);sym=m.group(3)
     mm=re.match(r'(?:func|D)_([0-9A-Fa-f]{8})(?:_|$)',sym)
     if not mm:raise ValueError('unmapped relocation symbol '+sym)
     addr=int(mm.group(1),16)
     if sym not in original_asm:raise ValueError('symbol absent from original ASM: '+sym)
     old=int.from_bytes(compiled[off:off+4],'big')
     if typ=='R_MIPS_HI16':val=((addr+0x8000)>>16)&0xffff;mask=0xffff
     elif typ=='R_MIPS_LO16':val=addr&0xffff;mask=0xffff
     elif typ=='R_MIPS_26':val=(addr>>2)&0x3ffffff;mask=0x3ffffff
     else:raise ValueError('unsupported relocation '+typ)
     compiled[off:off+4]=((old&~mask)|val).to_bytes(4,'big')
     observed.append({'type':typ,'symbol':sym,'offset':off})
    # Compare relocation records as sets (readelf's ordering can be independently sorted)
    def canon(a):return sorted((x['type'],x['symbol'],x['offset']) for x in a)
    if canon(observed)!=canon(rec['relocations']):raise ValueError('source relocation set differs from pinned isolated proof')
    rom_off=int(rec['rom_offset'],16);size=rec['size_bytes']
    reference=rom[rom_off:rom_off+size]
    if hashlib.sha256(reference).hexdigest()!=rec['original_sha256']:raise ValueError('original function SHA256 mismatch')
    if len(compiled)<size or compiled[:size]!=reference or any(compiled[size:]):raise ValueError('compiled code does not reproduce original ROM function bytes')
    matched+=1
   except Exception as err:
    failed.append((rec['name'],str(err)))
    print('FAIL',rec['name'],str(err)[:150],flush=True)
   if i%20==0:print('Verified',i,'/',len(records),'native exact',matched,flush=True)
 print('ISOLATED_NATIVE_PROOF:',matched,'/',len(records),'exact;',len(failed),'failed. Full ROM/ELF gate NOT RUN.')
 return 0 if not failed else 1

if __name__=='__main__':sys.exit(main())
