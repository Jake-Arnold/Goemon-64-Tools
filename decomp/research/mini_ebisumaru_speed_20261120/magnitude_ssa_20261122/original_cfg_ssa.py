#!/usr/bin/env python3
"""Read-only control-flow + reaching-def analysis for the USA clamp; no original code bytes printed.
Uses authenticated original ROM supplied by user; records only generic native metadata.
"""
from pathlib import Path
import argparse, hashlib, collections, struct, json
VMA=0x801cd310;ROM=0x589220;SIZE=4320;SHA='6ea0ed71032ce08fc2745f412d84936382197494'
def sext16(x):return x-0x10000 if x&0x8000 else x

def decode(rom):
 words=struct.unpack_from('>'+str(SIZE//4)+'I',rom,ROM)
 jtbl=struct.unpack_from('>18I',rom,0x5c676c)
 targets=sorted(set(x-VMA for x in jtbl))
 assert len(jtbl)==18 and len(targets)==5
 assert targets==[0xbc,0xe0,0x110,0x140,0x174],targets
 return words,targets

def branch_graph(words,jtbl):
 # State=(PC, delayed transfer target). None means ordinary instruction entry.
 # This context distinguishes a jump into a delay-slot address from execution
 # of the very same instruction as a pending branch delay slot.
 N=len(words);size=N*4;edges={};branches=[];delay_slots=set();dynamic=[]
 pending=[(0,None)]
 q=collections.deque(pending)
 while q:
  state=q.popleft()
  if state in edges:continue
  pc,delay_dst=state
  assert 0<=pc<size and pc%4==0, state
  w=words[pc//4];op=w>>26;rs=(w>>21)&31;rt=(w>>16)&31;fun=w&63
  if delay_dst is not None:
   delay_slots.add(pc)
   succ=[] if delay_dst==-1 else [(delay_dst,None)]
  else:
   target=pc+4+sext16(w&0xffff)*4
   if op in (4,5,6,7,0x14,0x15,0x16,0x17,1) or (op==0x11 and rs==8):
    assert 0<=target<size, (pc,target)
    likely=(op in (0x14,0x15,0x16,0x17)) or (op==1 and rt in (2,3,18,19)) or (op==0x11 and (rt & 3) in (2,3))
    succ=[(pc+4,target)]
    if likely:succ.append((pc+8,None))
    else:succ.append((pc+4,pc+8))
    branches.append({'pc':pc,'dest':target,'likely':likely})
   elif op in (2,3):
    if op==3:dst=pc+8
    else:dst=(((VMA+pc+4)&0xf0000000)|((w&0x3ffffff)<<2))-VMA
    assert 0<=dst<size,(hex(pc),hex(dst))
    succ=[(pc+4,dst)]
   elif op==0 and fun==8:
    if rs==31:succ=[(pc+4,-1)]
    elif rs==12:succ=[(pc+4,t) for t in jtbl];dynamic.append(pc)
    else:raise AssertionError(('unknown jr',hex(pc),rs))
   else:succ=[(pc+4,None)] if pc+4<size else []
  edges[state]=succ
  for t in succ:
   if t not in edges:q.append(t)
 return edges,delay_slots,branches,dynamic

def reaching_definitions(edges, write_sites, read_sites):
 """Forward may-def analysis on contextual delayed-branch states.

 A write is associated with an instruction PC, not an edge. When the same
 instruction is entered both ordinarily and as a branch delay slot, its
 write applies on each actually executed path.
 """
 writes=set(write_sites)
 reads=set(read_sites)
 inp=collections.defaultdict(set)
 inp[(0,None)].add(None)
 q=collections.deque([(0,None)])
 processed=0
 while q:
  state=q.popleft();processed+=1
  value={state[0]} if state[0] in writes else inp[state]
  for nxt in edges[state]:
   if not value.issubset(inp[nxt]):
    inp[nxt]|=value;q.append(nxt)
 assert processed<100000
 result={r:set().union(*(defs for state,defs in inp.items() if state[0]==r)) for r in reads}
 return result,inp,processed

def analyze(rom):
 assert len(rom)==33554432 and hashlib.sha1(rom).hexdigest()==SHA
 words,jtbl=decode(rom);edges,slots,branches,dynamic=branch_graph(words,jtbl)
 reads={};writes={}
 for i,w in enumerate(words):
  pc=i*4;op=w>>26;base=(w>>21)&31;reg=(w>>16)&31;disp=w&0xffff
  if base==29 and disp==0x8c and op in (0x31,0x39,0x23,0x2b,0x25,0x29):
   if op in (0x39,0x2b,0x29):writes[pc]=(op,reg)
   else: reads[pc]=(op,reg)
 assert writes=={0x218:(0x39,14),0x4e4:(0x39,0),0xffc:(0x39,8)},writes
 assert reads=={0xfe8:(0x31,4),0x1000:(0x31,10)},reads
 for x in set(reads)|set(writes):assert x not in slots
 # No call takes address directly with addiu $aN,$sp,+8c
 escaped=[]
 for i,w in enumerate(words):
  op=w>>26;rs=(w>>21)&31;rt=(w>>16)&31;disp=w&0xffff
  if op in (8,9,13) and rs==29 and disp==0x8c:escaped.append(i*4)
 # MIPS branch-likely delay slots are represented as distinct CFG states.
 reached,incoming,processed=reaching_definitions(edges,writes,reads)
 reached={r:sorted('0x%X'%k if k is not None else 'UNINITIALIZED' for k in defs) for r,defs in reached.items()}
 # Finite state witness generation: preserve the last magnitude writer through
 # the executable (PC, delay-slot-target) state graph without evaluating flags.
 witnesses={}
 for writer in (0x218,0x4e4):
  source=((0,None),None)
  queue=collections.deque([source]);parent={source:None};winner=None
  while queue:
   state,last=queue.popleft()
   if state[0]==0xfe8 and last==writer:
    winner=(state,last);break
   now=state[0] if state[0] in writes else last
   for succ in edges[state]:
    key=(succ,now)
    if key not in parent:
     parent[key]=(state,last);queue.append(key)
  assert winner is not None, ('missing witness',hex(writer))
  trace=[];cur=winner
  while cur is not None:
   trace.append(cur[0][0]);cur=parent[cur]
  trace.reverse()
  # summarize without copying original instruction words or full disassembly
  witnesses[f'0x{writer:X}']={'transition_count':len(trace)-1,'passes_zero_definition':0x218 in trace,'passes_sqrt_overwrite':0x4e4 in trace,'late_read':'0xFE8','chosen_branch_sites_near_sqrt':[hex(x) for x in trace if 0x300<=x<=0x550 and x in {b['pc'] for b in branches}][:12]}
 return {'status':'ORIGINAL_CFG_REACHING_DEFS_VALIDATED','function_relative_size':SIZE,'native_instructions':len(words),'branch_points':len(branches),'branch_likely_count':sum(b['likely'] for b in branches),'dynamic_jump_sites':len(dynamic),'jump_table_entries':18,'distinct_jump_targets':len(jtbl),'reached_cfg_states':len(incoming),'graph_updates':processed,'delay_slot_instructions':len(slots),'dual_entry_delay_slot_pcs':[hex(pc) for pc in sorted(slots) if (pc,None) in edges],'magnitude_source_witnesses':witnesses,'sp8c_writes':[hex(x) for x in writes],'sp8c_reads':[hex(x) for x in reads],'sp8c_definitions_at_reads':{'0x%x'%k:v for k,v in reached.items()},'escaped_direct_address_at':[hex(x) for x in escaped]}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--rom',type=Path,required=True);p.add_argument('--output',type=Path);a=p.parse_args()
 result=analyze(a.rom.read_bytes());print(json.dumps(result,indent=2))
 if a.output:a.output.write_text(json.dumps(result,indent=2)+'\n')
