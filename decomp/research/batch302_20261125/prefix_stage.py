"""Owner split trial with authenticated original zero-prefix retention. No gate weakened."""
from decomp.usa_cright4_promotion import plan, jp55, glitch, opening, BATCH, write, sha, re
def stage_with_prefix(co,r,selected=None,*,candidates=None,namespace="cright10"):
    if not re.fullmatch(r"[a-z][a-z0-9_]*",namespace):raise ValueError("Invalid staging namespace")
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
            header=raw[:ms[0].start()]; cursor=ms[0].start()
            prefix=jp55.word_span(header) if re.search(r"/\* [0-9A-Fa-f]{5,8} [0-9A-Fa-f]{8} [0-9A-Fa-f]{8} \*/",header) else None
            if prefix is not None and prefix != (None,None):
                # Existing owner split left zero padding before its first complete function.
                # Preserve every prefix byte and any orphan marker in the first ASM fragment.
                a,b=prefix
                if b!=begin or a>=b or any(rom[a:b]):raise ValueError('Prefix not authenticated zero padding')
                first=re.search(r'(?m)^\s*(?:nonmatching |/\* [0-9A-Fa-f]{5,8} [0-9A-Fa-f]{8} [0-9A-Fa-f]{8} \*/)',header)
                if not first:raise ValueError('Missing original prefix boundary')
                cursor=first.start();header=raw[:cursor];begin=a
            end_real=begin+s['size']
            if end_real<end:raise ValueError('Owner span beyond prior ELF object')
            if end_real>end:
                if jp55.word_span(raw[ms[-1].end():])!=(end,end_real) or any(rom[end:end_real]):raise ValueError('Unexpected prior text suffix')
            if section is None:raise ValueError('Unknown original section')
            cur=begin;byname={m['name']:m for m in ms};parts=[]
            for j,c in enumerate(rs):
                m=byname[c['name']];off=c['rom_offset'];size=c['original_bytes']
                if off<cur or m.start()<cursor:raise ValueError('overlapping owner extent')
                frag=raw[cursor:m.start()]
                if off>cur:
                    if jp55.word_span(frag)!=(cur,off):raise ValueError('Noncontiguous leading ASM span')
                    path=f'asm/{r}/{namespace}_{i:03}_{j:03}.s';parts.append(('asm',path,(header+frag).encode(),cur,off,None))
                elif re.search(r'/\* [0-9A-Fa-f]{5,8} [0-9A-Fa-f]{8} [0-9A-Fa-f]{8} \*/',frag):raise ValueError('Unowned ASM before candidate')
                path=f'src/{namespace}/{c["name"]}.c';parts.append(('c',path,(BATCH/c['source']).read_bytes(),off,off+size,c))
                cur=off+size;cursor=m.end()
            if cur<end_real:
                frag=raw[cursor:]
                if jp55.word_span(frag)!=(cur,end_real):raise ValueError('Noncontiguous final ASM span')
                path=f'asm/{r}/{namespace}_{i:03}_tail.s';parts.append(('asm',path,(header+frag).encode(),cur,end_real,None))
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
    write(co/f'build/{r}/{namespace}-stage.json',doc)
    return doc

