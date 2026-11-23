"""Fail-closed post-USA2090 promotion for two original file18 IDO C helpers.

Uses the already accepted stable-decomp 2,090-C predecessor and authentic
native SGI IDO5.3; never patches machine instructions, the ROM or ASM operands.
"""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import hashlib,json,re,struct,subprocess

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'research/usa_file18_new2_20261123/sources'
FIXTURE=ROOT/'research/usa_file18_new2_20261123/manifest.json'
FORMAT='goemon-usa-file18-new2-post2090-v1'
FIXTURE_HASH='0403e2cd99315379c79a8c454de45bf5e8b8b6c7d20544c8b941da2399f43ee3'
ROM_SHA1='6ea0ed71032ce08fc2745f412d84936382197494'
RELOC_HASH='f7f25e257c9bce27c00e756b85ca7bfa5774137925d5aba9a6626ba4693e5a97'
EXPECTED=(('func_8020D7E8_6771C8',0x6771C8,0x8020D7E8,48),
          ('func_8021F330_688D10',0x688D10,0x8021F330,44))

def sha(b):return hashlib.sha256(b).hexdigest()

def fixture():
    raw=FIXTURE.read_bytes()
    if sha(raw)!=FIXTURE_HASH:raise ValueError('USA new2 fixture SHA256 changed')
    d=json.loads(raw)
    if set(d)!= {'format','region','original_rom_sha1','upstream_commit','prior_c','prior_bytes','functions'} or (
        d['format'],d['region'],d['original_rom_sha1'],d['upstream_commit'],d['prior_c'],d['prior_bytes'])!=(FORMAT,'usa',ROM_SHA1,'7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee',2090,94668):
        raise ValueError('Unapproved post2090 fixture')
    fs=d['functions']
    if len(fs)!=2 or tuple((f['name'],f['rom_offset'],f['vma'],f['size']) for f in fs)!=EXPECTED:
        raise ValueError('Wrong or reordered original USA source targets')
    from . import overlay_isolated233 as isolated
    for f in fs:
        if set(f)!={'name','rom_offset','vma','size','source','source_sha256','original_code_sha256','original_asm'} or f['original_asm']!='file_18' or not re.fullmatch(r'new2_native_0[01]',f['source']):
            raise ValueError('Unapproved new2 source unit')
        if sha((SOURCE/(f['source']+'.c')).read_bytes())!=f['source_sha256']:
            raise ValueError('Authentic new2 C source changed')
    return d

def validate_predecessor(manifest,rom=None):
    if manifest.get('overlay_usa_opening_new2_stage')!={'format':FORMAT}:
        raise ValueError('Missing or unexpected USA new2 gate')
    other={k:v for k,v in manifest.items() if k!='overlay_usa_opening_new2_stage'}
    from .verify import claimed_functions
    prev=claimed_functions(other)
    if len(prev)!=2090 or sum(x['size'] for x in prev)!=94668:
        raise ValueError('USA new2 requires accepted exact 2090-C predecessor')
    got={(x['name'],x['rom_offset'],x['size']) for x in prev}
    ranges=sorted((x['rom_offset'],x['rom_offset']+x['size']) for x in prev)
    for name,at,vma,size in EXPECTED:
        if (name,at,size) in got or any(at<hi and lo<at+size for lo,hi in ranges):
            raise ValueError('USA new2 is already owned or overlaps original C '+name)
    d=fixture()
    if rom is not None:
        from . import overlay_isolated233 as isolated
        isolated.validate_sources(rom,d,SOURCE)
    return d

def elf_sections(raw):
    if raw[:6]!=b'\x7fELF\x01\x02' or struct.unpack_from('>H',raw,18)[0]!=8:
        raise ValueError('Authentic MIPS big-endian ELF32 object required')
    shoff=struct.unpack_from('>I',raw,32)[0]
    entsize,num,sidx=struct.unpack_from('>HHH',raw,46)
    if entsize!=40 or not num or sidx>=num:raise ValueError('Unknown ELF section layout')
    def head(i):return shoff+40*i
    base=struct.unpack_from('>I',raw,head(sidx)+16)[0]
    def name(at):return raw[at:raw.index(0,at)].decode('ascii')
    out={}
    for i in range(num):
        h=head(i);n=name(base+struct.unpack_from('>I',raw,h)[0]);off,size=struct.unpack_from('>II',raw,h+16)
        out[n]={'index':i,'head':h,'offset':off,'size':size,'link':struct.unpack_from('>I',raw,h+24)[0],
                'entsize':struct.unpack_from('>I',raw,h+36)[0]}
    return out

def patch_absolute_symbol_type(path):
    """Correct only original ABS symbol provenance NOTYPE; no MIPS instructions patched."""
    path=Path(path);original=path.read_bytes();buf=bytearray(original)
    sec=elf_sections(original)
    if not {'.symtab','.text','.rel.text'}<=set(sec):raise ValueError('Missing native C object sections')
    tab=sec['.symtab'];strings=sec.get('.strtab')
    if not strings or tab['entsize']!=16 or tab['size']%16:raise ValueError('Unexpected IDO symbol table')
    name='D_CF8F8';positions=[]
    for i in range(tab['size']//16):
        at=tab['offset']+16*i
        nameoff=struct.unpack_from('>I',buf,at)[0]
        current=buf[strings['offset']+nameoff:buf.index(0,strings['offset']+nameoff)].decode('ascii')
        if current==name:
            if (buf[at+12],struct.unpack_from('>I',buf,at+4)[0],struct.unpack_from('>I',buf,at+8)[0],struct.unpack_from('>H',buf,at+14)[0])!=(0x11,0,0,0):
                raise ValueError('Unexpected original-symbol type/size/binding')
            positions.append(at+12)
    if len(positions)!=1:raise ValueError('D_CF8F8 symbol is not uniquely typed OBJECT')
    buf[positions[0]]=0x10
    if sum(a!=b for a,b in zip(original,buf))!=1 or len(original)!=len(buf):
        raise ValueError('Adapter may change one ELF st_info metadata byte only')
    for key in ('.text','.rel.text'):
        x=sec[key];s=x['offset'];e=s+x['size']
        if original[s:e]!=buf[s:e]:raise ValueError('Native code/relocations mutated')
    path.write_bytes(buf)
    return {'changed_metadata_byte':positions[0],'symbol':name,'original_type':'OBJECT','restored_type':'NOTYPE',
            'native_MIPS_instructions_untouched':True,'native_relocations_untouched':True,
            'original_object_sha256':sha(original),'retargeted_object_sha256':sha(buf)}

def stable_globals(elf):
    out=Counter()
    for line in subprocess.check_output(['readelf','-Ws',str(elf)],text=True).splitlines():
        p=line.strip().split()
        if (len(p)>=8 and p[0].endswith(':') and p[4] in ('GLOBAL','WEAK') and p[6]!='UND' and
                not p[7].startswith('.L') and not p[7].endswith('.NON_MATCHING')):
            out[tuple(p[1:8])]+=1
    return out

def verify_link(baseline,prior,candidate,rom,plan):
    from . import overlay_crossregion47 as cross
    from .glitch_g2_promotion import all_semantic_relocations
    baseline,prior,candidate=map(Path,(baseline,prior,candidate))
    newrom=(candidate/'build/usa/mnsg.z64').read_bytes()
    if len(newrom)!=33554432 or newrom!=rom or hashlib.sha1(newrom).hexdigest()!=ROM_SHA1:
        raise ValueError('Post2090 new2 full 32 MiB USA ROM fails original identity')
    baseline_elf=baseline/'build/usa/mnsg.elf'
    candidate_elf=candidate/'build/usa/mnsg.elf'
    previous=cross._funcs(prior);new=cross._funcs(candidate_elf);original=cross._funcs(baseline_elf)
    if previous!=new or sum(original.values())!=7376 or sum(new.values())!=7376:
        raise ValueError('Any of 7,376 original ELF FUNC identities changed')
    reloc0,n0,h0=all_semantic_relocations(prior)
    reloc1,n1,h1=all_semantic_relocations(candidate_elf)
    if n0!=n1 or n0!=82103 or h0!=h1 or h0!=RELOC_HASH or reloc0!=reloc1:
        raise ValueError('Canonical original 82,103 semantic relocation provenance mismatch')
    globals0=stable_globals(prior);globals1=stable_globals(candidate_elf)
    if globals0!=globals1:
        raise ValueError('Stable global symbol identity/type mismatch: '+str((globals0-globals1).most_common(4)))
    for f in fixture()['functions']:
        a=f['rom_offset'];n=f['size']
        if newrom[a:a+n]!=rom[a:a+n] or sha(rom[a:a+n])!=f['original_code_sha256']:
            raise ValueError('New C function mismatches original address/size/bytes')
    return {'status':'PASSED_G2_LOCAL','added_c':2,'added_original_bytes':92,'accepted_c_before':2090,
            'accepted_c_after':2092,'accepted_original_bytes_after':94760,'remaining_asm':5271,
            'original_rom_size':len(newrom),'original_sha1':ROM_SHA1,
            'ELF_function_identities':7376,'stable_global_identical_count':sum(globals0.values()),
            'complete_semantic_relocations':n0,'semantic_relocation_sha256':h0,
            'full_ROM_equal':True,'all_ELF_functions_equal':True,
            'stable_ELF_globals_equal':True,'all_semantic_relocations_equal':True,
            'retained_asm_fragments':len(plan['assembly'])}
