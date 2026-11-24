"""Additive native USA C-Right4 original-ROM verification after canonical 2319-C."""
from pathlib import Path
from collections import defaultdict,Counter
import argparse,hashlib,json,os,re,shutil,struct,subprocess,sys
from decomp import overlay_crossregion47 as cross
from decomp import overlay_isolated233 as splice
from decomp import japan_jp55_promotion as jp55
from decomp import glitch_g2_promotion as glitch
from decomp import usa_opening_new2_promotion as opening
from decomp import usa_short72_promotion as short72
from decomp import japan_cright_promotion as cright
from decomp import inventory
from decomp import verify
ROOT=Path(__file__).resolve().parent
BATCH=ROOT/'research/cright_promotion_checkpoint_20261124'
MANIFEST_SHA='72901ff559c3511062e0c85fb0d1c98800e9d441c7036527a8302bb5e697180e'
KEY='usa_cright4_promotion'
FORMAT='goemon-usa-cright4-post2319-v1'
from decomp.native_probe_helpers251 import get_original_splat_lines,check_exact,check_size
SHA={'usa':'6ea0ed71032ce08fc2745f412d84936382197494','japan_0':'6f8745fecc3a5e7d4918c7a73353eb0726116ded'}

def sha(b):return hashlib.sha256(b).hexdigest()
def write(path,data):path.write_text(json.dumps(data,indent=2)+'\n')
def original(co,r):
    b=(co/f'config/{r}/baserom.decompressed.z64').read_bytes()
    assert len(b)==33554432 and hashlib.sha1(b).hexdigest()==SHA[r]
    return b

def rows(r):
    manifest=BATCH/'usa_manifest.json'
    assert sha(manifest.read_bytes())==MANIFEST_SHA
    a=[c for c in json.loads(manifest.read_text()) if c['region']==r]
    assert r=='usa' and len(a)==4
    assert all(c['status']=='PASSED_ISOLATED_NATIVE' for c in a)
    assert len({c['rom_offset'] for c in a})==len(a)
    return a

def runmake(co,r,ld,targets,log,uv="uv",jobs=4):
    # Use all currently linked C input files, not the other region's Splat-generated C.
    c=sorted(set(re.findall(r'build/'+r+r'/(src/[^\s()]+\.c)\.o\(',ld)))
    assert c
    override=co/f'build/{r}/cright10-files.mk';override.write_text('override C_FILES := '+' '.join(c)+'\n');cmd=['make','-f',str(override),'-f','Makefile','-j'+str(jobs),'VERSION='+r,'UV='+str(uv),*targets]
    with log.open('w') as f:
        subprocess.run(cmd,cwd=co,stdout=f,stderr=subprocess.STDOUT,check=True)

def plan(co,r,selected=None,*,candidates=None):
    rom=original(co,r); ldpath=co/f'.splat/{r}/mnsg.ld';ld=ldpath.read_text()
    allrows=[c for c in (rows(r) if candidates is None else candidates) if selected is None or c['name'] in selected]
    if any(c['region']!=r for c in allrows):raise ValueError('Wrong regional candidates')
    target={c['name']:c for c in allrows}; owners={}; cache={}; sec=None
    active=[]
    for line in ld.splitlines():
        sm=re.match(r'^\s*\.(\w+)\s+0x[0-9a-fA-F]+\s*:\s*AT\(',line)
        if sm:sec=sm[1]
        for m in re.finditer(r'build/'+r+r'/(asm/'+r+r'/[^\s()]+\.s)\.o\((\.text(?:\.archive61)?)\);',line):active.append((m[1],m[2],sec))
    blocked=[]
    for owner,suffix,section in active:
        raw=(co/owner).read_text();ms=list(jp55.BLOCK.finditer(raw)); hit=[m for m in ms if m['name'] in target]
        if not hit:continue
        cache[owner]=(raw,ms,suffix,section)
        for m in hit:
            name=m['name'];c=target[name];off=c['rom_offset'];size=c['original_bytes']
            if name in owners:raise ValueError('duplicate active owner '+name)
            assert int(m['size'],16)==size and jp55.word_span(raw[m.start():m.end()])==(off,off+size),name
            assert sha(rom[off:off+size])==c['code_sha256'] and sha((BATCH/c['source']).read_bytes())==c['source_sha256'],name
            owners[name]=(owner,m)
    for name in sorted(set(target)-set(owners)):
        matches=[]
        for p in (co/'src').rglob('*.c'):
            text=p.read_text(errors='replace')
            if re.search(r'GLOBAL_ASM\("[^"\n]*/'+re.escape(name)+r'\.s"\)',text):matches.append(str(p.relative_to(co)))
        blocked.append({'name':name,'reason':'MIXED_C_OWNER' if matches else 'NO_ACTIVE_STANDALONE_OWNER','mixed_owners':matches})
    groups=defaultdict(list)
    for name,(own,m) in owners.items():groups[own].append(target[name])
    return rom,ldpath,ld,cache,groups,blocked

def stage(co,r,selected=None,*,candidates=None):
    rom,ldpath,ld,cache,groups,blocked=plan(co,r,selected,candidates=candidates)
    out=[];frags=[];parent_records=[];sections=set()
    for i,(own,rs) in enumerate(sorted(groups.items())):
        raw,ms,suffix,section=cache[own];rs.sort(key=lambda c:c['rom_offset']);begin=jp55.word_span(raw[ms[0].start():ms[0].end()])[0]
        end=jp55.word_span(raw[ms[-1].start():ms[-1].end()])[1]
        old_obj=co/f'build/{r}/{own}.o'
        if not old_obj.exists():raise ValueError('Missing prior linked object '+own)
        # Verify all non-text bytes of original parent are empty.
        try:
            glitch.check_nontext(old_obj)
            secs=opening.elf_sections(old_obj.read_bytes()); s=secs[suffix]
            end_real=begin+s['size']; header=raw[:ms[0].start()]
            if re.search(r'/\* [0-9A-Fa-f]{5,8} [0-9A-Fa-f]{8} [0-9A-Fa-f]{8} \*/',header):raise ValueError('Non-function text in parent prefix')
            if end_real<end:raise ValueError('Owner span beyond prior ELF object')
            if end_real>end:
                if jp55.word_span(raw[ms[-1].end():])!=(end,end_real) or any(rom[end:end_real]):raise ValueError('Unexpected prior text suffix')
            if section is None:raise ValueError('Unknown original section')
            cur=begin;cursor=ms[0].start();byname={m['name']:m for m in ms};parts=[]
            for j,c in enumerate(rs):
                m=byname[c['name']];off=c['rom_offset'];size=c['original_bytes']
                if off<cur or m.start()<cursor:raise ValueError('overlapping owner extent')
                frag=raw[cursor:m.start()]
                if off>cur:
                    if jp55.word_span(frag)!=(cur,off):raise ValueError('Noncontiguous leading ASM span')
                    path=f'asm/{r}/cright10_{i:03}_{j:03}.s';parts.append(('asm',path,(header+frag).encode(),cur,off,None))
                elif re.search(r'/\* [0-9A-Fa-f]{5,8} [0-9A-Fa-f]{8} [0-9A-Fa-f]{8} \*/',frag):raise ValueError('Unowned ASM before candidate')
                path=f'src/cright10/{c["name"]}.c';parts.append(('c',path,(BATCH/c['source']).read_bytes(),off,off+size,c))
                cur=off+size;cursor=m.end()
            if cur<end_real:
                frag=raw[cursor:]
                if jp55.word_span(frag)!=(cur,end_real):raise ValueError('Noncontiguous final ASM span')
                path=f'asm/{r}/cright10_{i:03}_tail.s';parts.append(('asm',path,(header+frag).encode(),cur,end_real,None))
            assert parts[0][3]==begin and parts[-1][4]==end_real and all(a[4]==b[3] for a,b in zip(parts,parts[1:]))
            orig=f'build/{r}/{own}.o';needle=f'{orig}({suffix});'
            if ld.count(needle)!=1:raise ValueError('Missing unique original input section')
            newld=ld.replace(needle,'\n'.join(f'        build/{r}/{path}.o({suffix if kind=="asm" else ".text"});' for kind,path,*_ in parts),1)
            for sec in ('.data','.rodata','.bss','.sdata','.sbss'):
                q=f'{orig}({sec});'
                if newld.count(q)>1:raise ValueError('Duplicate nontext input')
                newld=newld.replace(q,'')
            if orig+'(' in newld:raise ValueError('Unexpected other original section')
        except (ValueError,AssertionError,KeyError) as exc:
            blocked.extend({'name':c['name'],'owner':own,'reason':str(exc)} for c in rs);continue
        for kind,path,data,a,b,c in parts:
            dest=co/path;assert not dest.exists(),path;dest.parent.mkdir(exist_ok=True,parents=True);dest.write_bytes(data)
            if kind=='c':out.append({**c,'staged_path':path,'active_owner':own,'section':section})
            else:frags.append({'path':path,'start':a,'end':b,'suffix':suffix,'owner':own})
        ld=newld;sections.add(section);parent_records.append({'owner':own,'section':section,'suffix':suffix,'names':[c['name'] for c in rs]})
    for sec in sections:
        ld,n=re.subn(r'(?m)^(\s*\.'+re.escape(sec)+r'\s+0x[0-9A-Fa-f]+\s*:\s*AT\([^)]+\)) SUBALIGN\(16\)',r'\1 SUBALIGN(4)',ld)
        assert n<=1
    ldpath.write_text(ld)
    doc={'region':r,'functions':out,'fragments':frags,'parents':parent_records,'blocked':blocked,'linker_sha256':sha(ld.encode())}
    write(co/f'build/{r}/cright10-stage.json',doc)
    return doc

def compile_pack(co,r,stage,pristine,uv="uv",jobs=4):
    rom=original(co,r);ld=(co/f'.splat/{r}/mnsg.ld').read_text()
    targets=[f'build/{r}/{c["staged_path"]}.o' for c in stage['functions']]+[f'build/{r}/{a["path"]}.o' for a in stage['fragments']]
    assert targets
    ledger=(ROOT/'COMPILER_QUIRKS.md').read_bytes();assert b'NO_NEW_COMPILER_FINDING' in ledger
    runmake(co,r,ld,targets,co/f'build/{r}/cright10-compile.log',uv,jobs)
    failures=[];recs=[]
    for c in stage['functions']:
        name=c['name'];off=c['rom_offset'];z=c['original_bytes'];p=co/f'build/{r}/{c["staged_path"]}.o';orig=rom[off:off+z]
        try:
            assert sha((co/c['staged_path']).read_bytes())==c['source_sha256']
            obj=opening.elf_sections(p.read_bytes())['.text'];b=p.read_bytes()[obj['offset']:obj['offset']+obj['size']]
            lines=get_original_splat_lines(Path(pristine)/f'asm/{r}'/c['owner'],name,off,c['vma'],z,orig)
            rel=subprocess.check_output(['readelf','-rW',str(p)],text=True);sym=subprocess.check_output(['readelf','-sW',str(p)],text=True)
            exact,reason,diff,actual,expected=check_exact(b,orig,rel,lines,z);size_ok,_=check_size(sym,name,z)
            if not exact or not size_ok:raise ValueError(f'{reason} at {diff}; extent={size_ok}')
            glitch.check_nontext(p)
            rec=cross._trim_object(p,z,orig)
            recs.append({'name':name,'compiler_quirk_outcome':c['compiler_quirk_outcome'],'ledger_sha256':sha(ledger),'source_sha256':c['source_sha256'],'relocations':actual,'pack':rec})
        except (ValueError,AssertionError,KeyError) as exc:failures.append({'name':name,'owner':c['active_owner'],'reason':str(exc),'compiler_quirk_outcome':'NO_NEW_COMPILER_FINDING'})
    for a in stage['fragments']:
        p=co/f'build/{r}/{a["path"]}.o';length=a['end']-a['start']
        try:
            if a['suffix']=='.text.archive61':splice._trim_archive_asm(p,length)
            else:cross._trim_object(p,length,rom[a['start']:a['end']])
        except (ValueError,AssertionError,KeyError) as exc:failures.append({'owner':a['owner'],'fragment':a['path'],'reason':str(exc),'compiler_quirk_outcome':'NO_NEW_COMPILER_FINDING'})
    result={'positive_full_flags':len(recs),'records':recs,'failures':failures};write(co/f'build/{r}/cright10-compile.json',result);return result

from decomp import usa_script_vm_dual_reference as vmdual, native251_promotion as native251
RETAIL_SHA='df8083a54296b8c151917c5333e1c85f014a2a66'
NEW_ELF='8cc24cf708723517dfdc2efcd4484dc8695961abfaecf0649bee81e7087d1ade'
COMPILER_SHA='76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0'

def require(condition,message):
    if not condition:raise ValueError('USA C-Right4: '+message)

def claims():
    return [{'name':f['name'],'rom_offset':f['rom_offset'],'vma':f['vma'],'size':f['original_bytes']} for f in rows('usa')]

def validate_predecessor(manifest,rom=None):
    require(manifest.get(KEY)=={'format':FORMAT},'unreviewed stage')
    require(manifest.get(vmdual.KEY)=={'format':vmdual.FORMAT},'missing dual-reference predecessor')
    old=verify.claimed_functions({k:v for k,v in manifest.items() if k!=KEY})
    require((len(old),sum(f['size'] for f in old))==(2319,111008),'wrong predecessor count')
    fs=rows('usa');require(sum(f['original_bytes'] for f in fs)==728,'wrong new instruction extent')
    for f in fs:
        name=f['name'];off=f['rom_offset'];end=off+f['original_bytes'];require(not any(x['name']==name or x['rom_offset']<end and off<x['rom_offset']+x['size'] for x in old),'duplicate original owner '+name)
        require(sha((BATCH/f['source']).read_bytes())==f['source_sha256'],'native source drift '+name)
        if rom is not None:require(len(rom)==33554432 and hashlib.sha1(rom).hexdigest()==SHA['usa'] and sha(rom[off:end])==f['code_sha256'],'wrong original ROM/code '+name)
    require(sha((BATCH/'negative_controls/func_8020D724_5C8BF4.c').read_bytes())=='ff3cacfdc23c61618c5a5147367b490bea4700d0cd1e31fad923c47954208146','initializer negative control drift')
    return old

def source_path(f):return (BATCH/f['source']).relative_to(ROOT).as_posix()

def apply_usa(candidate,baseline,work,uv,jobs):
    co,base,work=map(Path,(candidate,baseline,work));rom=original(co,'usa');bd=co/'build/usa';new=bd/'mnsg.elf';prior=work/'accepted2319-before-cright4.elf';require(not prior.exists(),'predecessor snapshot collision');shutil.copyfile(new,prior)
    require(sha(prior.read_bytes())==vmdual.NEW_ELF and (bd/'mnsg.z64').read_bytes()==rom and (base/'build/usa/mnsg.z64').read_bytes()==rom,'wrong canonical predecessor or pristine ROM')
    require(sha((co/'tools/ido-5.3/cc').read_bytes())==COMPILER_SHA,'wrong native IDO')
    names0=cright.c_identities(prior);require(len(names0)==2332,'predecessor C ownership drift')
    targets=rows('usa');d=stage(co,'usa');require(len(d['functions'])==4 and not d['blocked'],'active original ownership mismatch')
    compiled=compile_pack(co,'usa',d,base,uv,jobs);require(compiled['positive_full_flags']==4 and not compiled['failures'],'native full-flags object proof failed')
    g0=opening.stable_globals(prior);fix=native251.restore_undefined_type(bd/'src/cright10/func_8020D6BC_5C8B8C.c.o','D_3B03C',0,g0)
    new.unlink();(bd/'mnsg.z64').unlink();runmake(co,'usa',(co/'.splat/usa/mnsg.ld').read_text(),['build/usa/mnsg.z64'],bd/'cright10-metadata-relink.log',uv,jobs)
    fixes=[fix,short72.restore_original_abs_label_type(new,prior),native251.restore_inline_usa(new,prior)]
    require((bd/'mnsg.z64').read_bytes()==rom,'full expanded ROM differs')
    funcs=cross._funcs(prior);require(funcs==cross._funcs(new) and sum(funcs.values())==7376,'positive FUNC identities changed')
    rel0=glitch.all_semantic_relocations(prior);rel1=glitch.all_semantic_relocations(new);require(rel0==rel1 and rel1[1:]==(82102,vmdual.NEW_RELOC),'entire semantic relocation multiset differs')
    require(g0==opening.stable_globals(new) and sum(g0.values())==26714,'stable global identity changed')
    names=cright.c_identities(new);require(names-names0=={f['name'] for f in targets} and not names0-names,'new C source ownership differs')
    require(sha(new.read_bytes())==NEW_ELF,'candidate ELF fingerprint drift')
    retail=work/'cright4-retail.z64';subprocess.run([str(uv),'run','python','tools/rommy.py','compress','--input','build/usa/mnsg.z64','--output',str(retail),'--manifest','config/usa/rommy.yaml','--pad','--verify'],cwd=co,check=True,stdout=subprocess.DEVNULL)
    rb=(base/'config/usa/baserom.z64').read_bytes();require(len(rb)==16777216 and hashlib.sha1(rb).hexdigest()==RETAIL_SHA and retail.read_bytes()==rb,'full retail ROM differs')
    return {'status':'PASSED_G2_LOCAL','base_c':2319,'accepted_c_after':2323,'added_c':4,'added_original_bytes':728,'accepted_original_bytes_after':111736,'remaining_assembly':5040,'full_rom_match':True,'original_32MiB_ROM_bytes_exact':33554432,'original_rom_sha1':SHA['usa'],'retail_rom_exact':True,'original_16MiB_ROM_bytes_exact':16777216,'retail_rom_sha1':RETAIL_SHA,'positive_elf_function_identities_exact':7376,'semantic_relocations_exact':82102,'semantic_relocation_sha256':rel1[2],'stable_global_symbols_exact':26714,'predecessor_elf_sha256':vmdual.NEW_ELF,'candidate_elf_sha256':NEW_ELF,'source_manifest_sha256':MANIFEST_SHA,'guarded_metadata_corrections':fixes,'new_c_names':sorted(names-names0),'ownership_exact':True,'compiler_quirk_outcome':'EXISTING_QUIRK_REPRODUCED','gameplay':'NOT_RUN'}
