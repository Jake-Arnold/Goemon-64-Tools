#!/usr/bin/env python3
"""ROM-authenticated, read-only FP stack-slot access map; never export opcodes."""
import argparse,hashlib,json,struct
from pathlib import Path
from audit_scaffold import native_section,secs
from original_cfg_ssa import SHA,ROM

WATCH=(0x8C,0xA4,0xA8,0xAC,0xB0,0xB4,0xB8,0xD4)

def fp_uses(code):
 assert len(code)%4==0
 d={f'0x{off:X}':[] for off in WATCH}
 for pc in range(0,len(code),4):
  w=struct.unpack_from('>I',code,pc)[0]
  op=w>>26;base=(w>>21)&31;reg=(w>>16)&31;off=w&0xffff
  if base==29 and op in (0x31,0x39) and off in WATCH:
   d[f'0x{off:X}'].append({'pc':f'0x{pc:X}','operation':'swc1' if op==0x39 else 'lwc1','reg':f'f{reg}'})
 return {name:{'total':len(a),'first':a[0]['pc'] if a else None,'last':a[-1]['pc'] if a else None,'writes':[z['pc'] for z in a if z['operation']=='swc1'],'reads':[z['pc'] for z in a if z['operation']=='lwc1']} for name,a in d.items()}

def analyze(rom,objects):
 data=Path(rom).read_bytes()
 assert len(data)==33554432 and hashlib.sha1(data).hexdigest()==SHA
 orig=fp_uses(data[ROM:ROM+4320])
 assert orig['0x8C']['writes']==['0x218','0x4E4','0xFFC']
 assert orig['0x8C']['reads']==['0xFE8','0x1000']
 out={'status':'PASS','original_usa_sha1':SHA,'original':orig,'candidates':{}}
 for label,p in objects.items():
  start,size=secs(p)
  code=native_section(p,'text')[start:start+size]
  out['candidates'][label]={'code_bytes':size,'fp_stack_accesses':fp_uses(code)}
 return out
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--f14-object',required=True);p.add_argument('--f16-object',required=True);p.add_argument('--output');args=p.parse_args()
 out=analyze(args.rom,{'F14_117':args.f14_object,'F16_8':args.f16_object})
 if args.output:Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
 print('FP_STACK_OWNERSHIP_AUDIT_PASS',json.dumps({name:{k:v['total'] for k,v in cand['fp_stack_accesses'].items()} for name,cand in out['candidates'].items()}))
