from pathlib import Path
import os
import struct,json,hashlib,subprocess,re
ROOT=Path(os.environ['GOEMON_CANDIDATE']).resolve()
meta=json.loads((ROOT/'promotion_scratch_metadata.json').read_text())['functions']
RANGES={
'file_12':(0x5C8770,0x5E3C90,'5C8770'),
'file_13':(0x5F6840,0x634E30,'5F6840'),
'file_14':(0x63A2B0,0x6576E0,'63A2B0'),
'file_15':(0x65E310,0x666140,'65E310'),
'file_17':(0x66C250,0x6759D0,'66C250'),
'file_18':(0x676C80,0x693770,'676C80'),
'file_19':(0x694CA0,0x69C000,'694CA0')}
changes=[]
for sec,(start,end,orig) in RANGES.items():
 fns=sorted((e for e in meta if e['section']==sec),key=lambda e:int(e['rom_offset'],16))
 if not fns: continue
 intervals=[]
 cursor=start
 for f in fns:
  offset=int(f['rom_offset'],16)
  intervals.append((cursor,offset))
  cursor=offset+f['size']
 intervals.append((cursor,end))
 for n,(left,right) in enumerate(intervals):
  p=ROOT/f'build/usa/asm/usa/{orig}_scratch_part_{n:03}.s.o'
  if left==right:
   assert not p.exists(),(p,'Unexpected zero-sized ASM object')
   continue
  assert p.exists(),('Missing ASM object',p)
  b=bytearray(p.read_bytes())
  assert b[:6]==b'\x7fELF\x01\x02'
  hoff=struct.unpack_from('>I',b,32)[0];count=struct.unpack_from('>H',b,48)[0];step=struct.unpack_from('>H',b,46)[0]
  assert step==40
  ids=[]
  for i in range(count):
   sh=hoff+i*step;t,flags=struct.unpack_from('>II',b,sh+4)
   if t==1 and flags==6:ids.append(sh)
  assert len(ids)==1,(p,len(ids))
  sh=ids[0];offs,size=struct.unpack_from('>II',b,sh+16);align=struct.unpack_from('>I',b,sh+32)[0]
  needed=right-left
  assert size>=needed and size<=needed+15,(p,size,needed)
  assert not any(b[offs+needed:offs+size]),(p,'nonzero padding')
  assert align in (4,16),(p,align)
  struct.pack_into('>I',b,sh+20,needed)
  struct.pack_into('>I',b,sh+32,4)
  p.write_bytes(b)
  changes.append((str(p.relative_to(ROOT)),needed,size-needed))
print('TRIMMED_ASM_OBJECTS',len(changes),'EXPECTED_ORIGINAL_ASM_BYTES',sum(x[1] for x in changes),'PADDED_ASM_BYTES_REMOVED',sum(x[2] for x in changes))
(ROOT/'promotion_scratch_asm_padding_proof.json').write_text(json.dumps([dict(path=p,original_code_bytes=n,removed_zero_padding=pad) for p,n,pad in changes],indent=2))
