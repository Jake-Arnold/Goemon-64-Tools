"""Post-E234 native F37C/DF98 stage: independent full original-ASM references.

No relocation filter, rewrite, or default comparator change. The reference pair
is assembled from pinned original Splat source, not candidate instructions.
The prior mixed-C build must independently reproduce the original named gate;
only the two explicitly scoped native local-pool changes may differ thereafter.
"""
from __future__ import annotations
import hashlib,json,re,shutil,subprocess,sys,os
from collections import Counter
from pathlib import Path
from .probe import Elf32
from .glitch_g2_promotion import all_semantic_relocations
from .overlay_crossregion47 import _funcs
from .usa_opening_new2_promotion import stable_globals
from .native251_promotion import runmake,restore_inline_usa
from .usa_short72_promotion import restore_original_abs_label_type
from . import usa_script_vm440_promotion as vm440

ROOT=Path(__file__).resolve().parent
KEY='usa_script_vm_dual_reference'
FORMAT='goemon-usa-script-vm-dual-original-reference-v1'
ROM_SHA=vm440.ROM_SHA
RETAIL_SHA='df8083a54296b8c151917c5333e1c85f014a2a66'
PRIOR_ELF='f03cb69cf367c2627d6e5e3e0838e2753b7bd13f67da3796f7d619d323043cad'
NEW_ELF='42a11447a374762135e2bc2e72d185b4efd9e35bee5c91eec071284bfb8bcd1e'
NEW_RELOC='d5a4088ec689e35bce8f766c400d8ddb8dd2b42662ad30cdf2492ff6d17f8e19'
ORIG_ASM='8926b42c28518fc93ccd74f8f2635a25a9d1d54fbe40d0b936e398f2299cfc17'
ORIG_DATA='77353a624400b81dd7c3e664a3215cfb93da487723d51bac0c29256445b8b90d'
PRIOR_ASM='351d6e1019f1c462651cd6ce603688cd4abaa14d2149257f87d809b9695bb6d3'
SHADOW_ASM='c71550666d6669638d25613b2304974bd032db8161a140432fcec2eebf59b5e0'
CROSS_METADATA='5eef2ba3a2a00040032e7643ae46e10841ace84982e71ac3f167c6fc35bcf768'
MIXED_SHA='e95c02d7215f61aa15a5395dd21368607f626cdf43eeae67ffe13e199b01cfbb'
TARGETS=(
 dict(name='func_8003DF98_3EB98',rom_offset=0x3EB98,vma=0x8003DF98,size=528,source='research/usa_script_vm_df98_reference_20261123/df98.c',source_sha256='8eaf68308afa51862d07ee5795db6cbfd09250070bd243ad69744f6aa144a1f9',code_sha256='76285ca92a7f611916d867d9938f93fcb3df32ebfa2962120083f2471a501631'),
 dict(name='func_8003F37C_3FF7C',rom_offset=0x3FF7C,vma=0x8003F37C,size=192,source='research/usa_script_vm_f37c_reference_20261123/f37c.c',source_sha256='4cca0e20ec00d4b2e3b45b3acfe3d3c05fb74aa06c87f85e6da3026bdbee6cdb',code_sha256='74867178f34d8d45b1753520e1218d6e6c2307f44937258e95c3828f1cf1efd0'))
RESEARCH=ROOT/'research/usa_script_vm_combined2319_20261123'
sha=lambda b:hashlib.sha256(b).hexdigest()

def require(ok,msg):
    if not ok:raise ValueError('VM dual reference: '+msg)

def claims():
    return [{k:f[k] for k in ('name','rom_offset','vma','size')} for f in TARGETS]

def validate_predecessor(manifest,rom=None):
    from .verify import claimed_functions
    require(manifest.get(KEY)=={'format':FORMAT},'unreviewed stage')
    require(manifest.get(vm440.KEY)=={'format':vm440.FORMAT},'missing E234 predecessor')
    old=claimed_functions({k:v for k,v in manifest.items() if k!=KEY})
    require((len(old),sum(f['size'] for f in old))==(2317,110288),'wrong predecessor count')
    unit=next(u for u in manifest['units'] if u['source']=='script_vm.c')
    for f in TARGETS:
        require(unit['assembly_functions'].count(f['name'])==1,'missing original ASM owner')
        require(not any(x['name']==f['name'] or x['rom_offset']<f['rom_offset']+f['size'] and f['rom_offset']<x['rom_offset']+x['size'] for x in old),'duplicate original owner')
        require(sha((ROOT/f['source']).read_bytes())==f['source_sha256'],'tested C drift')
    if rom is not None:
        require(len(rom)==33554432 and hashlib.sha1(rom).hexdigest()==ROM_SHA,'wrong original ROM')
        for f in TARGETS:require(sha(rom[f['rom_offset']:f['rom_offset']+f['size']])==f['code_sha256'],'wrong original function bytes')
    require(sha((RESEARCH/'replay.py').read_bytes())=='a1dea8754f2ebf9bdfa44a15f011d1279aab286fba6facc8fed01585775ca9df','replay source drift')
    require(sha((RESEARCH/'audit_reference_delta.py').read_bytes())=='23f438f85a722b94172d2b799ca682431f34dc2ac002bd6f1dd50dc1c37d0675','reference audit drift')
    return old

def reference_sources(original,data):
    """Prior normalization is separately validated against *all* old relocs.
    The two new local-pool transformations then produce the independent shadow.
    Exact hashes bind the authentic Splat inputs and both derived references.
    """
    require(sha(original.encode())==ORIG_ASM and sha(data.encode())==ORIG_DATA,'original ASM inputs drift')
    s=original
    for site in ('3F014','3F494'):
        s,n=re.subn(r'(?m)^(\s*/\* '+site+r' [^\n]*?\*/[^\n]*?)%hi\(D_3ADCE\)',r'\g<1>0x0004',s);require(n==1,'prior literal high site')
    for site in ('3F020','3F4A0'):
        s,n=re.subn(r'(?m)^(\s*/\* '+site+r' [^\n]*?\*/[^\n]*?)%lo\(D_3ADCE\)',r'\g<1>-0x5232',s);require(n==1,'prior literal low site')
    for sym,disp,sites in [('D_801C77F0_1C83F0',8,['3F28C','3F294','3FE18','3FE1C']),('D_801C77F4_1C83F4',12,['3F4C8','3F4CC','3F558','3F578','3F5B4','3F5C4']),('D_801C77F8_1C83F8',16,['40068','40070','401FC','40204'])]:
        for site in sites:
            s,n=re.subn(r'(?m)^(\s*/\* '+site+r' [^\n]*?\*/[^\n]*?)%(hi|lo)\('+sym+r'\)',lambda m:m[1]+'%'+m[2]+'(D_801C77E8_1C83E8+'+str(disp)+')',s);require(n==1,'prior alias site')
    def pool(text,symbol,label,count):
        require(text.count('%hi('+symbol+')')==text.count('%lo('+symbol+')')==1,'pool references not unique')
        m=re.search(r'^dlabel '+symbol+r'\n(.*?)^enddlabel '+symbol+r'$',data,re.M|re.S);require(m is not None,'original pool missing')
        lines=[l for l in m[1].splitlines() if '*/' in l][:count];require(len(lines)==count,'wrong pool extent')
        labels={m[1] for l in lines if (m:=re.search(r'\.word (\.L\w+)',l))}
        for lab in labels:
            text,n=re.subn(r'(?m)^  jlabel '+re.escape(lab)+r'$', '  '+lab+':',text);require(n==1,'wrong original local label')
        return text.replace(symbol,label),label+':\n'+'\n'.join(lines)+'\n'
    s,a=pool(s,'jtbl_8007D02C_7DC2C','.Lvm_assignment_pool',15)
    section='\n.section .rodata,"a"\n.balign 4\n';before=s+section+a
    s,b=pool(s,'jtbl_8007D068_7DC68','.Lvm_dispatch_pool',40)
    s,c=pool(s,'D_8007D108_7DD08','.Lvm_f37c_pool',1)
    after=s+section+a+b+c
    require(sha(before.encode())==PRIOR_ASM and sha(after.encode())==SHADOW_ASM,'independent source normalization drift')
    return before,after

def object_identity(asm,native,counts):
    a,b=Elf32(asm),Elf32(native)
    for section,extent,count in (('.text',10112,counts[0]),('.rodata',counts[1]*4+(4 if counts[1]==55 else 0),counts[1])):
        i,j=a.names.index(section),b.names.index(section)
        def records(e,z):return Counter((r.offset,r.relocation_type,r.symbol.name or e.names[r.symbol.section],r.symbol.value,r.addend) for r in e.relocations(z))
        x,y=records(a,i),records(b,j)
        require(len(a.payload(i))==extent and a.payload(i)==b.payload(j),'independent '+section+' payload differs')
        require(sum(x.values())==count and x==y,'independent '+section+' relocations differ')

def check_linked(native_before,native_after,ref_before,ref_after):
    """Four independent linked images, no filtering of any relocation multiset."""
    files=(native_before,native_after,ref_before,ref_after)
    r=[all_semantic_relocations(x) for x in files]
    require([(n,h) for _,n,h in r]==[(82103,vm440.RELOC_SHA),(82102,NEW_RELOC),(82103,vm440.RELOC_SHA),(82102,NEW_RELOC)],'whole ELF relocation fingerprints differ')
    require(r[0][0]==r[2][0] and r[1][0]==r[3][0],'native/reference full relocation multisets differ')
    removed,added=r[0][0]-r[1][0],r[1][0]-r[0][0]
    require((sum(removed.values()),sum(added.values()))==(45,44),'unrecognised relocation delta')
    f=list(map(_funcs,files));g=list(map(stable_globals,files))
    require(f[0]==f[1] and f[2]==f[3] and all(sum(x.values())==7376 for x in f),'function identity changed within native or independent pair')
    require(g[0]==g[1] and g[2]==g[3] and all(sum(x.values())==26714 for x in g),'stable global identity changed within native or independent pair')
    # The independent reference assembles the whole original VM, not the already
    # accepted C siblings. These cross-pair metadata differences predate the
    # new targets and must be identical on both sides, not silently filtered.
    oldf=Counter({('func_8003F6E8_402E8',0x8003F6E8,48):1});newf=Counter({('func_8003F6E8_402E8',0x8003F6E8,56):1})
    require(f[2]-f[0]==oldf and f[0]-f[2]==newf and f[3]-f[1]==oldf and f[1]-f[3]==newf,'unexpected cross-reference function metadata')
    a,b=g[2]-g[0],g[0]-g[2];require(a==g[3]-g[1] and b==g[1]-g[3] and sum(a.values())==sum(b.values())==39,'cross-reference metadata delta changed')
    require(sha(json.dumps([sorted(a.items()),sorted(b.items())],separators=(',',':')).encode())==CROSS_METADATA,'unexpected historical cross-reference metadata')
    return {'original_named_relocations':82103,'independent_prior_relocations':82103,'native_relocations':82102,'independent_shadow_relocations':82102,'native_predecessor_relocation_sha256':vm440.RELOC_SHA,'native_shadow_relocation_sha256':NEW_RELOC,'entire_reference_relocations_equal':True,'removed_named_records':45,'added_section_records':44,'native_function_identities':7376,'native_stable_globals':26714,'independent_function_identities':7376,'independent_stable_globals':26714,'unchanged_cross_reference_metadata_sha256':CROSS_METADATA,'original_named_relocation_gate_exact':False,'ordinary_comparator_unchanged':True}

def apply_usa(candidate,baseline,work,uv,jobs):
    candidate,baseline,work=map(Path,(candidate,baseline,work));repo=ROOT.parent
    rom=(baseline/'config/usa/baserom.decompressed.z64').read_bytes()
    require(len(rom)==33554432 and hashlib.sha1(rom).hexdigest()==ROM_SHA,'wrong expanded ROM')
    prior_elf=candidate/'build/usa/mnsg.elf';require(sha(prior_elf.read_bytes())==PRIOR_ELF,'E234 predecessor fingerprint differs')
    require((candidate/'build/usa/mnsg.z64').read_bytes()==(baseline/'build/usa/mnsg.z64').read_bytes()==rom,'wrong predecessor ROM')
    (ROOT/'COMPILER_QUIRKS.md').read_text()
    out=work/'vmdual-native';subprocess.run([sys.executable,str(RESEARCH/'replay.py'),'--repo',str(repo),'--predecessor',str(candidate),'--out',str(out),'--uv',str(uv),'--jobs',str(jobs)],check=True)
    new=out/'candidate';newelf=new/'build/usa/mnsg.elf';require(sha(newelf.read_bytes())==NEW_ELF,'new native ELF fingerprint differs')
    auditout=out/'reference-delta.json';subprocess.run([sys.executable,str(RESEARCH/'audit_reference_delta.py'),'--repo',str(repo),'--rom',str(baseline/'config/usa/baserom.decompressed.z64'),'--object',str(new/'build/usa/src/script_vm.c.o'),'--combined',str(out/'evidence.json'),'--out',str(auditout)],check=True)
    audit=json.loads(auditout.read_text());require(audit['status']=='RESEARCH_ONLY_ALL_DELTA_RECORDS_EXACT_AGAINST_INDEPENDENT_REFERENCE' and len(audit['negative_controls_rejected'])==7,'exact delta audit failed')
    original=(baseline/'asm/usa/3DBA0.s').read_text();data=(baseline/'asm/usa/data/main_continued.rodata.s').read_text()
    sources=reference_sources(original,data);refs=[]
    for label,source,co,counts in zip(('prior','shadow'),sources,(candidate,new),((740,15),(739,55))):
        ref=work/('vmdual-asm-'+label);shutil.copytree(co,ref,symlinks=True);asm=work/('vmdual-asm-'+label+'.s');asm.write_text(source);obj=work/('vmdual-asm-'+label+'.o')
        subprocess.run(['mips-linux-gnu-as','-EB','-mtune=vr4300','-march=vr4300','-mabi=32','-Iinclude','-I.','-o',str(obj),str(asm)],cwd=baseline,check=True)
        build=ref/'build/usa';dest=build/'src/script_vm.c.o';object_identity(obj.read_bytes(),dest.read_bytes(),counts)
        shutil.copyfile(obj,dest);os.utime(dest,None)
        for name in ('mnsg.elf','mnsg.z64'):(build/name).unlink()
        runmake(ref,'usa',(ref/'.splat/usa/mnsg.ld').read_text(),['build/usa/mnsg.z64'],work/('vmdual-link-'+label+'.log'),uv,jobs)
        require(dest.read_bytes()==obj.read_bytes(),'independent ASM object replaced during link')
        require((build/'mnsg.z64').read_bytes()==rom,'independent full ROM differs')
        # Reapply only previously accepted metadata restoration outside VM.
        elf=build/'mnsg.elf';restore_original_abs_label_type(elf,co/'build/usa/mnsg.elf');restore_inline_usa(elf,co/'build/usa/mnsg.elf');refs.append(elf)
    proof=check_linked(prior_elf,newelf,*refs)
    require((new/'build/usa/mnsg.z64').read_bytes()==rom,'candidate full ROM differs')
    for f in TARGETS:
        off=f['rom_offset'];size=f['size'];require(sha(rom[off:off+size])==f['code_sha256'],'wrong original function')
        require(f['name']+'.NON_MATCHING' not in (new/'build/usa/mnsg.map').read_text(),'target still marked ASM')
    retail=work/'vmdual-retail.z64';subprocess.run([str(uv),'run','python','tools/rommy.py','compress','--input','build/usa/mnsg.z64','--output',str(retail),'--manifest','config/usa/rommy.yaml','--pad','--verify'],cwd=new,check=True,stdout=subprocess.DEVNULL)
    original_retail=(baseline/'config/usa/baserom.z64').read_bytes();require(len(original_retail)==16777216 and hashlib.sha1(original_retail).hexdigest()==RETAIL_SHA and retail.read_bytes()==original_retail,'retail ROM differs')
    require(sha((new/'src/script_vm.c').read_bytes())==MIXED_SHA,'native mixed source drift')
    proof.update(status='PASSED_G2_DUAL_REFERENCE_LOCAL',base_c=2317,accepted_c_after=2319,added_c=2,added_original_bytes=720,accepted_original_bytes_after=111008,remaining_assembly=5044,original_rom_sha1=ROM_SHA,full_rom_match=True,original_32MiB_ROM_bytes_exact=33554432,retail_rom_sha1=RETAIL_SHA,retail_rom_exact=True,original_16MiB_ROM_bytes_exact=16777216,predecessor_elf_sha256=PRIOR_ELF,candidate_elf_sha256=NEW_ELF,independent_prior_elf_sha256=sha(refs[0].read_bytes()),independent_shadow_elf_sha256=sha(refs[1].read_bytes()),original_asm_sha256=ORIG_ASM,original_data_sha256=ORIG_DATA,independent_prior_asm_sha256=PRIOR_ASM,independent_shadow_asm_sha256=SHADOW_ASM,mixed_source_sha256=MIXED_SHA,targets=[dict(x) for x in TARGETS],native_object_relocations_unmodified=True,negative_controls_rejected=audit['negative_controls_rejected'],compiler_quirk_outcome='EXISTING_QUIRK_REPRODUCED',gameplay='NOT_RUN')
    # Preserve the prior build and return the independently verified candidate
    # to the verifier's canonical scratch path for strict inventory.
    candidate.rename(work/'vmdual-predecessor');new.rename(candidate)
    return proof
