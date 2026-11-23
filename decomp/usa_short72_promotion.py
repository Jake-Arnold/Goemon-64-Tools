"""Fail-closed USA 72 original IDO function staging on accepted 2092-C baseline."""
from pathlib import Path
import hashlib, json, re, struct, subprocess
from . import overlay_isolated233 as splice
from . import overlay_crossregion47 as cross
from . import usa_opening_new2_promotion as opening
from .glitch_g2_promotion import all_semantic_relocations

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'research/usa_short72_20261123/sources'
FIXTURE=ROOT/'research/usa_short72_20261123/manifest.json'
FORMAT='goemon-usa-short72-post2092-v1'
ROM_SHA1='6ea0ed71032ce08fc2745f412d84936382197494'
RELOC_HASH='f7f25e257c9bce27c00e756b85ca7bfa5774137925d5aba9a6626ba4693e5a97'
FROZEN_FIXTURE_HASH='20ec6ca1f9ad449fd535e2c375acabe01973711ee4622c299f54b49516fc1595'
def sha(b): return hashlib.sha256(b).hexdigest()
def fixture():
    raw=FIXTURE.read_bytes()
    if sha(raw)!=FROZEN_FIXTURE_HASH:raise ValueError('Unreviewed USA short72 fixture changed')
    doc=json.loads(raw)
    if (set(doc)!={'format','region','original_rom_sha1','upstream_commit','prior_c','prior_bytes','functions'} or
        (doc['format'],doc['region'],doc['original_rom_sha1'],doc['upstream_commit'],doc['prior_c'],doc['prior_bytes'])!=(FORMAT,'usa',ROM_SHA1,'7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee',2092,94760)):
        raise ValueError('Invalid 72-target original baseline')
    fs=doc['functions']; names=set();ranges=[]
    if len(fs)!=72 or sum(f['size'] for f in fs)!=4844:raise ValueError('New short72 count/size mismatch')
    for i,f in enumerate(fs):
        if set(f)!={'name','rom_offset','vma','size','source','source_sha256','original_code_sha256','original_asm'}:raise ValueError('Invalid 72 fields')
        if f['source']!=f'short72_{i:03d}' or f['name'] in names or not 8<=f['size']<100 or f['size']%4:raise ValueError('Name/source or original extent mismatch')
        n=re.fullmatch(r'func_([0-9A-Fa-f]{8})_([0-9A-Fa-f]+)',f['name'])
        if n is None or (int(n[1],16),int(n[2],16))!=(f['vma'],f['rom_offset']):raise ValueError('Unverified function original addresses')
        if sha((SOURCE/(f['source']+'.c')).read_bytes())!=f['source_sha256']:raise ValueError('Source changed: '+f['name'])
        names.add(f['name']);ranges.append((f['rom_offset'],f['rom_offset']+f['size']))
    if any(a[1]>b[0] for a,b in zip(sorted(ranges),sorted(ranges)[1:])):raise ValueError('Overlapping new original code')
    return doc
def validate_predecessor(manifest,rom=None):
    if manifest.get('overlay_usa_short72_stage')!={'format':FORMAT}:raise ValueError('Unreviewed USA short72 stage')
    from .verify import claimed_functions
    prev=claimed_functions({k:v for k,v in manifest.items() if k!='overlay_usa_short72_stage'})
    if (len(prev),sum(f['size'] for f in prev))!=(2092,94760):raise ValueError('Wrong accepted predecessor for new C')
    fs=fixture();old={(x['name'],x['rom_offset'],x['size']) for x in prev}
    span=sorted((x['rom_offset'],x['rom_offset']+x['size']) for x in prev)
    for f in fs['functions']:
        start,end=f['rom_offset'],f['rom_offset']+f['size']
        if (f['name'],start,f['size']) in old or any(start<b and a<end for a,b in span):raise ValueError('Already accepted/overlapping '+f['name'])
    if rom is not None:splice.validate_sources(rom,fs,SOURCE)
    return fs

def restore_original_abs_label_type(path, original_elf):
    """Restore one original ASM inline label metadata, never modifying machine code."""
    path=Path(path);src=path.read_bytes();out=bytearray(src)
    if out[:6]!=b'\x7fELF\x01\x02':raise ValueError('Not ELF32 big-endian')
    shoff=struct.unpack_from('>I',out,32)[0];shentsize,shnum,shstrndx=struct.unpack_from('>HHH',out,46)
    if shentsize!=40:raise ValueError('Unknown ELF section layout')
    shbase=struct.unpack_from('>I',out,shoff+40*shstrndx+16)[0]
    def secname(i):
        j=shbase+struct.unpack_from('>I',out,shoff+40*i)[0]
        return out[j:out.index(0,j)].decode('ascii')
    sec={secname(i):(shoff+40*i) for i in range(shnum)}
    if '.symtab' not in sec or '.strtab' not in sec:raise ValueError('Missing canonical symbol table')
    st=sec['.symtab'];strtab=sec['.strtab'];p,n=struct.unpack_from('>II',out,st+16);strings=struct.unpack_from('>I',out,strtab+16)[0]
    if n%16:raise ValueError('Malformed ELF symbol table')
    needed='D_080019A0_71D420';found=[]
    for i in range(n//16):
        at=p+16*i;no=struct.unpack_from('>I',out,at)[0]
        name=out[strings+no:out.index(0,strings+no)].decode('utf8')
        if name==needed:
            val,size=struct.unpack_from('>II',out,at+4);info=out[at+12];other=out[at+13];idx=struct.unpack_from('>H',out,at+14)[0]
            if (val,size,info,other,idx)!=(0x080019a0,0,0x10,0,0xfff1):raise ValueError('Unexpected original inline ABS provenance')
            found.append(at+12)
    if len(found)!=1:raise ValueError('Original ASM inline-label identity not unique')
    # Guard original exact symbol and expected type in the previous accepted ELF.
    def syms(elf):
        return [line.strip().split() for line in subprocess.check_output(['readelf','-Ws',str(elf)],text=True).splitlines() if needed in line]
    before=syms(original_elf)
    if len(before)!=1 or before[0][1:8]!=['080019a0','0','FUNC','GLOBAL','DEFAULT','ABS',needed]:raise ValueError('Unverified predecessor original inline-label type')
    out[found[0]]=0x12
    if sum(a!=b for a,b in zip(src,out))!=1:raise ValueError('Only one ELF metadata byte may change')
    path.write_bytes(out)
    return {'symbol':needed,'original_TYPE':'FUNC','source_split_TYPE':'NOTYPE','restored_elf_type':'FUNC','changed_metadata_byte':found[0],'code_and_relocations_unchanged':True,'sha256_before':sha(src),'sha256_after':sha(out)}

def verify_combined(baseline,prior,candidate,rom,plan):
    baseline,prior,candidate=map(Path,(baseline,prior,candidate))
    image=(candidate/'build/usa/mnsg.z64').read_bytes()
    if len(image)!=33554432 or image!=rom or hashlib.sha1(image).hexdigest()!=ROM_SHA1:raise ValueError('Full original USA ROM mismatch')
    old=prior if prior.is_file() else prior/'build/usa/mnsg.elf'; new=candidate/'build/usa/mnsg.elf'
    oldfunc=cross._funcs(old); newfunc=cross._funcs(new)
    if oldfunc!=newfunc or sum(newfunc.values())!=7376 or sum(cross._funcs(baseline/'build/usa/mnsg.elf').values())!=7376:raise ValueError('One of 7376 native ELF FUNC identity mismatched')
    r0,n0,h0=all_semantic_relocations(old);r1,n1,h1=all_semantic_relocations(new)
    if not (r0==r1 and n0==n1==82103 and h0==h1==RELOC_HASH):raise ValueError('82,103 canonical relocations modified')
    g0=opening.stable_globals(old);g1=opening.stable_globals(new)
    if g0!=g1:raise ValueError('One of 26,714 stable symbol names, types or locations changed')
    fs=fixture()['functions']
    link=(candidate/'build/usa/mnsg.map').read_text()
    plan_sources={f['name']:f['source'] for f in plan['functions']}
    if set(plan_sources)!={f['name'] for f in fs}:raise ValueError('New unit plan not same original 72 functions')
    for f in fs:
        pos=f['rom_offset'];size=f['size'];name=f['name']
        if (name,f['vma'],size) not in newfunc or name+'.NON_MATCHING' in link or f'build/usa/src/{plan_sources[name]}.c.o' not in link or sha(image[pos:pos+size])!=f['original_code_sha256']:
            raise ValueError('Native new original address lacks C source/ELF proof: '+name)
    return {'status':'PASSED_G2_LOCAL','prior_c':2092,'accepted_c_after':2164,'added_c':72,'added_original_bytes':4844,'accepted_original_bytes_after':99604,'remaining_assembly':5199,'original_rom_sha1':ROM_SHA1,'original_32MiB_ROM_bytes_exact':33554432,'positive_elf_function_identities_exact':7376,'semantic_relocations_exact':82103,'semantic_relocation_sha256':h1,'stable_global_symbol_identities_exact':sum(g1.values()),'full_rom_match':True,'all_semantic_relocations_equal':True,'stable_ELF_globals_equal':True,'original_elf_sha256':sha((baseline/'build/usa/mnsg.elf').read_bytes()),'accepted_predecessor_elf_sha256':sha(old.read_bytes()),'candidate_elf_sha256':sha(new.read_bytes())}
