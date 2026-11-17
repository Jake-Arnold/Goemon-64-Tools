from pathlib import Path
import os
import struct,hashlib,json,subprocess,re
ROOT=Path(os.environ['GOEMON_CANDIDATE']).resolve()
ORG=(Path(os.environ['GOEMON_BASELINE'])/'config/usa/baserom.decompressed.z64').read_bytes()
M=json.loads((ROOT/'promotion_scratch_metadata.json').read_text())['functions']
checks=[]
for f in M:
 name=f['name'];size=f['size'];rom=int(f['rom_offset'],16)
 p=ROOT/f'build/usa/src/promotion_scratch/{name}.c.o'
 data=bytearray(p.read_bytes())
 assert data[:6]==b'\x7fELF\x01\x02',name+' ELF not big-endian 32'
 shoff=struct.unpack_from('>I',data,32)[0]
 count=struct.unpack_from('>H',data,48)[0]
 shentsize=struct.unpack_from('>H',data,46)[0]
 assert shentsize==40 and count>0
 text_sections=[]
 for i in range(count):
  h=shoff+40*i
  typ,flags=struct.unpack_from('>II',data,h+4)
  if typ==1 and flags==6:text_sections.append(h)
 assert len(text_sections)==1,(name,text_sections)
 h=text_sections[0]
 data_off,sect_size=struct.unpack_from('>II',data,h+16)
 align=struct.unpack_from('>I',data,h+32)[0]
 assert sect_size==(size+15)&~15,(name,size,sect_size)
 assert align==16,(name,align)
 assert data[data_off:data_off+size]==ORG[rom:rom+size], name+' original code mismatch'
 assert not any(data[data_off+size:data_off+sect_size]),name+' nonzero tail padding'
 symtext=subprocess.check_output(['readelf','-Ws',str(p)],text=True)
 found=[a for a in (row.split() for row in symtext.splitlines()) if len(a)>7 and a[3]=='FUNC' and a[7]==name]
 assert len(found)==1 and int(found[0][2])==size and int(found[0][1],16)==0, name+' symbol mismatch'
 # We do not accept external relocations for this initial promotion scratch.
 rels=subprocess.check_output(['readelf','-Wr',str(p)],text=True)
 assert 'There are no relocations in this file.' in rels,name+' has MIPS relocations'
 struct.pack_into('>I',data,h+20,size)
 struct.pack_into('>I',data,h+32,4)
 p.write_bytes(data)
 checks.append({'name':name,'bytes':size,'sha256':hashlib.sha256(ORG[rom:rom+size]).hexdigest(),
                'trimmed_zero_padding':sect_size-size})
print('PACKED_VERIFIED',len(checks),'ORIGINAL_BYTES',sum(x['bytes'] for x in checks))
print('TRIMMED_ZERO_PADDING_BYTES',sum(x['trimmed_zero_padding'] for x in checks))
(ROOT/'promotion_scratch_compiler_proof.json').write_text(json.dumps(checks,indent=2))
