"""Private original-address integration experiment. No promotion from this alone."""
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
BATCH=ROOT/'research/promotion251_20261123'
MANIFEST_SHA='09c4568258a6a0d31efdef7ff1e43083ba434371c998da4a7f5d7f10a94c84ee'
FORMAT='goemon-usa-native151-post2165-v1'
from decomp.native_probe_helpers251 import get_original_splat_lines,check_exact,check_size
SHA={'usa':'6ea0ed71032ce08fc2745f412d84936382197494','japan_0':'6f8745fecc3a5e7d4918c7a73353eb0726116ded'}
BASE={'usa':2165,'japan_0':2428}
BASE_BYTES={'usa':100040,'japan_0':130268}
RELOCS={'usa':(82103,'f7f25e257c9bce27c00e756b85ca7bfa5774137925d5aba9a6626ba4693e5a97'),'japan_0':(80745,'43a133b21ac2b18d8e1d00f8c4e5718776b001a1f45c54e807dae12165e797c0')}
GLOBALS={'usa':26714,'japan_0':26393}

def sha(b):return hashlib.sha256(b).hexdigest()
def write(path,data):path.write_text(json.dumps(data,indent=2)+'\n')
def original(co,r):
    b=(co/f'config/{r}/baserom.decompressed.z64').read_bytes()
    assert len(b)==33554432 and hashlib.sha1(b).hexdigest()==SHA[r]
    return b

def rows(r):
    if sha((BATCH/'manifest.json').read_bytes())!=MANIFEST_SHA:raise ValueError('Native251 source ledger changed')
    allrows=json.loads((BATCH/'manifest.json').read_text()); a=[c for c in allrows if c['region']==r]
    assert len(a)==(151 if r=='usa' else 100)
    assert len({c['rom_offset'] for c in a})==len(a)
    return a

def runmake(co,r,ld,targets,log,uv="uv",jobs=4):
    # Use all currently linked C input files, not the other region's Splat-generated C.
    c=sorted(set(re.findall(r'build/'+r+r'/(src/[^\s()]+\.c)\.o\(',ld)))
    assert c
    override=co/f'build/{r}/promo251-files.mk';override.write_text('override C_FILES := '+' '.join(c)+'\n');cmd=['make','-f',str(override),'-f','Makefile','-j'+str(jobs),'VERSION='+r,'UV='+str(uv),*targets]
    with log.open('w') as f:
        subprocess.run(cmd,cwd=co,stdout=f,stderr=subprocess.STDOUT,check=True)

def plan(co,r,selected=None):
    rom=original(co,r); ldpath=co/f'.splat/{r}/mnsg.ld';ld=ldpath.read_text()
    allrows=[c for c in rows(r) if selected is None or c['name'] in selected]
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
            assert sha((BATCH/c['negative_source']).read_bytes())==c['negative_sha256'],name
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

def stage(co,r,selected=None):
    rom,ldpath,ld,cache,groups,blocked=plan(co,r,selected)
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
                    path=f'asm/{r}/promo251_{i:03}_{j:03}.s';parts.append(('asm',path,(header+frag).encode(),cur,off,None))
                elif re.search(r'/\* [0-9A-Fa-f]{5,8} [0-9A-Fa-f]{8} [0-9A-Fa-f]{8} \*/',frag):raise ValueError('Unowned ASM before candidate')
                path=f'src/promo251/{c["name"]}.c';parts.append(('c',path,(BATCH/c['source']).read_bytes(),off,off+size,c))
                cur=off+size;cursor=m.end()
            if cur<end_real:
                frag=raw[cursor:]
                if jp55.word_span(frag)!=(cur,end_real):raise ValueError('Noncontiguous final ASM span')
                path=f'asm/{r}/promo251_{i:03}_tail.s';parts.append(('asm',path,(header+frag).encode(),cur,end_real,None))
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
    write(co/f'build/{r}/promo251-stage.json',doc)
    return doc

def compile_pack(co,r,stage,pristine,uv="uv",jobs=4):
    rom=original(co,r);ld=(co/f'.splat/{r}/mnsg.ld').read_text()
    targets=[f'build/{r}/{c["staged_path"]}.o' for c in stage['functions']]+[f'build/{r}/{a["path"]}.o' for a in stage['fragments']]
    assert targets
    ledger=(ROOT/'COMPILER_QUIRKS.md').read_bytes();assert b'NO_NEW_COMPILER_FINDING' in ledger
    runmake(co,r,ld,targets,co/f'build/{r}/promo251-compile.log',uv,jobs)
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
            recs.append({'name':name,'compiler_quirk_outcome':'NO_NEW_COMPILER_FINDING','ledger_sha256':sha(ledger),'source_sha256':c['source_sha256'],'relocations':actual,'pack':rec})
        except (ValueError,AssertionError,KeyError) as exc:failures.append({'name':name,'owner':c['active_owner'],'reason':str(exc),'compiler_quirk_outcome':'NO_NEW_COMPILER_FINDING'})
    for a in stage['fragments']:
        p=co/f'build/{r}/{a["path"]}.o';length=a['end']-a['start']
        try:
            if a['suffix']=='.text.archive61':splice._trim_archive_asm(p,length)
            else:cross._trim_object(p,length,rom[a['start']:a['end']])
        except (ValueError,AssertionError,KeyError) as exc:failures.append({'owner':a['owner'],'fragment':a['path'],'reason':str(exc),'compiler_quirk_outcome':'NO_NEW_COMPILER_FINDING'})
    result={'positive_full_flags':len(recs),'records':recs,'failures':failures};write(co/f'build/{r}/promo251-compile.json',result);return result

def link_and_check(co,r,stage,base,uv="uv",jobs=4):
    rom=original(co,r);ld=(co/f'.splat/{r}/mnsg.ld').read_text();bd=co/f'build/{r}';old=base if base.is_file() else base/f'build/{r}/mnsg.elf';new=bd/'mnsg.elf'
    for p in (new,bd/'mnsg.z64'):
        if p.exists():p.unlink()
    runmake(co,r,ld,[f'build/{r}/mnsg.z64'],bd/'promo251-link.log',uv,jobs)
    if r=='usa':
        # Previously reviewed short72 inline label restoration; exact predecessor guard.
        short72.restore_original_abs_label_type(new,old)
    b=(bd/'mnsg.z64').read_bytes(); rom_ok=(b==rom)
    a0=cross._funcs(old);a1=cross._funcs(new)
    t0,n0,h0=glitch.all_semantic_relocations(old);t1,n1,h1=glitch.all_semantic_relocations(new)
    g0=opening.stable_globals(old);g1=opening.stable_globals(new)
    old_names=cright.c_identities(old);new_names=cright.c_identities(new); targets={c['name'] for c in stage['functions']}
    d={'region':r,'rom_exact':rom_ok,'rom_sha1':hashlib.sha1(b).hexdigest(),'first_rom_difference':next((i for i,(a,b) in enumerate(zip(rom,b)) if a!=b),None),'rom_size':len(b),'func_exact':a0==a1 and sum(a0.values())==7376,'func_removed':list((a0-a1).items())[:50],'func_added':list((a1-a0).items())[:50], 'relocs_exact':t0==t1 and (n0,h0)==RELOCS[r], 'relocs_count':n1,'relocs_sha256':h1,'relocs_removed':list((t0-t1).items())[:50],'relocs_added':list((t1-t0).items())[:50], 'globals_exact':g0==g1 and sum(g0.values())==GLOBALS[r], 'globals_removed':list((g0-g1).items())[:50],'globals_added':list((g1-g0).items())[:50], 'ownership_exact':new_names-old_names==targets and not old_names-new_names and len(old_names)==BASE[r]+(13 if r=='usa' else 0),'new_ownership':len(new_names-old_names),'ownership_missing':sorted(targets-(new_names-old_names)),'ownership_unexpected':sorted((new_names-old_names)-targets),'ownership_regressed':sorted(old_names-new_names)}
    write(bd/'promo251-link.json',d);return d


USA_ABS_FIXES=[('func_08001398_71CE18', 'D_8003090', 4), ('func_08001618_71D098', 'D_8003090', 4), ('func_08000284_71BD04', 'D_8003DB0', 4), ('func_08001908_71D388', 'D_8005B10', 4), ('func_801CCDCC_65FC7C', 'D_801E9914_67C7C4', 4), ('func_080016D4_71D154', 'D_8001E00', 4), ('func_080016D4_71D154', 'D_8003E00', 4), ('func_08001398_71CE18', 'D_8004090', 4), ('func_08001618_71D098', 'D_8004090', 4), ('func_801CCDCC_65FC7C', 'D_801E9930_67C7E0', 4), ('func_8020F13C_66E0EC', 'D_3ADCA', 1), ('func_08001B7C_71D5FC', 'D_80031F0', 4), ('func_801CB56C_63A3BC', 'D_3ADDF', 1), ('func_08001B7C_71D5FC', 'D_80041F0', 4), ('func_08001B7C_71D5FC', 'D_80021F0', 4), ('func_08000284_71BD04', 'D_8002DB0', 4), ('func_08001908_71D388', 'D_8006B10', 4), ('func_08001790_71D210', 'D_8004010', 4), ('func_080001C8_71BC48', 'D_80025B0', 4), ('func_08001398_71CE18', 'D_8002090', 4), ('func_08001618_71D098', 'D_8002090', 4), ('func_08001790_71D210', 'D_8003010', 4), ('func_08001908_71D388', 'D_8003B10', 4), ('func_080001C8_71BC48', 'D_80035B0', 4), ('func_080016D4_71D154', 'D_8002E00', 4), ('func_080001C8_71BC48', 'D_80045B0', 4), ('func_08000284_71BD04', 'D_8001DB0', 4), ('func_08001790_71D210', 'D_8002010', 4)]

def validate_predecessor(manifest,rom=None):
    if manifest.get('usa_native151_promotion')!={'format':FORMAT}:raise ValueError('Unreviewed native151 stage')
    prior=verify.claimed_functions({k:v for k,v in manifest.items() if k!='usa_native151_promotion'})
    if (len(prior),sum(f['size'] for f in prior))!=(2165,100040):raise ValueError('Native151 requires exact 2165 predecessor')
    fs=rows('usa'); names={x['name'] for x in prior}; spans=[(x['rom_offset'],x['rom_offset']+x['size']) for x in prior];ranges=[]
    if len({x['name'] for x in fs})!=151 or sum(x['original_bytes'] for x in fs)!=9808:raise ValueError('Native151 count/extent')
    for c in fs:
        off=c['rom_offset'];end=off+c['original_bytes'];name=c['name']
        if name in names or any(off<b and a<end for a,b in spans):raise ValueError('Native151 duplicates predecessor '+name)
        if sha((BATCH/c['source']).read_bytes())!=c['source_sha256'] or sha((BATCH/c['negative_source']).read_bytes())!=c['negative_sha256']:raise ValueError('Native151 source changed '+name)
        if rom is not None and sha(rom[off:end])!=c['code_sha256']:raise ValueError('Native151 original bytes changed '+name)
        ranges.append((off,end))
    if any(a[1]>b[0] for a,b in zip(sorted(ranges),sorted(ranges)[1:])):raise ValueError('Native151 overlapping targets')
    return fs

def restore_undefined_type(path,name,expected_size,prior_globals):
    """Existing ABS NOTYPE/IDO OBJECT quirk, bounded to reviewed symbol + size.
    Only an undefined C symbol st_info byte changes; code/relocs unchanged."""
    if sum(n for k,n in prior_globals.items() if k[1:]==('0','NOTYPE','GLOBAL','DEFAULT','ABS',name))!=1:raise ValueError('Original ABS identity missing '+name)
    before=path.read_bytes();buf=bytearray(before);sec=opening.elf_sections(before);tab=sec['.symtab'];strings=sec['.strtab'];assert tab['entsize']==16
    found=[]
    for i in range(tab['size']//16):
        at=tab['offset']+i*16;off=struct.unpack_from('>I',buf,at)[0];start=strings['offset']+off
        if buf[start:buf.index(0,start)].decode('ascii')!=name:continue
        if (struct.unpack_from('>II',buf,at+4),buf[at+12],buf[at+13],struct.unpack_from('>H',buf,at+14)[0])!=((0,expected_size),0x11,0,0):raise ValueError('Unexpected undefined C symbol '+name)
        found.append(at+12)
    if len(found)!=1:raise ValueError('Undefined symbol identity not unique '+name)
    at=found[0];buf[at]=0x10
    if [i for i,(a,b) in enumerate(zip(before,buf)) if a!=b]!=[at]:raise ValueError('Forbidden metadata change')
    for part in ('.text','.rel.text'):
        e=sec[part];i=e['offset'];j=i+e['size'];assert before[i:j]==buf[i:j]
    path.write_bytes(buf)
    return {'symbol':name,'undefined_size':expected_size,'st_info_bytes_changed':1,'code_and_relocations_unchanged':True,'source_object_sha256':sha(before),'original_provenance_object_sha256':sha(buf),'compiler_outcome':'EXISTING_QUIRK_REPRODUCED'}

def restore_inline_usa(path,prior):
    name='D_08001710_71D190';identity=('08001710','0','FUNC','GLOBAL','DEFAULT','ABS',name)
    before=path.read_bytes();buf=bytearray(before);sec=opening.elf_sections(before);tab=sec['.symtab'];strings=sec['.strtab'];assert tab['entsize']==16
    if opening.stable_globals(prior)[identity]!=1:raise ValueError('Unknown original inline label')
    found=[]
    for i in range(tab['size']//16):
        at=tab['offset']+i*16;off=struct.unpack_from('>I',buf,at)[0];start=strings['offset']+off
        if buf[start:buf.index(0,start)].decode('ascii')!=name:continue
        if (struct.unpack_from('>II',buf,at+4),buf[at+12],buf[at+13],struct.unpack_from('>H',buf,at+14)[0])!=((0x08001710,0),0x10,0,0xfff1):raise ValueError('Unexpected inline label metadata')
        found.append(at+12)
    if len(found)!=1:raise ValueError('Original inline symbol not unique')
    at=found[0];buf[at]=0x12
    if [i for i,(a,b) in enumerate(zip(before,buf)) if a!=b]!=[at]:raise ValueError('Forbidden inline metadata change')
    path.write_bytes(buf)
    return {'symbol':name,'metadata_byte_offset':at,'pre_sha256':sha(before),'post_sha256':sha(buf),'compiler_quirk_outcome':'EXISTING_QUIRK_REPRODUCED'}

def stage_mixed_usa(co,doc,uv,jobs):
    name='func_80023840_24440';c=next(x for x in rows('usa') if x['name']==name);f=co/'src/return_zero.c';old=f.read_bytes()
    if sha(old)!='a24dc36c3070d83e01d0e4e752638b5861ff1d885cc244194c711fb941ac1488':raise ValueError('Original mixed C owner changed')
    src=(BATCH/c['source']).read_text();src=src[src.index('s32 osPfsIsPlug'):].replace('M2C_UNK','s32');needle='#pragma GLOBAL_ASM("asm/usa/nonmatchings/return_zero/func_80023840_24440.s")'
    text=old.decode();assert text.count(needle)==1;new=text.replace(needle,src.rstrip(),1).encode()
    if sha(new)!='13266e90f8320fba00d33e8281b3f5b766cb159854964ddcd5a9f0c735049273':raise ValueError('Unreviewed mixed C owner construction')
    f.write_bytes(new);ledger=(ROOT/'COMPILER_QUIRKS.md').read_bytes();ld=(co/'.splat/usa/mnsg.ld').read_text()
    runmake(co,'usa',ld,['build/usa/src/return_zero.c.o'],co/'build/usa/promo251-mixed.log',uv,jobs)
    doc['functions'].append({**c,'staged_path':'src/return_zero.c','active_owner':'src/return_zero.c','section':'main','integrated_source_sha256':sha(new)})
    doc['blocked']=[x for x in doc['blocked'] if x['name']!=name];write(co/'build/usa/promo251-stage.json',doc)
    return {'name':name,'source_sha256':c['source_sha256'],'mixed_unit_sha256':sha(new),'compiler_quirk_outcome':'NO_NEW_COMPILER_FINDING','ledger_sha256':sha(ledger)}

def apply_usa(candidate,baseline,work,uv,jobs):
    co=Path(candidate);base=Path(baseline);work=Path(work);prior=work/'accepted2165-before-native151.elf';shutil.copyfile(co/'build/usa/mnsg.elf',prior)
    rom=original(co,'usa');assert (co/'build/usa/mnsg.z64').read_bytes()==rom
    doc=stage(co,'usa');assert len(doc['functions'])==150 and [x['name'] for x in doc['blocked']]==['func_80023840_24440']
    compiled=compile_pack(co,'usa',doc,base,uv,jobs)
    if compiled['positive_full_flags']!=150 or compiled['failures']:raise ValueError('USA native151 object integration failed')
    g=opening.stable_globals(prior);fixes=[]
    for fn,sym,size in USA_ABS_FIXES:
        c=next(x for x in doc['functions'] if x['name']==fn);obj=co/'build/usa'/(c['staged_path']+'.o');fixes.append({'function':fn,**restore_undefined_type(obj,sym,size,g)})
    mixed=stage_mixed_usa(co,doc,uv,jobs)
    audit=link_and_check(co,'usa',doc,prior,uv,jobs)
    if not all(audit[k] for k in ('rom_exact','func_exact','relocs_exact','ownership_exact')) or audit['new_ownership']!=151:raise ValueError('Native151 linked identity mismatch')
    # The sole known zero-size ABS annotation is not a positive-sized function.
    name='D_08001710_71D190'
    if audit['globals_removed']!=[[['08001710','0','FUNC','GLOBAL','DEFAULT','ABS',name],1]] and audit['globals_removed']!=[(('08001710','0','FUNC','GLOBAL','DEFAULT','ABS',name),1)]:raise ValueError('Unexpected new stable symbol mismatch')
    new=co/'build/usa/mnsg.elf';fix=restore_inline_usa(new,prior)
    if opening.stable_globals(prior)!=opening.stable_globals(new) or cross._funcs(prior)!=cross._funcs(new) or glitch.all_semantic_relocations(prior)!=glitch.all_semantic_relocations(new):raise ValueError('Stable ELF identity mismatch after guarded metadata correction')
    return {'status':'PASSED_G2_LOCAL','base_c':2165,'accepted_c_after':2316,'added_c':151,'added_original_bytes':9808,'accepted_original_bytes_after':109848,'remaining_assembly':5047,'full_rom_match':True,'original_rom_sha1':SHA['usa'],'original_32MiB_ROM_bytes_exact':33554432,'positive_elf_function_identities_exact':7376,'semantic_relocations_exact':82103,'semantic_relocation_sha256':RELOCS['usa'][1],'stable_global_symbols_exact':26714,'source_manifest_sha256':MANIFEST_SHA,'original_elf_sha256':sha((base/'build/usa/mnsg.elf').read_bytes()),'predecessor_elf_sha256':sha(prior.read_bytes()),'candidate_elf_sha256':sha(new.read_bytes()),'native_object_count':150,'mixed_unit':mixed,'abs_metadata_fixes':fixes,'inline_metadata_fix':fix,'ownership_exact':True,'compiler_quirk_outcome':'EXISTING_QUIRK_REPRODUCED'}

JP_ABS_FIXES=[('func_80200180_5BC150','D_3AE23',1),('func_80213F2C_672D9C','D_3ADCA',1),('func_801D0C9C_63F18C','D_3ADDF',1),('func_80011518_12118','D_8002664',1)]

def verify_japan_rows(fs):
    if len(fs)!=100 or len({x['name'] for x in fs})!=100 or sum(x['original_bytes'] for x in fs)!=7136:raise ValueError('Native100 JP source extent mismatch')
    ranges=[]
    for c in fs:
        if sha((BATCH/c['source']).read_bytes())!=c['source_sha256'] or sha((BATCH/c['negative_source']).read_bytes())!=c['negative_sha256']:raise ValueError('JP native source hash changed '+c['name'])
        ranges.append((c['rom_offset'],c['rom_offset']+c['original_bytes']))
    if any(a[1]>b[0] for a,b in zip(sorted(ranges),sorted(ranges)[1:])):raise ValueError('JP original ranges overlap')

def apply_japan(candidate,pristine,work,uv,jobs=4):
    co=Path(candidate);work=Path(work);prior=work/'accepted2428-before-native100.elf';work.mkdir(exist_ok=True,parents=True)
    rom=original(co,'japan_0');assert (co/'build/japan_0/mnsg.z64').read_bytes()==rom
    shutil.copyfile(co/'build/japan_0/mnsg.elf',prior);assert len(cright.c_identities(prior))==2428
    fs=rows('japan_0');verify_japan_rows(fs);assert not ({x['name'] for x in fs}&cright.c_identities(prior))
    doc=stage(co,'japan_0');assert len(doc['functions'])==100 and not doc['blocked']
    compiled=compile_pack(co,'japan_0',doc,Path(pristine),uv,jobs)
    if compiled['positive_full_flags']!=100 or compiled['failures']:raise ValueError('JP native100 object integration failed')
    g=opening.stable_globals(prior);fixes=[]
    for fn,sym,size in JP_ABS_FIXES:
        c=next(x for x in doc['functions'] if x['name']==fn);obj=co/'build/japan_0'/(c['staged_path']+'.o');fixes.append({'function':fn,**restore_undefined_type(obj,sym,size,g)})
    audit=link_and_check(co,'japan_0',doc,prior,uv,jobs)
    if not all(audit[k] for k in ('rom_exact','func_exact','relocs_exact','globals_exact','ownership_exact')) or audit['new_ownership']!=100:raise ValueError('Native100 JP complete original ELF/ROM identity failed')
    return {'status':'PASSED_G2_LOCAL','region':'japan_0','before_C':2428,'after_C':2528,'added_C':100,'added_bytes':7136,'original_bytes_after':137404,'asm_remaining':4848,'rom_bytes':33554432,'rom_sha1':SHA['japan_0'],'elf_identities_exact':7376,'semantic_relocations_exact':80745,'semantic_relocations_sha256':RELOCS['japan_0'][1],'stable_global_symbol_identities_exact':26393,'source_manifest_sha256':MANIFEST_SHA,'predecessor_elf_sha256':sha(prior.read_bytes()),'candidate_elf_sha256':sha((co/'build/japan_0/mnsg.elf').read_bytes()),'abs_metadata_fixes':fixes,'ownership_exact':True,'new_C_names':sorted(x['name'] for x in fs)}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--region',choices=['usa','japan_0'],required=True);parser.add_argument('--checkout',type=Path,required=True);parser.add_argument('--pristine',type=Path,required=True);parser.add_argument('--work',type=Path,required=True);parser.add_argument('--uv',default='uv');parser.add_argument('--jobs',type=int,default=4);a=parser.parse_args()
    result=(apply_usa if a.region=='usa' else apply_japan)(a.checkout,a.pristine,a.work,a.uv,a.jobs);print(json.dumps(result,indent=2))
