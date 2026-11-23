"""Read-only audit of the two VM C-generated pools. NOT canonical relocation identity."""
import argparse, hashlib, json, struct
from pathlib import Path

def sections(raw):
    if raw[:7]!=b'\x7fELF\x01\x02\x01':raise ValueError('wrong ELF format')
    sh=struct.unpack_from('>I',raw,32)[0];es,n,si=struct.unpack_from('>HHH',raw,46)
    if es!=40:raise ValueError('wrong header width')
    sec=[struct.unpack_from('>10I',raw,sh+i*40) for i in range(n)]
    def data(s):return raw[s[4]:s[4]+s[5]]
    names=data(sec[si]); indices={names[s[0]:].split(b'\0',1)[0].decode():i for i,s in enumerate(sec)}
    return sec,indices,data

def s16(x):return (x&0xffff)-0x10000 if x&0x8000 else x&0xffff

def audit(obj,rom,diff):
    if hashlib.sha1(rom).hexdigest()!='6ea0ed71032ce08fc2745f412d84936382197494':raise ValueError('wrong original USA ROM')
    if not(diff['rom_exact'] and diff['funcs_exact'] and diff['globals_before']==diff['globals_after']==26714 and not diff['globals_removed'] and not diff['globals_added']):raise ValueError('full original ROM/function/global gate failed')
    if (diff['reloc_before'],diff['reloc_after'])!=(82103,82102):raise ValueError('unexpected relocation totals')
    removed={tuple(row):count for row,count in diff['reloc_removed']}; added={tuple(row):count for row,count in diff['reloc_added']}
    if len(removed)!=45 or len(added)!=44 or set(removed.values())!={1} or set(added.values())!={1}:raise ValueError('unexpected relocation delta')
    sec,idx,data=sections(obj); text=data(sec[idx['.text']]); ro=data(sec[idx['.rodata']]);syms=data(sec[idx['.symtab']]);
    if len(text)!=10112 or len(ro)!=224:raise ValueError('wrong native VM extent')
    def refs(name):
        b=data(sec[idx[name]]); result={}
        for p in range(0,len(b),8):
            off,info=struct.unpack_from('>II',b,p);_,v,_,kind,_,section=struct.unpack_from('>IIIBBH',syms,(info>>8)*16)
            if off in result:raise ValueError('duplicate relocation offset')
            result[off]=(info&255,section,v,kind&15)
        return result
    tr=refs('.rel.text');rr=refs('.rel.rodata');T=0x8003cfa0;R=0x8007d02c;M=0x80000450
    def word(b,p):return struct.unpack_from('>I',b,p)[0]
    def orig(a):return word(rom,a-0x80000000+0xc00)
    def take(old,new):
        if removed.pop(old,None)!=1 or added.pop(new,None)!=1:raise ValueError('unexpected named-to-section relocation delta '+str(old))
    targets=[]
    for hi,lo,addr,name in [(0x8003dfbc,0x8003dfc4,0x8007d068,'jtbl_8007D068_7DC68'),(0x8003f380,0x8003f384,0x8007d108,'D_8007D108_7DD08')]:
        if tr[hi-T]!=(5,idx['.rodata'],0,3) or tr[lo-T]!=(6,idx['.rodata'],0,3):raise ValueError('wrong native HI/LO relocation')
        rawadd=((word(text,hi-T)&0xffff)<<16)+s16(word(text,lo-T)); target=R+rawadd
        linked=((orig(hi)&0xffff)<<16)+s16(orig(lo))
        if target!=addr or linked!=addr:raise ValueError('native pool reference resolves to wrong original address')
        for a,k in [(hi,'R_MIPS_HI16'),(lo,'R_MIPS_LO16')]:take(('.rel.main',a,k,addr,name),('.rel.main',a,k,M,'.main'))
        targets.append({'reference':name,'hi':hex(hi),'lo':hex(lo),'native_section_addend':hex(rawadd),'resolved_original_target':hex(target)})
    for i in range(40):
        off=60+i*4; a=R+off; t=T+word(ro,off)
        if rr[off]!=(2,idx['.text'],0,3) or t!=orig(a):raise ValueError('wrong native dispatcher target')
        originals=[r for r in removed if r[:4]==('.rel.main',a,'R_MIPS_32',t) and r[4].startswith('.L')]
        if len(originals)!=1:raise ValueError('wrong original named table entry')
        take(originals[0],('.rel.main',a,'R_MIPS_32',M,'.main'))
    a=0x8003dfb4;dest=a+4+4*s16(word(text,a-T)); expected=('.rel.main',a,'R_MIPS_PC16',dest,'.L8003E190_3ED90')
    if dest!=0x8003e190 or word(text,a-T)!=orig(a) or a-T in tr or removed.pop(expected,None)!=1:raise ValueError('wrong eliminated local branch relocation')
    if removed or added:raise ValueError('unexpected remaining differences')
    return {'status':'TARGET_EQUIVALENCE_ONLY_CANONICAL_RELOC_FAIL','named_to_section_reference_entries_verified':44,'original_jump_table_targets_verified':40,'original_pool_hi_lo_pairs_verified':2,'local_branch_target_verified':hex(dest),'native_relocations_mutated':False,'original_named_relocation_identity':False,'pool_pairs':targets}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('object',type=Path);p.add_argument('rom',type=Path);p.add_argument('audit',type=Path);p.add_argument('--out',type=Path);args=p.parse_args();r=audit(args.object.read_bytes(),args.rom.read_bytes(),json.loads(args.audit.read_text()));s=json.dumps(r,indent=2)+'\n';print(s,end='');
    if args.out:args.out.write_text(s)
