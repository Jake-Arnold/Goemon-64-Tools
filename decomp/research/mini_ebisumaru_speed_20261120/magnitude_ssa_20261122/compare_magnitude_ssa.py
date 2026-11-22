#!/usr/bin/env python3
"""Compare original and compiled C magnitude dataflow without exporting original code.
Requires user original SHA-authenticated USA ROM, baseline ELF, and native IDO C objects.
"""
import argparse,collections,hashlib,json,struct,sys
from pathlib import Path
from original_cfg_ssa import analyze,branch_graph,reaching_definitions,SHA,ROM
try:
    from audit_scaffold import native_section,secs
except ImportError:
    raise SystemExit('Add the companion source-only audit_scaffold.py beside this script')

def reaching(binary,table_values,slot):
    size=len(binary)
    assert size>0 and size%4==0
    words=struct.unpack('>'+str(size//4)+'I',binary)
    edges,delay_slots,branches,dynamic=branch_graph(words,sorted(set(table_values)))
    assert len(dynamic)==1
    writes={};reads={}
    for i,w in enumerate(words):
      op=w>>26;base=(w>>21)&31;reg=(w>>16)&31;imm=w&0xffff
      if base==29 and imm==slot and op in (0x31,0x39):
        if op==0x39:writes[i*4]={'register':f'f{reg}'}
        else:reads[i*4]={'register':f'f{reg}'}
    defs,incoming,_=reaching_definitions(edges,writes,reads)
    flows={f'0x{x:X}':sorted('UNINITIALIZED' if v is None else f'0x{v:X}' for v in vals) for x,vals in defs.items()}
    return {'bytes':size,'stack_slot':f'0x{slot:X}','reachable_control_states':len(edges),'branch_points':len(branches),'branch_likely':sum(x['likely'] for x in branches),'dual_entry_delay_slots':[f'0x{x:X}' for x in sorted(delay_slots) if (x,None) in edges], 'writes':[{'pc':f'0x{x:X}',**detail} for x,detail in sorted(writes.items())], 'reads':[{'pc':f'0x{x:X}',**detail} for x,detail in sorted(reads.items())],'reaching_definitions':flows}

def audit(original_rom,objects):
 b=original_rom.read_bytes();assert len(b)==33554432 and hashlib.sha1(b).hexdigest()==SHA
 original=b[ROM:ROM+4320]
 orig_table=struct.unpack_from('>18I',b,0x5c676c)
 orig_table=[w-0x801CD310 for w in orig_table]
 results={'original':reaching(original,orig_table,0x8c),'candidates':[]}
 for name,path in objects.items():
   start,size=secs(path)
   code=native_section(path,'text')[start:start+size]
   table=list(struct.unpack('>18I',native_section(path,'rodata')[:72]))
   result=reaching(code,table,0xd4)
   result['name']=name
   # independently record the candidate use of the original slot
   result['original_magnitude_slot_used_by_other_data']=reaching(code,table,0x8c)['writes']
   results['candidates'].append(result)
 return results

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--rom',type=Path,required=True);p.add_argument('--f14-object',type=Path,required=True);p.add_argument('--f16-object',type=Path,required=True);p.add_argument('--output',type=Path)
 args=p.parse_args()
 output=audit(args.rom,{'F14_117':args.f14_object,'F16_8':args.f16_object})
 if args.output:args.output.write_text(json.dumps(output,indent=2)+'\n')
 print(json.dumps(output,indent=2))
