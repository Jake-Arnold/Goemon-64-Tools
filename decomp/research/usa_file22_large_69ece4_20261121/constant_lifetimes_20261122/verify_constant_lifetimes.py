#!/usr/bin/env python3
"""Replay original ROM against four native-IDO C candidates (source-only research).

Expected result: BOTH final C sources match all visible memory events, but fail
original machine-code identity. Negative GBI macro has 25 reversed store pairs.
Never promotes a function or changes an original ROM or local source checkout.
"""
from __future__ import annotations
import argparse,collections,hashlib,json,os,struct,subprocess,sys
from pathlib import Path
from reproduce_compiled_ido import FLAGS, PIN, FUN_SHA256, compiled_guest_text, code_stats
from trace_original_file22_mips import ROM_SHA1
from full_effects_oracle import run
from compare_function_shape import align
from analyze_stack_slots import analyze as analyze_stack

ROM_START=0x69ECE4
ROM_LENGTH=1808
SOURCES={
 'original_gbi_negative_control':'macro_store_order_negative_control.c',
 'ordered_unpadded':'ordered_gbi_unpadded_RESEARCH.c',
 'dual_named':'dual_named_constants_RESEARCH.c',
 'dual_named_and_bound':'dual_named_constants_and_bound_RESEARCH.c',
}
EXPECTED={
 'original_gbi_negative_control':(1808,144,3,3),
 'ordered_unpadded':(1792,80,3,3),
 'dual_named':(1776,80,3,3),
 'dual_named_and_bound':(1776,80,3,3),
}
EVENT_COUNTS=(113,10,4,90910,100869,33623)

def count_lui(code):
 return collections.Counter(w&0xffff for (w,) in struct.iter_unpack('>I',code) if w>>26==15)

def exact_events(a,b):
 return a['status']==b['status']=='OK' and a['loads']==b['loads'] and a['stores']==b['stores'] and a['gfx']==b['gfx']

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--full-all",action="store_true",help="Run all 113 scenarios for all three improved sources (longer)")
 for x in ('checkout','deps','runtime','output'):
  p.add_argument('--'+x,type=Path,required=True)
 a=p.parse_args();base=a.checkout.resolve();out=a.output.resolve();root=Path(__file__).parent.resolve()
 if out.exists():raise FileExistsError('Output directory already exists')
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()
 if head!=PIN:raise ValueError('Pinned upstream original checkout commit mismatch')
 rom=(base/'config/usa/baserom.decompressed.z64').read_bytes()
 if len(rom)!=33554432 or hashlib.sha1(rom).hexdigest()!=ROM_SHA1:raise ValueError('Original ROM SHA mismatch')
 original=rom[ROM_START:ROM_START+ROM_LENGTH]
 if hashlib.sha256(original).hexdigest()!=FUN_SHA256:raise ValueError('Original function SHA mismatch')
 stack=analyze_stack(rom)
 cc=base/'tools/ido-5.3/cc'
 if not cc.is_file():raise FileNotFoundError(cc)
 env=os.environ.copy()
 env['PATH']=str(a.deps.resolve()/'bin')+os.pathsep+env.get('PATH','')
 env['LD_LIBRARY_PATH']=str(a.runtime.resolve()/'lib')+os.pathsep+env.get('LD_LIBRARY_PATH','')
 out.mkdir(parents=True)
 original_modes={m:run(rom,None,m) for m in range(4)}
 report={'format':'goemon-file22-ido-ordered-gbi-constant-lifetimes-v1',
  'status':'RESEARCH_ONLY_FAILED_NATIVE','original_sha1':ROM_SHA1,
  'original_function_sha256':FUN_SHA256,'pinned_original_git_commit':PIN,
  'original_byte_count':ROM_LENGTH,'original_frame_bytes':320,
  'original_lui_count':sum(count_lui(original).values()),
  'original_direct_sp_slots':stack['direct_sp_reference_slot_count'],
  'probes':{},'no_new_accepted_C':True,'whole_ROM_G2':'NOT_RUN','full_local_CI':'NOT_RUN'}
 orig_lui=count_lui(original)
 for label,filename in SOURCES.items():
  source=root/filename;obj=out/(label+'.o')
  cmd=[str(cc),*FLAGS,'-I'+str(base/'libultra/include'),'-o',str(obj),str(source)]
  trial=subprocess.run(cmd,cwd=base,env=env,text=True,capture_output=True)
  (out/(label+'.ido.log')).write_text(trial.stdout+'\n'+trial.stderr)
  if trial.returncode:raise RuntimeError('Native IDO compiler failed: '+label)
  generated=compiled_guest_text(obj)  # Also strictly checks exactly two expected source relocs.
  stats=code_stats(original,generated)
  got=(len(generated),stats['candidate_frame_bytes'],stats['candidate_lui_F300'],stats['candidate_lui_E700'])
  if got!=EXPECTED[label]:raise AssertionError(f'Unexpected native IDO output for {label}: {got}')
  lui=count_lui(generated)
  shape=align(original,generated)
  modes=[]
  for mode in range(4):
   first=original_modes[mode];second=run(rom,generated,mode)
   row={'mode':mode,'read_order_equal':first['loads']==second['loads'],
    'store_order_equal':first['stores']==second['stores'],'gfx_equal':first['gfx']==second['gfx'],
    'store_differences':sum(x!=y for x,y in zip(first['stores'],second['stores']))}
   modes.append(row)
  if label=='original_gbi_negative_control':
   assert modes[0]['read_order_equal'] and modes[0]['gfx_equal'] and modes[0]['store_differences']==50
   assert all(all((x['read_order_equal'],x['store_order_equal'],x['gfx_equal'])) for x in modes[1:])
  else:
   if not all(all((x['read_order_equal'],x['store_order_equal'],x['gfx_equal'])) for x in modes):
    raise AssertionError('Visible memory-event regression in '+label)
  if label=='dual_named_and_bound':
   if orig_lui-lui != collections.Counter({0xFD50:1}) or lui-orig_lui:
    raise AssertionError('Expected exactly one fewer branch-local FD50 LUI and no extraneous LUI')
   if sum(lui.values())!=39 or sum(orig_lui.values())!=40:
    raise AssertionError('Original versus candidate LUI multiset drift')
   if (shape['ordered_opcode_shape_matches'],stats['matching_raw_word_positions'])!=(309,17):
    raise AssertionError('Instruction shape changed')
  row={'source_file':filename,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
   'code':stats,'ordered_opcode_shape_matches':shape['ordered_opcode_shape_matches'],
   'two_original_global_relocations_verified':True,
   'lui_total':sum(lui.values()),
   'lui_missing_relative_original':{hex(k):v for k,v in (orig_lui-lui).items()},
   'lui_excess_relative_original':{hex(k):v for k,v in (lui-orig_lui).items()},
   'modes':modes}
  if label=='dual_named_and_bound' or (a.full_all and label in ('ordered_unpadded','dual_named')):
   events_path=out/(label+'.all_events.json')
   command=[sys.executable,str(root/'full_effects_oracle.py'),
     '--usa',str(base/'config/usa/baserom.decompressed.z64'),
     '--object',str(obj),'--output',str(events_path)]
   process=subprocess.run(command,cwd=root,env=env,text=True,capture_output=True)
   (out/(label+'.events.log')).write_text(process.stdout+'\n'+process.stderr)
   if process.returncode:raise AssertionError('Full event suite FAILED: '+label+' '+process.stderr[-350:])
   s=json.loads(events_path.read_text())['summary']
   got=(s['completed_memory_cases'],s['truncated_alias_cases_excluded'],s['division_guards'],
        s['total_external_reads_each'],s['total_external_stores_each'],s['total_gfx_commands_each'])
   if got!=EVENT_COUNTS or not (s['all_completed_reads_equal'] and s['all_completed_writes_equal'] and s['all_completed_gfx_equal']):
    raise AssertionError('Full event suite counts/equality drift: '+label)
   row['full_external_event_summary']=s
  report['probes'][label]=row
  print(f'{label}: {len(generated)} B / frame {stats["candidate_frame_bytes"]:#x}, '
        f'LUI {sum(lui.values())}/40, modes {sum(x["read_order_equal"] and x["store_order_equal"] and x["gfx_equal"] for x in modes)}/4',flush=True)
 assert not any(x['code']['source_code_exact'] for x in report['probes'].values())
 (out/'sanitized_summary.json').write_text(json.dumps(report,indent=2)+'\n')
 print('PASS original ROM + IDO + negative control + best-source 113 event scenarios + 18 stack offsets. FAILED_NATIVE; no promotion.')

if __name__=='__main__':main()
