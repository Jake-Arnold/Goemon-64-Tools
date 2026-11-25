"""Authenticate the single synthetic PC16 provenance delta using two complete original-ASM links."""
from pathlib import Path
from collections import Counter
import hashlib, subprocess, re
from decomp.consolidated_batch_promotion import stage, cross, opening, glitch, jp55, probe

NAME='func_080040B8_6C8278'
LABEL='.L08004178_6C8338'
DELTA=('.rel.file_30',0x08004154,'R_MIPS_PC16',0x08004178,LABEL)
ALIAS=LABEL+' = . + 0xC0;'
sha=lambda b:hashlib.sha256(b).hexdigest()

def link_references(co,base,w,doc,prior,elf,ld,rom):
    """No relocation record rewritten. Both full reference ROMs must equal original."""
    f=next(x for x in doc['functions'] if x['name']==NAME)
    assert f['rom_offset']==0x6C8278 and f['vma']==0x080040B8 and f['original_bytes']==356
    original=(base/'asm/japan_0'/f['owner']).read_text(); active=(co/f['active_owner']).read_text()
    probe.get_original_splat_lines(base/'asm/japan_0'/f['owner'],NAME,f['rom_offset'],f['vma'],f['original_bytes'],rom[f['rom_offset']:f['rom_offset']+f['original_bytes']])
    blocks=list(jp55.BLOCK.finditer(original));block=[m for m in blocks if m['name']==NAME];assert len(block)==1; m=block[0]; src=original[m.start():m.end()]
    active_block=[m for m in jp55.BLOCK.finditer(active) if m['name']==NAME];assert len(active_block)==1;am=active_block[0];active_src=active[am.start():am.end()]
    # Global declaration is from the accepted predecessor's assembly split;
    # the independently extracted original Splat block has a local branch.
    assert len(re.findall(r'(?m)^\s*\.globl '+re.escape(LABEL)+r'\s*$',active_src))==1
    assert re.sub(r'(?m)^\s*\.globl '+re.escape(LABEL)+r'\s*\n','\n',active_src).split()==src.split()
    header=original[:blocks[0].start()];header=header if '.include' in header else '.include "macro.inc"\n.set noat\n.set noreorder\n.set gp=64\n.section .text, "ax"\n'
    before=glitch.all_semantic_relocations(prior);after=glitch.all_semantic_relocations(elf);assert before[0]-after[0]==Counter({DELTA:1}) and not after[0]-before[0]
    # Negative control: omission of the original section-relative alias must fail
    # specifically at the previously authenticated external interior label.
    assert ld.count(ALIAS)==1
    neg=w/'missing_alias.ld';neg.write_text(ld.replace(ALIAS,'',1));negout=w/'missing_alias.elf'
    failure=subprocess.run(['mips-linux-gnu-ld','-T',str(neg),'-T','.splat/japan_0/undefined_syms_auto.ld','-T','.splat/japan_0/undefined_funcs_auto.ld','--no-check-sections','--emit-relocs','-o',str(negout)],cwd=co,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    assert failure.returncode!=0 and 'undefined reference' in failure.stdout and LABEL in failure.stdout
    (w/'missing_alias.log').write_text(failure.stdout);negout.unlink(missing_ok=True)
    records=[]
    for mode,body,expect,other in [('prior_global',active_src,before,prior),('original_local',src,after,elf)]:
        asm=w/(mode+'.s');obj=w/(mode+'.o');script=w/(mode+'.ld');out=w/(mode+'.elf');img=w/(mode+'.z64');asm.write_text(header+body+'\n');
        subprocess.run(['mips-linux-gnu-as','-EB','-mtune=vr4300','-march=vr4300','-mabi=32','-Iinclude','-I.','-o',str(obj),str(asm)],cwd=co,check=True)
        glitch.check_nontext(obj);cross._trim_object(obj,356,rom[0x6C8278:0x6C8278+356]);
        needle=f'build/japan_0/{f["staged_path"]}.o(.text);';assert ld.count(needle)==1 and ld.count(ALIAS)==1
        refld=ld.replace(needle,f'{obj}(.text);',1)
        if mode=='prior_global':refld=refld.replace(ALIAS,'',1)
        script.write_text(refld)
        subprocess.run(['mips-linux-gnu-ld','-T',str(script),'-T','.splat/japan_0/undefined_syms_auto.ld','-T','.splat/japan_0/undefined_funcs_auto.ld','--no-check-sections','--emit-relocs','-o',str(out)],cwd=co,check=True)
        subprocess.run(['mips-linux-gnu-objcopy','-O','binary','--pad-to=0x2000000','--gap-fill=0x00',str(out),str(img)],cwd=co,check=True)
        assert img.read_bytes()==rom;assert glitch.all_semantic_relocations(out)==expect;assert cross._funcs(out)==cross._funcs(other);assert opening.stable_globals(out)==opening.stable_globals(other)
        def identity(p):return [x.split()[1:] for x in subprocess.check_output(['readelf','-Ws',str(p)],text=True).splitlines() if x.split() and x.split()[-1]==LABEL]
        assert identity(out)==identity(other) and len(identity(out))==1
        records.append({'mode':mode,'source_sha256':sha(asm.read_bytes()),'elf_sha256':sha(out.read_bytes()),'expanded_sha1':hashlib.sha1(img.read_bytes()).hexdigest(),'relocations':expect[1],'relocation_sha256':expect[2],'full_rom_exact':True,'full_relocations_exact':True,'function_identities_exact':True,'stable_globals_exact':True,'label_identity_exact':True})
        img.unlink();out.unlink()
    return {'status':'PASS','original_asm_sha256':sha(original.encode()),'active_asm_sha256':sha(active.encode()),'removed_named_record':list(DELTA),'added_named_records':[],'reference_links':records,'native_relocation_records_unmodified':True,'no_alias_link_negative_rejected':True}
