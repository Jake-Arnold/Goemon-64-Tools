#!/usr/bin/env python3
"""Source-only, authenticated-ROM analysis of direct SP-relative original MIPS accesses.

No ROM bytes or extracted instructions are emitted. Not a full data-flow proof:
indirect stack accesses through non-$sp base registers would require separate analysis.
"""
from __future__ import annotations
import argparse,hashlib,json,struct,collections
from pathlib import Path
from trace_original_file22_mips import ROM_SHA1,FUNCTION_SHA256
ROM_OFFSET=0x69ECE4
SIZE=1808

def analyze(image:bytes)->dict:
 if len(image)!=33554432 or hashlib.sha1(image).hexdigest()!=ROM_SHA1:
  raise ValueError('Original USA decompressed 32 MiB SHA-1 mismatch')
 code=image[ROM_OFFSET:ROM_OFFSET+SIZE]
 if hashlib.sha256(code).hexdigest()!=FUNCTION_SHA256:
  raise ValueError('Original large function slice hash mismatch')
 refs=collections.defaultdict(lambda:collections.Counter())
 for offset,(word,) in enumerate(struct.iter_unpack('>I',code)):
  op=word>>26; rs=(word>>21)&31
  if rs!=29 or op not in {0x20,0x21,0x23,0x24,0x25,0x28,0x29,0x2B}:
   continue
  imm=struct.unpack('>h',struct.pack('>H',word&0xffff))[0]
  refs[imm]['load' if op in (0x20,0x21,0x23,0x24,0x25) else 'store']+=1
 accessed=sorted(refs)
 out={'status':'DIRECT_SP_REFERENCE_INVENTORY_NOT_SOURCE_PROOF',
  'original_decompressed_sha1':ROM_SHA1,'original_function_sha256':FUNCTION_SHA256,
  'frame_size_bytes':320,'instruction_positions':452,'direct_sp_reference_slot_count':len(accessed),
  'direct_sp_referenced_word_offsets':[hex(v) for v in accessed],
  'direct_sp_access_counts':{hex(k):dict(v) for k,v in sorted(refs.items())},
  'warning':'Direct $sp base references only, NOT proof that untouched frame bytes were unused or unallocated'}
 if len(accessed)!=18 or accessed[-1]!=0x138 or accessed[10]!=0x34:
  raise AssertionError('Original stack-reference inventory changed')
 return out

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--rom',type=Path,required=True)
 p.add_argument('--output',type=Path,required=True)
 a=p.parse_args()
 if a.output.exists():raise FileExistsError('Refuse to overwrite output')
 r=analyze(a.rom.read_bytes());a.output.write_text(json.dumps(r,indent=2)+'\n')
 print('PASS: authenticated original 320-byte frame has 18 distinct direct SP-relative word offsets')
