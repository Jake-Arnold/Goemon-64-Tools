"""Research-only MIPS32 VM text-loop differential regression.

Original instructions come only from a user-supplied locally verified ROM.
This MIPS subset interpreter and synthetic callbacks are not an in-game test,
original-address linked code match, nor complete-ROM verifier.
"""
from __future__ import annotations
import argparse
import ctypes as ct
import hashlib
import os
import random
import struct
import subprocess
import tempfile
from pathlib import Path

BASE = 0x8003DBEC
ROM_OFFSET = 0x3E7EC
FUNCTION_SIZE = 0x1D8
ROM_SHA1 = "6ea0ed71032ce08fc2745f412d84936382197494"
ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_SOURCE = ROOT / 'decomp/candidates/vm_text_loop.c'
STUB_SOURCE = ROOT / 'decomp/test_vm_text_loop_differential_stubs.c'
words = {}
lib = work = controller = None

S32=lambda x:((x+2**31)%2**32)-2**31
U32=lambda x:x&0xffffffff
sx16=lambda x:S32((x&0xffff)|(-0x10000 if x&0x8000 else 0))

class Machine:
 def __init__(self,p):
  self.mem={};self.r=[0]*32;self.pc=BASE;self.count=0
  self.steps=self.handled=self.resets=0
  self.r[29]=0x7fffffc0;self.r[31]=0x88888888
  initial={0x801c77d8:p['count'],0x801c7754:0x1234,0x801c77e0:p['state'],
  0x801c7770:p['input_gate'],0x801c7774:p['handler_arg'],0x80077858:-1,
  0x801c77e8:0x4000}
  for addr,v in initial.items():self.w32(addr,v)
  self.w16(0x801c77f2,p['gate_halfword']); self.w16(0x801c790a,p['held']); self.w16(0x801c790c,p['pressed'])
  # The cursor value is 0x4000. Its pointee +0xA is deliberately distinct
  # from the global VM-work halfword at 0x801C77E8 + 0xA.
  self.w16(0x400a,p['script_pointee_gate_halfword'])
 def b(self,addr):return self.mem.get(U32(addr),0)
 def w8(self,addr,val):self.mem[U32(addr)]=val&0xff
 def u16(self,addr):return (self.b(addr)<<8)|self.b(addr+1)
 def u32(self,addr):return (self.u16(addr)<<16)|self.u16(addr+2)
 def w16(self,addr,val):self.w8(addr,val>>8);self.w8(addr+1,val)
 def w32(self,addr,val):self.w16(addr,val>>16);self.w16(addr+2,val)
 def call(self,target):
  if target==0x8003de80:
   assert self.r[4]==0x1234
   self.steps+=1
   if self.p['state_on_step']>=0:self.w32(0x801c77e0,self.p['state_on_step'])
   if self.p['bound_on_step']>=0:self.w32(0x801c77d8,self.p['bound_on_step'])
   self.r[2]=0 if self.p['return_null'] else U32(self.r[5]+4)
  elif target==0x8003de48:
   self.handled+=1;self.r[2]=U32(self.r[4]+123)
  elif target==0x8003e680:self.resets+=1
  else:raise AssertionError(f'unknown call target {target:x}')
 def insn(self,pc):
  w=words.get(pc)
  if w is None:raise AssertionError(f'unknown PC {pc:x}')
  o=w>>26; rs=(w>>21)&31; rt=(w>>16)&31;rd=(w>>11)&31;imm=sx16(w);r=self.r
  jump=None; likely=False; taken=False; call=False;ret=False
  if w==0:pass
  elif o==0:
   f=w&63
   if f==0x25:r[rd]=U32(r[rs]|r[rt])
   elif f==0x21:r[rd]=U32(r[rs]+r[rt])
   elif f==0x2a:r[rd]=int(S32(r[rs])<S32(r[rt]))
   elif f==0x08:jump=r[rs];taken=True;ret=True
   else:raise AssertionError(f'rtype {pc:x} {w:x}')
  elif o==0x0f:r[rt]=U32((w&0xffff)<<16)
  elif o==0x09:r[rt]=U32(r[rs]+imm)
  elif o==0x0a:r[rt]=int(S32(r[rs])<imm)
  elif o==0x0c:r[rt]=r[rs]&(w&0xffff)
  elif o==0x23:r[rt]=self.u32(U32(r[rs]+imm))
  elif o==0x2b:self.w32(U32(r[rs]+imm),r[rt])
  elif o==0x25:r[rt]=self.u16(U32(r[rs]+imm))
  elif o==0x29:self.w16(U32(r[rs]+imm),r[rt])
  elif o in (0x04,0x05,0x14,0x15,0x06):
   likely=o in (0x14,0x15)
   if o in (0x04,0x14):taken=r[rs]==r[rt]
   elif o in (0x05,0x15):taken=r[rs]!=r[rt]
   elif o==0x06:taken=S32(r[rs])<=0
   jump=U32(pc+4+imm*4)
  elif o==0x03:
   taken=True;call=True;jump=0x80000000|((w&0x3ffffff)<<2)
   r[31]=U32(pc+8)
  else:raise AssertionError(f'unhandled opcode {pc:x} {w:08x}')
  r[0]=0
  if jump is None:return pc+4
  if taken or not likely:
   ds=words.get(pc+4)
   assert ds is not None, f'delay slot missing {pc:x}'
   # Real function delay slots only contain plain nonbranch instructions.
   dsop=ds>>26
   assert dsop not in (0x02,0x03,0x04,0x05,0x14,0x15,0x06),f'branch in DS {pc:x}'
   self.insn(pc+4)
  if call:
   self.call(jump)
   return pc+8
  if ret:
   if jump==0x88888888:return None
   return jump
  return jump if taken else pc+8
 def run(self,p):
  self.p=p
  for i in range(3000):
   nxt=self.insn(self.pc)
   self.count+=1
   if nxt is None:break
   self.pc=nxt
  else:raise AssertionError('run exceeded instruction budget')
  return dict(script=self.u32(0x801c77e8),state=S32(self.u32(0x801c77e0)),bound=S32(self.u32(0x801c77d8)),gate=self.u16(0x801c77f2),script_pointee_gate=self.u16(0x400a),result=S32(self.u32(0x80077858)),steps=self.steps,handled=self.handled,resets=self.resets)

class Vm(ct.Structure):
 _fields_=[('script_word',ct.c_int32),('unk4',ct.c_uint16),('unk6',ct.c_uint16),('marker',ct.c_int16),('gate_halfword',ct.c_uint16),('choice_state',ct.c_int32),('countdown',ct.c_int32)]
class Controller(ct.Structure):
 _fields_=[('status',ct.c_uint16),('held',ct.c_uint16),('pressed',ct.c_uint16)]
# ctypes objects are initialized after checking the caller-supplied ROM.
def i(name):return ct.c_int32.in_dll(lib,name)
def bind_library(path):
 global lib, work, controller
 lib=ct.CDLL(str(path.resolve()))
 work=Vm.in_dll(lib,'D_801C77E8_1C83E8')
 controller=Controller.in_dll(lib,'D_801C7908_1C8508')

def host(p):
 work.script_word=0x4000;work.unk4=work.unk6=work.marker=work.choice_state=work.countdown=0
 work.gate_halfword=p['gate_halfword'];controller.status=0;controller.held=p['held'];controller.pressed=p['pressed']
 ct.c_uint16.in_dll(lib,'script_pointee_gate_halfword').value=p['script_pointee_gate_halfword']
 for name,v in [('D_801C77D8_1C83D8',p['count']),('D_801C7754_1C8354',0x1234),('D_801C77E0_1C83E0',p['state']),('D_801C7770_1C8370',p['input_gate']),('D_801C7774_1C8374',p['handler_arg']),('D_80077858_78458',-1),('state_on_step',p['state_on_step']),('bound_on_step',p['bound_on_step']),('return_null',p['return_null']),('steps',0),('handled',0),('resets',0)]:i(name).value=v
 lib.func_8003DBEC_3E7EC()
 return dict(script=U32(work.script_word),state=i('D_801C77E0_1C83E0').value,bound=i('D_801C77D8_1C83D8').value,gate=work.gate_halfword,script_pointee_gate=ct.c_uint16.in_dll(lib,'script_pointee_gate_halfword').value,result=i('D_80077858_78458').value,steps=i('steps').value,handled=i('handled').value,resets=i('resets').value)

def scenario(r):
 return {'count':r.choice([-1,0,1,2,3,4,5]),'state':r.choice([0,1,2,3,4,5,6,7]),
 'input_gate':r.choice([0,0,1]),'handler_arg':r.choice([0,7,123]),
 'held':r.choice([0,0x8000,0x4000,0xc000,1]),'pressed':r.choice([0,0x8000,0x4000,0xc000,0x1]),
 'script_pointee_gate_halfword':r.choice([0,1,0x8000,0x5a5a,0xa55a]),
 'gate_halfword':r.choice([0,1,7,65535]),'state_on_step':r.choice([-1,-1,-1,0,1,3,5,6]),
 'bound_on_step':r.choice([-1,-1,0,1,2,5]),'return_null':r.choice([0,0,0,1])}

def fixed_scenarios():
 """Named edge cases grounded in the original ROM's control-flow trace."""
 base={'count':3,'state':1,'input_gate':1,'handler_arg':7,'held':0,
       'pressed':0,'gate_halfword':0,'script_pointee_gate_halfword':0x5a5a,
       'state_on_step':-1,'bound_on_step':-1,'return_null':0}
 def case(name, **updates):
  return name, {**base, **updates}
 return [
  case('nonpositive-bound', count=0),
  case('held-0x8000-retries-with-latch', count=5, input_gate=0,
       gate_halfword=1, held=0x8000),
  case('pressed-0x8000-sets-latch', count=1, input_gate=0, pressed=0x8000),
  case('pressed-0x4000-restart-resets-state', input_gate=0, pressed=0x4000),
  case('pressed-0x4000-zero-handler-returns', input_gate=0, handler_arg=0,
       pressed=0x4000),
  case('callback-lowers-bound', count=5, bound_on_step=1),
  case('callback-raises-bound', count=1, bound_on_step=3),
  case('callback-null-return-clears-state', return_null=1),
  case('callback-terminal-state-clears-work-latch', input_gate=0,
       gate_halfword=0x1234, state_on_step=4),
  case('cursor-pointee-plus-a-is-independent', input_gate=0, gate_halfword=0,
       script_pointee_gate_halfword=1),
 ]

# Expected original-MIPS interpreter traces for the named fixed cases. Fields
# are returned cursor, VM state, loop bound, work latch, independent script
# pointee halfword, DE80 calls, DE48 calls and E680 calls. Callbacks are
# synthetic hooks; these are harness contracts, not live-game observations.
TRACE_FIELDS = ('result', 'state', 'bound', 'gate', 'script_pointee_gate',
                'steps', 'handled', 'resets')
EXPECTED_FIXED_TRACES = {
 'nonpositive-bound': (-1, 1, 0, 0, 23130, 0, 0, 0),
 'held-0x8000-retries-with-latch': (-1, 1, 5, 1, 23130, 4, 0, 0),
 'pressed-0x8000-sets-latch': (-1, 1, 1, 0, 23130, 2, 0, 0),
 'pressed-0x4000-restart-resets-state': (130, 0, 3, 0, 23130, 3, 3, 0),
 'pressed-0x4000-zero-handler-returns': (-1, 1, 3, 0, 23130, 1, 0, 1),
 'callback-lowers-bound': (-1, 1, 1, 0, 23130, 1, 0, 0),
 'callback-raises-bound': (-1, 1, 3, 0, 23130, 3, 0, 0),
 'callback-null-return-clears-state': (-1, 0, 3, 0, 23130, 1, 0, 0),
 'callback-terminal-state-clears-work-latch': (-1, 4, 3, 0, 23130, 1, 0, 0),
 'cursor-pointee-plus-a-is-independent': (-1, 1, 3, 0, 1, 3, 0, 0),
}

def replace_once(source, old, new, label):
 if source.count(old)!=1:
  raise ValueError(f'{label}: expected one source anchor, found {source.count(old)}')
 return source.replace(old,new,1)

def mutant_sources(source):
 """Return focused, intentionally incorrect local variants for negative controls."""
 variants=[]
 variants.append(('signed-held-high-bit', replace_once(
  source, 'if (D_801C7908_1C8508.held & 0x8000) {',
  'if ((short)D_801C7908_1C8508.held > 0x7fff) {', 'held signedness'),
  'held-0x8000-retries-with-latch'))
 variants.append(('signed-pressed-high-bit', replace_once(
  source, 'if (D_801C7908_1C8508.pressed & 0x8000) {',
  'if ((short)D_801C7908_1C8508.pressed > 0x7fff) {', 'pressed signedness'),
  'pressed-0x8000-sets-latch'))
 stale=replace_once(source, 'if (D_801C77D8_1C83D8 <= 0) return;',
                    's32 cached_bound = D_801C77D8_1C83D8;\n    if (cached_bound <= 0) return;',
                    'initial bound')
 stale=replace_once(stale, 'outer_count >= D_801C77D8_1C83D8',
                    'outer_count >= cached_bound', 'loop bound reload')
 variants.append(('stale-outer-bound', stale, 'callback-lowers-bound'))
 alias=replace_once(source, 'typedef unsigned short u16;',
                     'typedef unsigned short u16;\nextern u16 script_pointee_gate_halfword;',
                     'alias mutant declaration')
 alias=alias.replace('D_801C77E8_1C83E8.gate_halfword','script_pointee_gate_halfword')
 if alias==source or 'D_801C77E8_1C83E8.gate_halfword' in alias:
  raise ValueError('script-pointee alias mutant did not replace the work latch')
 variants.append(('cursor-pointee-alias', alias, 'cursor-pointee-plus-a-is-independent'))
 return variants

def check_mutants(compiler):
 scenarios=dict(fixed_scenarios())
 source=CANDIDATE_SOURCE.read_text()
 with tempfile.TemporaryDirectory(prefix='vm-text-loop-mutants-') as tmp:
  tmpdir=Path(tmp)
  for name, mutant, target in mutant_sources(source):
   src=tmpdir/f'{name}.c'; so=tmpdir/f'lib{name}.so'
   src.write_text(mutant)
   subprocess.run([compiler,'-std=c99','-shared','-fPIC','-O2',str(src),
                   str(STUB_SOURCE),'-o',str(so)],check=True)
   bind_library(so)
   params=scenarios[target]
   actual=Machine(params).run(params)
   candidate=host(params)
   if actual==candidate:
    raise AssertionError(f'mutant survived targeted case {target}: {name}')
   print(f'mutant killed: {name} by {target}')

def main():
 global words, lib, work, controller
 parser = argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--decompressed-rom', type=Path, required=True,
                     help='local 32MiB pinned USA decompressed ROM (never transmitted)')
 parser.add_argument('--host-library', type=Path, required=True,
                     help='locally built native C candidate plus synthetic hook library')
 parser.add_argument('--cases', type=int, default=10000)
 parser.add_argument('--seed', type=lambda x:int(x,0), default=0x1D8)
 parser.add_argument('--check-mutants', action='store_true',
                     help='compile temporary signedness, stale-bound and alias mutants and require each to fail')
 parser.add_argument('--c-compiler', default=os.environ.get('CC','cc'),
                     help='host C compiler used only with --check-mutants (default: CC or cc)')
 args=parser.parse_args()
 if args.cases <= 0: parser.error('--cases must be positive')
 rom=args.decompressed_rom.read_bytes()
 if len(rom)!=33554432 or hashlib.sha1(rom).hexdigest()!=ROM_SHA1:
  raise ValueError('decompressed ROM length/SHA-1 does not match pinned USA baseline')
 code=rom[ROM_OFFSET:ROM_OFFSET+FUNCTION_SIZE]
 words={BASE+4*i:struct.unpack('>I',code[4*i:4*i+4])[0]
        for i in range(FUNCTION_SIZE//4)}
 bind_library(args.host_library)
 fixed = fixed_scenarios()
 if {name for name, _ in fixed} != set(EXPECTED_FIXED_TRACES):
  raise AssertionError('fixed scenario names and expected trace fixtures differ')
 for name,p in fixed:
  actual=Machine(p).run(p)
  actual_trace=tuple(actual[k] for k in TRACE_FIELDS)
  if actual_trace != EXPECTED_FIXED_TRACES[name]:
   print('MISMATCH fixed MIPS trace',name,'expected',EXPECTED_FIXED_TRACES[name],
         'actual',actual_trace)
   return 1
  candidate=host(p)
  if actual!=candidate:
   print('MISMATCH fixed case',name,'params',p,'original',actual,'candidate',candidate)
   return 1
 r=random.Random(args.seed)
 for t in range(args.cases):
  p=scenario(r)
  actual=Machine(p).run(p)
  candidate=host(p)
  if actual!=candidate:
   print('MISMATCH case',t,'params',p,'original',actual,'candidate',candidate)
   return 1
 print(f'{len(fixed_scenarios())} fixed edge cases and {args.cases} deterministic synthetic '
       f'MIPS/C differential scenarios matched '
       f'(seed={args.seed}, original instructions from verified local ROM)')
 if args.check_mutants:
  check_mutants(args.c_compiler)
 return 0

if __name__=='__main__':
 raise SystemExit(main())
