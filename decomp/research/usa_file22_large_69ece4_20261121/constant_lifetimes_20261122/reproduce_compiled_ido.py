#!/usr/bin/env python3
"""Source-only original-USA file22 native IDO vs actual original-MIPS comparator.

Read-only to ROM/checkouts. Authenticates pinned original USA 32MiB ROM and
original 1808-byte slice, builds C with original IDO, resolves exactly the two
symbol relocations in scratch memory, then compares full 64-bit graphics streams.
No game process, patch, original ASM/ROM dump, copyrighted texture output,
or local build object is included in this source archive or committed to Git.
"""
from __future__ import annotations
import argparse, collections, hashlib, json, os, re, struct, subprocess
from pathlib import Path
import trace_original_file22_mips as trace

PIN='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
FUN_SHA256='eaccca6679247d56785806a92a2efe4c1adb73368f723b76d4b6aab5040ef3a9'
FUNC_ROM=0x69ECE4
FUNC_LEN=1808
FLAGS=['-c','-G','0','-non_shared','-Xfullwarn','-Xcpluscomm',
       '-Wab,-r4300_mul','-woff','649,838,712',
       '-D_LANGUAGE_C','-D_FINALROM','-DF3DEX_GBI','-D__sgi',
       '-DNDEBUG','-O2','-mips2']
SOURCES={
 'original_m2c_before_pointer_fix':'prior_nonmatching_double_scaled.c',
 'corrected_semantic_source':'usa_file22_1808_corrected_semantic.c',
 'corrected_plus_DIAGNOSTIC_stack_padding':'usa_file22_1808_stack_layout_diagnostic.c',
 'corrected_DIAGNOSTIC_exact_eight_stack_slots':'usa_file22_1808_all_eight_stack_slots_DIAGNOSTIC.c',
}

def text_from_elf32_be(path:Path)->bytes:
 b=path.read_bytes()
 if b[:6]!=b'\x7fELF\x01\x02':raise ValueError('Expected IDO ELF32 big-endian object')
 shoff=struct.unpack_from('>I',b,0x20)[0]
 ent=struct.unpack_from('>H',b,0x2e)[0]
 num=struct.unpack_from('>H',b,0x30)[0]
 strs=struct.unpack_from('>H',b,0x32)[0]
 if ent<40 or strs>=num or shoff+ent*num>len(b):raise ValueError('Invalid ELF section table')
 strbase=struct.unpack_from('>I',b,shoff+strs*ent+16)[0]
 for i in range(num):
  hdr=shoff+i*ent
  no=struct.unpack_from('>I',b,hdr)[0]
  if strbase+no>=len(b):raise ValueError('Invalid ELF section name')
  name=b[strbase+no:b.index(0,strbase+no)]
  if name==b'.text':
   off,n=struct.unpack_from('>II',b,hdr+16)
   if off+n>len(b):raise ValueError('Invalid ELF .text extent')
   return b[off:off+n]
 raise ValueError('Missing .text')

def compiled_guest_text(obj:Path)->bytes:
 data=bytearray(text_from_elf32_be(obj))
 # Parse and require the ORIGINAL source symbol's exact two MIPS relocs.
 raw=subprocess.check_output(['readelf','-rW',str(obj)],text=True)
 relocations=re.findall(r'(?m)^([0-9a-fA-F]{8})\s+[0-9a-fA-F]{8}\s+(R_MIPS_[A-Z0-9]+)\s+[0-9a-fA-F]{8}\s+(\S+)\s*$',raw)
 pairs=[(int(off,16),kind,name) for off,kind,name in relocations]
 if len(pairs)!=2 or [k for o,k,n in pairs]!=['R_MIPS_HI16','R_MIPS_LO16'] or any(n!='D_801D701C_6A9C3C' for o,k,n in pairs):
  raise ValueError(f'Unexpected candidate relocation list: {pairs}')
 for off,kind,name in pairs:
  if off<0 or off+4>len(data) or off%4:raise ValueError('Invalid object relocation offset')
  word=int.from_bytes(data[off:off+4],'big')
  if word&65535:raise ValueError('Source relocation carries unknown preexisting addend')
  hi=((trace.CURSOR+32768)>>16)&65535
  lo=trace.CURSOR&65535
  value=hi if kind=='R_MIPS_HI16' else lo
  data[off:off+4]=((word&0xffff0000)|value).to_bytes(4,'big')
 return bytes(data)

def code_stats(reference:bytes,compiled:bytes)->dict:
 n=min(len(reference),len(compiled))//4
 prefix=0
 while prefix<n and reference[4*prefix:4*prefix+4]==compiled[4*prefix:4*prefix+4]:prefix+=1
 matched=sum(reference[i*4:i*4+4]==compiled[i*4:i*4+4] for i in range(n))
 frame=-struct.unpack('>h',compiled[2:4])[0]
 def luis(data):
  return collections.Counter((int.from_bytes(data[i:i+4],'big')&65535) for i in range(0,len(data),4)
   if int.from_bytes(data[i:i+4],'big')>>26==15)
 a,b=luis(reference),luis(compiled)
 return {'original_length':len(reference),'candidate_text_length':len(compiled),
  'candidate_frame_bytes':frame,'original_frame_bytes':320,
  'matching_consecutive_entry_words':prefix,'matching_raw_word_positions':matched,
  'raw_word_positions_compared':n,'first_raw_mismatch_rom':hex(FUNC_ROM+prefix*4) if prefix<n else None,
  'source_code_exact':len(reference)==len(compiled) and reference==compiled,
  'original_lui_F300':a[0xF300],'candidate_lui_F300':b[0xF300],
  'original_lui_E700':a[0xE700],'candidate_lui_E700':b[0xE700]}

def cases():
 layouts=[('four_pages_160x128',(2,2,160,128,[0,1,2,3])),
          ('twenty_pages_64x64',(5,4,64,64,[i%4 for i in range(20)]))]
 for mode in (0,1,2,3):
  yield mode,'original',None,None
  yield mode,'reordered',[0,4,0,3,2,1,4,0],None
  yield mode,'uniform',[0]*8,None
  for name,layout in layouts:yield mode,name,None,layout

def run_candidate(rom,source_text:bytes,scenarios):
 data=source_text
 outcomes=[]
 for mode,label,rows,layout,orig in scenarios:
  ram=trace.prepare(rom,mode,rows,layout)
  buf,idx=ram.block(trace.ENTRY,len(data))
  buf[idx:idx+len(data)]=data
  machine=trace.OriginalMIPS(ram)
  try:machine.run()
  except Exception as exc:
   outcomes.append({'format':mode,'scenario':label,'pass':False,'error_type':type(exc).__name__,
    'compiled_guest_instruction_count_before_error':machine.executed});continue
  final=ram.load(trace.CURSOR)
  if not trace.OUTPUT<=final<=trace.OUTPUT+65536 or (final-trace.OUTPUT)%8:
   outcomes.append({'format':mode,'scenario':label,'pass':False,'invalid_cursor':hex(final)});continue
  got=[(ram.load(trace.OUTPUT+8*i),ram.load(trace.OUTPUT+8*i+4)) for i in range((final-trace.OUTPUT)//8)]
  mismatch=[i for i in range(max(len(orig),len(got))) if i>=len(orig) or i>=len(got) or orig[i]!=got[i]]
  outcomes.append({'format':mode,'scenario':label,'pass':not mismatch,'original_commands':len(orig),
                   'compiled_commands':len(got),'mismatching_64_bit_commands':len(mismatch),
                   'first_mismatch_index':mismatch[0] if mismatch else None,
                   'compiled_guest_instruction_count':machine.executed})
 return outcomes

def test_guards(rom,data):
 result=[]
 for label,offset in [('width_zero',0x20),('height_zero',0x22),('columns_zero',0x1C),('rows_zero',0x1E)]:
  arr=[]
  for compiled in (False,True):
   ram=trace.prepare(rom,2)
   ram.store(trace.SAVED_DESC+offset,0,2)
   if compiled:
    block,i=ram.block(trace.ENTRY,len(data));block[i:i+len(data)]=data
   cpu=trace.OriginalMIPS(ram)
   try:cpu.run();answer={'trapped':False}
   except ArithmeticError as exc:answer={'trapped':True,'break_guest_pc':hex(cpu.pc)}
   arr.append(answer)
  result.append({'scenario':label,'original':arr[0],'compiled':arr[1],
                 'both_trap':arr[0]['trapped'] and arr[1]['trapped']})
 return result

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--checkout',type=Path,required=True)
 p.add_argument('--deps',type=Path,required=True)
 p.add_argument('--runtime',type=Path,required=True)
 p.add_argument('--output',type=Path,required=True)
 a=p.parse_args()
 base=a.checkout.resolve();out=a.output.resolve()
 if out.exists():raise SystemExit('Refusing to overwrite an output directory')
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()
 if head!=PIN:raise ValueError('Not the pinned clean original upstream checkout')
 rom=(base/'config/usa/baserom.decompressed.z64').read_bytes()
 if len(rom)!=33554432 or hashlib.sha1(rom).hexdigest()!=trace.ROM_SHA1:
  raise ValueError('Wrong original 32MiB USA ROM')
 reference=rom[FUNC_ROM:FUNC_ROM+FUNC_LEN]
 if hashlib.sha256(reference).hexdigest()!=FUN_SHA256:raise ValueError('Wrong original file22 function bytes')
 cc=base/'tools/ido-5.3/cc'
 if not cc.is_file():raise ValueError('Original IDO compiler not found')
 env=os.environ.copy()
 env['PATH']=str(a.deps.resolve()/'bin')+os.pathsep+env.get('PATH','')
 env['LD_LIBRARY_PATH']=str(a.runtime.resolve()/'lib')+os.pathsep+env.get('LD_LIBRARY_PATH','')
 out.mkdir(parents=True)
 # Precompute original MIPS independently from every candidate. Do not publish code/data.
 scenarios=[]
 for mode,label,rows,layout in cases():
  _,gfx=trace.run_once(rom,mode,rows,layout)
  scenarios.append((mode,label,rows,layout,gfx))
 report={'status':'RESEARCH_ONLY_FAILED_NATIVE','function':'func_801CC0C4_69ECE4',
   'original_usa_rom_sha1':trace.ROM_SHA1,'original_function_sha256':FUN_SHA256,
   'ido_pinned_commit':PIN,'cases':len(scenarios),'probes':{}}
 for label,filename in SOURCES.items():
  source=Path(__file__).resolve().parent/filename
  obj=out/(label+'.o')
  process=subprocess.run([str(cc),*FLAGS,'-o',str(obj),str(source)],cwd=base,
                         env=env,capture_output=True,text=True)
  (out/(label+'.compiler.log')).write_text(process.stdout+'\n'+process.stderr)
  if process.returncode:raise RuntimeError(f'Native IDO compile failure for {label}')
  data=compiled_guest_text(obj)
  stats=code_stats(reference,data)
  outcomes=run_candidate(rom,data,scenarios)
  guards=test_guards(rom,data)
  report['probes'][label]={
   'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
   'native_compiler':'original IDO 5.3, -O2 -mips2, source toolchain flags',
   'code':stats,'graphics_cases_pass':sum(x['pass'] for x in outcomes),
   'graphics_cases_total':len(outcomes),
   'total_original_graphics_records':sum(x['original_commands'] for x in outcomes if 'original_commands' in x),
   'mismatching_command_records':sum(x['mismatching_64_bit_commands'] for x in outcomes if 'mismatching_64_bit_commands' in x),
   'cases':outcomes,'division_guards':guards,
   'diagnostic_extra_stack_storage':('DIAGNOSTIC' in label)}
  print(f"{label}: native={stats['candidate_text_length']}/{stats['original_length']} bytes "
        f"frame={stats['candidate_frame_bytes']} entry_prefix={stats['matching_consecutive_entry_words']} "
        f"gfx={report['probes'][label]['graphics_cases_pass']}/{len(outcomes)} "
        f"gfx_mismatches={report['probes'][label]['mismatching_command_records']}")
 corrected=report['probes']['corrected_semantic_source']
 diagnostic=report['probes']['corrected_plus_DIAGNOSTIC_stack_padding']
 exact_slots=report['probes']['corrected_DIAGNOSTIC_exact_eight_stack_slots']
 prior=report['probes']['original_m2c_before_pointer_fix']
 report['all_corrected_checks_pass']=(corrected['graphics_cases_pass']==20 and
         corrected['mismatching_command_records']==0 and diagnostic['graphics_cases_pass']==20 and
         diagnostic['mismatching_command_records']==0 and
         exact_slots['graphics_cases_pass']==20 and exact_slots['mismatching_command_records']==0 and
         all(x['both_trap'] for x in corrected['division_guards']) and
         all(x['both_trap'] for x in diagnostic['division_guards']) and
         all(x['both_trap'] for x in exact_slots['division_guards']))
 report['negative_control_detects_prior_bug']=(prior['graphics_cases_pass']<20)
 report['candidate_is_exact_native']=corrected['code']['source_code_exact']
 report['full_G2']='NOT_RUN';report['canonical_count_delta']=0
 (out/'native_compiled_mips_comparison.json').write_text(json.dumps(report,indent=2)+'\n')
 if not report['all_corrected_checks_pass'] or not report['negative_control_detects_prior_bug']:
  raise AssertionError('Original-MIPS vs compiled-MIPS regression gate failed')
 if report['candidate_is_exact_native']:
  print('Native bytes unexpectedly exact: full formal G2 would still be required')
 else:print('PASS semantic regression; FAILED_NATIVE machine-code match. NO PROMOTION.')

if __name__=='__main__':main()
