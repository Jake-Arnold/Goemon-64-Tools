#!/usr/bin/env python3
"""Fail-closed original-USA Mini clamp CFG and candidate magnitude SSA replay.
All private assets/tools supplied externally. Never changes production sources.
"""
import argparse,hashlib,json,subprocess,sys,tempfile
from pathlib import Path
from original_cfg_ssa import analyze,SHA
from compare_magnitude_ssa import audit as compare
from audit_stack_owner import analyze as audit_stack
from audit_scaffold import run as compare_mips

FLAGS=['-c','-G','0','-non_shared','-Xfullwarn','-Xcpluscomm','-Iinclude','-Ilibultra/include','-Ilibultra/include/PR','-Isrc','-I.','-Wab,-r4300_mul','-woff','649,838,712','-D_LANGUAGE_C','-D_FINALROM','-DF3DEX_GBI','-D__sgi','-DNDEBUG','-O2','-mips2']
EXPECTED={
 'clamp_f14_best_117':{'sha':'43f54bc681c1f1faaa33544a9effbba6750b9bc4acf49c29c36d2d73fbefb6d5','size':4440,'words':117,'compared':917,'relo':30},
 'clamp_f16_exact_reset':{'sha':'3f37cae5ab8d641f08d7818594c3b8a82b9767fa648b41cf66904c0509a485b3','size':4412,'words':86,'compared':906,'relo':20},
}
def sha1(path):return hashlib.sha1(path.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser(description=__doc__)
 for arg in ('upstream','rom','elf','built-rom'):p.add_argument('--'+arg,type=Path,required=True)
 p.add_argument('--json',type=Path);a=p.parse_args()
 here=Path(__file__).resolve().parent;u=a.upstream.resolve()
 subprocess.run([sys.executable,'-m','unittest','discover','-s',str(here),'-p','test_original_cfg_ssa.py','-q'],check=True,cwd=here)
 assert subprocess.check_output(['git','-C',str(u),'rev-parse','HEAD'],text=True).strip()=='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
 orig=a.rom.resolve();built=a.built_rom.resolve();assert orig.stat().st_size==33554432
 assert built.stat().st_size==33554432 and sha1(orig)==sha1(built)==SHA
 assert orig.read_bytes()==built.read_bytes()
 print('CLEAN_ORIGINAL_ROM_BYTE_EXACT_33554432',SHA,flush=True)
 original_result=analyze(orig.read_bytes())
 assert original_result['magnitude_source_witnesses']['0x218']['passes_sqrt_overwrite'] is False
 assert original_result['magnitude_source_witnesses']['0x4E4']['passes_sqrt_overwrite'] is True
 assert original_result['sp8c_definitions_at_reads']=={'0xfe8':['0x218','0x4E4'],'0x1000':['0xFFC']}
 assert original_result['dual_entry_delay_slot_pcs']==['0x610','0x8a4']
 with tempfile.TemporaryDirectory(prefix='goemon_magnitude_ssa_') as w:
  d=Path(w);objs={};native_results=[]
  for name,expect in EXPECTED.items():
   src=here/(name+'.c');assert hashlib.sha256(src.read_bytes()).hexdigest()==expect['sha']
   obj=d/(name+'.o');cc=u/'tools/ido-5.3/cc'
   p=subprocess.run([str(cc),*FLAGS,'-o',str(obj),str(src)],cwd=u,capture_output=True,text=True)
   if p.returncode:raise RuntimeError(name+': '+p.stderr[-1200:])
   m=compare_mips(orig,a.elf,obj,src)
   assert (m['candidate_bytes'],m['frame_bytes'],m['words_matching'],m['words_comparable'],m['relocation_offset_type_symbol_identical'])==(expect['size'],232,expect['words'],expect['compared'],expect['relo'])
   assert m['status']=='FAILED_NATIVE' and m['calls_candidate']==33 and m['sqrt_candidate']==9 and m['candidate_relocations']==101
   print('NATIVE_REPLAY_EXPECTED_FAILED',name,expect,flush=True)
   native_results.append({'candidate':name,'bytes':m['candidate_bytes'],'matching_instructions':m['words_matching'],'comparables':m['words_comparable'],'exact_relocations':m['relocation_offset_type_symbol_identical'],'status':'FAILED_NATIVE'})
   objs['F14_117' if name.endswith('117') else 'F16_8']=obj
  flow=compare(orig,objs)
  assert flow['original']['reaching_definitions']=={'0xFE8':['0x218','0x4E4'],'0x1000':['0xFFC']}
  by={x['name']:x for x in flow['candidates']}
  assert by['F14_117']['reaching_definitions']=={'0x1060':['0x1C4','0x4E4']}
  assert by['F16_8']['reaching_definitions']=={'0x1044':['0x220','0x500']}
  assert by['F14_117']['writes']==[{'pc':'0x1C4','register':'f14'},{'pc':'0x4E4','register':'f0'},{'pc':'0x1078','register':'f4'}]
  assert by['F16_8']['writes']==[{'pc':'0x220','register':'f16'},{'pc':'0x500','register':'f0'},{'pc':'0x105C','register':'f6'}]
  assert len(by['F14_117']['original_magnitude_slot_used_by_other_data'])==5
  assert len(by['F16_8']['original_magnitude_slot_used_by_other_data'])==2
  assert all(c['bytes']!=4320 for c in native_results)
  occupancy=audit_stack(orig,objs)
  assert occupancy['original']['0x8C']['writes']==['0x218','0x4E4','0xFFC']
  assert occupancy['original']['0x8C']['reads']==['0xFE8','0x1000']
  assert all(occupancy['candidates'][name]['fp_stack_accesses']['0xA4']['total']==0 for name in objs)
  assert all(occupancy['candidates'][name]['fp_stack_accesses']['0xB0']['total']==0 for name in objs)
  assert all(occupancy['candidates'][name]['fp_stack_accesses']['0xD4']['writes'] for name in objs)
  output={'status':'PASS_EXPECTED_FAILED_NATIVE','original_control_flow':original_result,'native_candidates':native_results,'original_to_candidate_magnitude':flow,'stack_ownership':occupancy,'production_promotion':'NOT_PERMITTED','candidate_integrated_ROM':'NOT_RUN','combined_decomp_verify':'NOT_RUN','strict_inventory':'NOT_RUN','full_local_ci':'NOT_RUN','gameplay':'NOT_RUN'}
 if a.json:a.json.write_text(json.dumps(output,indent=2)+'\n')
 print('COMPLETE_SSA_REPLAY_PASS_EXPECTED_NONMATCH; PRODUCTION_UNCHANGED',flush=True)
if __name__=='__main__':main()
