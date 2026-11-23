"""Research only: check the native VM pool layout; change section alignment only."""
import hashlib,struct,json,sys
from pathlib import Path
p=Path(sys.argv[1]);rom=Path(sys.argv[2]).read_bytes();raw=p.read_bytes(); b=bytearray(raw)
assert hashlib.sha1(rom).hexdigest()=='6ea0ed71032ce08fc2745f412d84936382197494'
assert raw[:7]==b'\x7fELF\x01\x02\x01'
sh=struct.unpack_from('>I',raw,32)[0];es,n,si=struct.unpack_from('>HHH',raw,46);assert es==40
sections=[struct.unpack_from('>10I',raw,sh+i*40) for i in range(n)]
strtab=sections[si]; names=raw[strtab[4]:strtab[4]+strtab[5]]
idx={names[s[0]:].split(b'\0',1)[0].decode():i for i,s in enumerate(sections)}
ri=idx['.rodata'];r=sections[ri]; assert (r[1],r[2],r[5],r[8])==(1,2,224,16)
data=raw[r[4]:r[4]+r[5]]; rel=sections[idx['.rel.rodata']];assert rel[5]==55*8 and rel[7]==ri
sym=sections[rel[6]]; textidx=idx['.text']; entries=[]
for i in range(55):
 off,info=struct.unpack_from('>II',raw,rel[4]+i*8); assert off==i*4 and info&255==2
 _,val,_,kind,_,sec=struct.unpack_from('>IIIBBH',raw,sym[4]+(info>>8)*16);assert val==0 and kind&15==3 and sec==textidx
 add=struct.unpack_from('>I',data,off)[0];entries.append(0x8003cfa0+add)
linked=b''.join(struct.pack('>I',x) for x in entries)+data[220:];assert linked==rom[0x7dc2c:0x7dd0c]
struct.pack_into('>I',b,sh+ri*40+32,4);assert sum(a!=c for a,c in zip(raw,b))==1
p.write_bytes(b);print(json.dumps({'native_pool_bytes':224,'assignment_bytes':60,'dispatcher_table_bytes':160,'float_bytes':4,'original_address':'0x8007D02C','relocations':55,'all_pool_words_exact_after_native_relocation':True,'alignment_before':16,'alignment_after':4,'only_alignment_metadata_changed':True,'before':hashlib.sha256(raw).hexdigest(),'after':hashlib.sha256(b).hexdigest()}))
