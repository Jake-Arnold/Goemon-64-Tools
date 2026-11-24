"""Native whole-unit USA 3CF0 replay on exact accepted USA2324 predecessor.
Original ROMs, generated reference assembly, and native objects remain private.
"""
import argparse, collections, hashlib, json, os, re, shutil, struct, subprocess
from pathlib import Path
from decomp.native251_promotion import runmake,restore_inline_usa
from decomp.usa_short72_promotion import restore_original_abs_label_type
from decomp.usa_opening_new2_promotion import elf_sections,stable_globals
from decomp.probe import Elf32
from decomp.glitch_g2_promotion import all_semantic_relocations
from decomp.overlay_crossregion47 import _funcs
from decomp.japan_cright_promotion import c_identities
from decomp.inventory import summarize_inventory
B=Path(__file__).resolve().parent
BASE='bd11874060a88dcac218550013796a82b802a89b'
PIN='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
TARGET='func_800030F0_3CF0'
PRIOR='efd759f4bf2e7024d695a15998427ab8696a5016c85e5c48c967df8db0d21c7f'
NATIVE='bb2691558d9c65b6443aaa60d26154286d52ffcaf4f84ed0cfe3d1db6cbf082b'
SHADOW='63fadb96b7a65499bfc17adc581037aa37e3449beb66cfbc211ace52ddee4918'
SOURCE='a632e01c1edd79e99fb8f12eb9cc9bc793863ca5df1d7fbce5ceaab5f2bc6a0f'
HEADER='9bbe57788cc6866b4d713e4b5f0f8cb07641d117a4d3e21cc8be4eee3df0cc74'
ROM='6ea0ed71032ce08fc2745f412d84936382197494';RETAIL='df8083a54296b8c151917c5333e1c85f014a2a66'
LEDGER='1babf419301bb2205b2d3a4f2815aca48bd6771aa998d9321c44eb8e9f8f9e94'
CC='76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0'
def sha(b):return hashlib.sha256(b).hexdigest()
def require(ok,msg):
    if not ok:raise ValueError(msg)
def eq(a,b,msg):require(a==b,msg)
def payload(e,n):return e.payload(e.names.index(n))
def records(e,n):
    return collections.Counter((r.offset,r.relocation_type,r.symbol.name or e.names[r.symbol.section],r.symbol.value,r.addend) for r in e.relocations(e.names.index(n)))
def typed_object(raw,prior):
    """Only the original ABS symbol types and exact zero-padding section metadata may change."""
    sec=elf_sections(raw);pool=sec['.rodata'];d=raw[pool['offset']:pool['offset']+pool['size']];require(pool['size'] in (20,32) and not any(d[20:]),'nonzero or unknown pool padding');buf=bytearray(raw)
    struct.pack_into('>I',buf,pool['head']+20,20);struct.pack_into('>I',buf,pool['head']+32,4)
    allowed=set(range(pool['head']+20,pool['head']+24))|set(range(pool['head']+32,pool['head']+36))
    if prior is not None:
        specs={'func_801CB460':('801cb460',0x12,[(0x6c,5),(0x70,6)]),'D_801CCB7C':('801ccb7c',0x11,[(0xfc,5),(0x10c,6),(0x1a8,5),(0x1b4,6),(0x1ec,5),(0x1f8,6)])}
        tab,strings=sec['.symtab'],sec['.strtab'];eq(tab['entsize'],16,'symbol width');g=stable_globals(prior)
        for name,(val,typ,sites) in specs.items():
            eq(g[(val,'0','NOTYPE','GLOBAL','DEFAULT','ABS',name)],1,'unverified predecessor ABS '+name);matches=[]
            for i in range(tab['size']//16):
                at=tab['offset']+16*i;no,v,sz,info,other,idx=struct.unpack_from('>IIIBBH',raw,at);n=strings['offset']+no
                if raw[n:raw.index(0,n)].decode()==name:matches.append((i,at,v,sz,info,other,idx))
            eq(len(matches),1,'ambiguous ABS '+name);i,at,v,sz,info,other,idx=matches[0];eq((v,sz,info,other,idx),(0,0,typ,0,0),'unexpected native symbol metadata '+name);actual=[]
            for k in ('.rel.text','.rel.rodata'):
                r=sec[k]
                for off,inf in struct.iter_unpack('>II',raw[r['offset']:r['offset']+r['size']]):
                    if inf>>8==i:eq(k,'.rel.text','unexpected relocation section');actual.append((off,inf&255))
            eq(actual,sites,'unexpected ABS sites '+name);buf[at+12]=0x10;allowed.add(at+12)
    require(all(i in allowed for i,(a,b) in enumerate(zip(raw,buf)) if a!=b),'nonmetadata byte change')
    for k in ('.text','.rel.text','.rel.rodata'):
        z=sec[k];eq(raw[z['offset']:z['offset']+z['size']],buf[z['offset']:z['offset']+z['size']],k+' changed')
    return bytes(buf)
def run(checkout,baseline,work,uv,ledger,jobs):
    c,base,w=map(Path,(checkout,baseline,work));w.mkdir(parents=True,exist_ok=False);bd=c/'build/usa';elf=bd/'mnsg.elf';obj=bd/'src/transition_state.c.o';src=c/'src/transition_state.c';ldpath=c/'.splat/usa/mnsg.ld';data=c/'asm/usa/data/main.rodata.s'
    old=w/'prior.elf';shutil.copyfile(elf,old);eq(sha(old.read_bytes()),PRIOR,'predecessor ELF');eq(subprocess.check_output(['git','rev-parse','HEAD'],cwd=c,text=True).strip(),PIN,'upstream pin');eq(sha((c/'tools/ido-5.3/cc').read_bytes()),CC,'IDO pin')
    # Ledger prefix is the exact reviewed live baseline; append-only findings permitted.
    eq(sha(Path(ledger).read_bytes()[:60826]),LEDGER,'reviewed compiler ledger drift')
    rom=(c/'config/usa/baserom.decompressed.z64').read_bytes();retail=(c/'config/usa/baserom.z64').read_bytes();eq((len(rom),hashlib.sha1(rom).hexdigest()),(33554432,ROM),'original expanded ROM');eq((len(retail),hashlib.sha1(retail).hexdigest()),(16777216,RETAIL),'original retail ROM');eq((bd/'mnsg.z64').read_bytes(),rom,'predecessor ROM');eq((base/'build/usa/mnsg.z64').read_bytes(),rom,'baseline ROM')
    f0=_funcs(old);g0=stable_globals(old);r0=all_semantic_relocations(old);n0=c_identities(old);eq((sum(f0.values()),sum(g0.values()),r0[1],len(n0)),(7376,26714,82098,2337),'predecessor identity/count');require(TARGET not in n0,'duplicate claim')
    # Original caller remains ASM: entry 15 in the handler table is the sole
    # symbolic reference, no live C caller or declaration exists. The exact
    # target overwrites the incoming a0 register before using it. Do not infer
    # a historical C prototype or introduce an incompatible future C caller.
    eq([x for x in r0[0] if x[-1]==TARGET],[('.rel.main',0x80058944,'R_MIPS_32',0x800030f0,TARGET)],'assembly dispatch reference changed')
    eq(struct.unpack_from('>I',rom,0x59544)[0],0x800030f0,'dispatch table entry');eq(rom[0x2ca0:0x2ca8].hex(),'0320f80900000000','assembly jalr/delay slot');eq(rom[0x3d00:0x3d04].hex(),'24647fff','incoming a0 overwritten')
    ld=ldpath.read_text();require('build/usa/asm/usa/2C40_w132_00.s.o(.text);' in ld,'original ASM caller not linked');active=set(re.findall(r'build/usa/(src/[^\s()]+\.c)\.o\(',ld));
    for f in sorted(active):
        p=c/f
        if p==src:continue
        require(TARGET not in p.read_text(errors='replace'),'unexpected C call or declaration '+f)
    for d in ('include','src','libultra/include'):
        for p in (c/d).rglob('*.h'):require(TARGET not in p.read_text(errors='replace'),'unexpected C header declaration '+str(p))
    body=(B/'arg_s32_add.c').read_bytes();header=(B/'transition.h').read_bytes();eq(sha(body),SOURCE,'candidate source drift');eq(sha(header),HEADER,'candidate header drift');eq(sha(src.read_bytes()),'330743dbb36806c8108c7f055b0980eabe9dd2ff53493578dd769a23f489950e','mixed predecessor owner drift');eq((c/'src/transition.h').read_bytes(),header,'header drift')
    # Independently assemble the original reference, taking only original
    # assembly from the pinned original checkout and verified ABS definitions.
    oasm=(base/'asm/usa/2C40.s').read_bytes();eq(sha(oasm),'f165645f8fd7a94387aa8b575118ce03346555c4db46943eb08364f333f9d343','original ASM provenance');a=oasm.decode();start=a.index('nonmatching '+TARGET);end='endlabel func_8000394C_454C';a=a[start:a.index(end)+len(end)];defs=(c/'.splat/usa/undefined_syms_auto.ld').read_text()
    for n in ('D_3ADCA','D_3ADD4','D_3ADD5','D_3ADD6','D_3ADD7','D_3ADD8','D_3ADD9','D_3ADDE','D_3ADDF','D_3ADE0','D_3ADE1','D_3ADF4'):
        v=int(n[2:],16);require(re.search(r'(?m)^'+n+r'\s*=\s*0x0*'+n[2:]+r'\s*;',defs,re.I),'unverified offset '+n);a=a.replace('%hi('+n+')',str((v+0x8000)>>16)).replace('%lo('+n+')',str((v&0xffff)-65536 if v&0x8000 else v&0xffff))
    a=a.replace('jtbl_8007A88C_7B48C','.Ltransition_pool');a=re.sub(r'(?m)^(\s*)jlabel (\.L\w+)$',r'\1\2:',a)
    text=data.read_text();eq(sha(data.read_bytes()),'744a979e38be80c94dd80d81ed683b45d1cf5ab8b8a439b0d507d856bcbad039','original data owner drift');m=re.search(r'^nonmatching jtbl_8007A88C_7B48C\n.*?^enddlabel jtbl_8007A88C_7B48C\n',text,re.M|re.S);require(m is not None,'original pool missing');words='\n'.join(x for x in m[0].splitlines() if '.word' in x);eq(len(words.splitlines()),5,'pool extent')
    independent='.include "macro.inc"\n\n.set noat\n.set noreorder\n.set gp=64\n\n.section .text, "ax"\n'+a+'\n\n.section .rodata,"a"\n.balign 4\n.Ltransition_pool:\n'+words+'\n\n.type D_802F7000,@object\n.type D_800C7AE4_C86E4,@object\n';eq(sha(independent.encode()),'63f35b17fce663f4c3a4f683f1f68f96e37d7cc4877f6e43309fc2c4fcefa754','independent reference source drift');shsrc=w/'independent.s';shsrc.write_text(independent);shobj=w/'independent.o';subprocess.run(['mips-linux-gnu-as','-EB','-mtune=vr4300','-march=vr4300','-mabi=32','-Iinclude','-I.','-o',str(shobj),str(shsrc)],cwd=c,check=True)
    pragma=f'#pragma GLOBAL_ASM("asm/usa/nonmatchings/transition_state/{TARGET}.s")'.encode();s=src.read_bytes();eq(s.count(pragma),1,'original pragma');s=s.replace(pragma,body.rstrip(),1);eq(s.count(b'#include "transition.h"'),2,'original header placement');p=s.rindex(b'#include "transition.h"\n');s=s[:p]+s[p+len(b'#include "transition.h"'):];eq(sha(s),'f9aa77062e4a1897d2c3f4d90b9448cd3ef115a5e0063735615980d248dbfd11','new whole source drift');src.write_bytes(s);obj.unlink();runmake(c,'usa',ld,['build/usa/src/transition_state.c.o'],w/'native-compile.log',uv,jobs);raw=obj.read_bytes();shraw=shobj.read_bytes();native=Elf32(raw);shadow=Elf32(shraw);eq(len(payload(native,'.text')),2256,'whole unit extent');eq(payload(native,'.text'),payload(shadow,'.text'),'whole unit text mismatch');eq(payload(native,'.rodata')[:20],payload(shadow,'.rodata'),'pool contents');eq(len(payload(shadow,'.rodata')),20,'pool size');eq(records(native,'.text'),records(shadow,'.text'),'whole text relocations');eq(records(native,'.rodata'),records(shadow,'.rodata'),'pool relocations');eq((sum(records(native,'.text').values()),sum(records(native,'.rodata').values())),(125,5),'unit relocation count')
    # Move the original five-word pool to the native owner without shifting
    # the rest of main.rodata; maintain the original exported symbol identity.
    alias='.section .rodata.transition_suffix,"a"\n.globl jtbl_8007A88C_7B48C\n.type jtbl_8007A88C_7B48C, @object\n.set jtbl_8007A88C_7B48C, . - 20\n.size jtbl_8007A88C_7B48C,20\n';data.write_text(text[:m.start()]+alias+text[m.end():]);owner='        build/usa/asm/usa/data/main.rodata.s.o(.rodata);';poolline='        build/usa/src/transition_state.c.o(.rodata);';eq((ld.count(owner),ld.count(poolline)),(1,1),'pool linker ownership');ld=ld.replace(poolline,'',1).replace(owner,owner+'\n'+poolline+'\n        build/usa/asm/usa/data/main.rodata.s.o(.rodata.transition_suffix);',1);ldpath.write_text(ld)
    mf=c/'Makefile';mf.write_text(mf.read_text()+'\n# Retain the exact original 0x16c byte prefix before the five-entry transition table.\nbuild/usa/asm/usa/data/main.rodata.s.o: ASFLAGS += --no-pad-sections\n');dobj=bd/'asm/usa/data/main.rodata.s.o';dobj.unlink(missing_ok=True);runmake(c,'usa',ld,['build/usa/asm/usa/data/main.rodata.s.o'],w/'data.log',uv,jobs);e=Elf32(dobj.read_bytes());eq((len(payload(e,'.rodata')),len(payload(e,'.rodata.transition_suffix'))),(364,512),'original pool boundaries')
    def link(tag,content,expected):
        obj.write_bytes(content);elf.unlink(missing_ok=True);(bd/'mnsg.z64').unlink(missing_ok=True);runmake(c,'usa',ld,['build/usa/mnsg.z64'],w/f'{tag}-link.log',uv,jobs);eq(obj.read_bytes(),content,'native/reference object unexpectedly rebuilt');restore_original_abs_label_type(elf,old);restore_inline_usa(elf,old);eq((bd/'mnsg.z64').read_bytes(),rom,tag+' expanded ROM mismatch');eq(_funcs(elf),f0,tag+' FUNC identities');eq(stable_globals(elf),g0,tag+' global identities');eq(sha(elf.read_bytes()),expected,tag+' ELF hash');rp=w/f'{tag}-retail.z64';subprocess.run([str(uv),'run','python','tools/rommy.py','compress','--input','build/usa/mnsg.z64','--output',str(rp),'--manifest','config/usa/rommy.yaml','--pad','--verify'],cwd=c,check=True,stdout=subprocess.DEVNULL);eq(rp.read_bytes(),retail,tag+' retail ROM');rp.unlink();shutil.copyfile(elf,w/f'{tag}.elf');return all_semantic_relocations(elf)
    # Independent reference first, native candidate last (retain native owner).
    rs=link('shadow',typed_object(shraw,None),SHADOW);rn=link('native',typed_object(raw,old),NATIVE);eq(rn,rs,'all original-reference relocations');eq(rn[1:],(82080,'4355f0fb9f6fa47bc6c301ac91b93c97682abb205df57db5052d31fa665a7722'),'full relocation identity');delta=json.loads((B/'relocation-delta.json').read_text());eq(dict(r0[0]-rn[0]),{tuple(x):v for x,v in delta['removed']},'exact removed relocation delta');eq(dict(rn[0]-r0[0]),{tuple(x):v for x,v in delta['added']},'exact added relocation delta');eq(c_identities(elf),n0|{TARGET},'strict new C owner');read=lambda p:subprocess.check_output(['readelf','-Ws',str(p)],text=True);inv=summarize_inventory(read(base/'build/usa/mnsg.elf'),read(elf),(n0-c_identities(base/'build/usa/mnsg.elf'))|{TARGET});eq(inv,json.loads((B/'strict-inventory.json').read_text()),'strict inventory')
    proof={'status':'PASSED_G2_LOCAL','base_commit':BASE,'target':TARGET,'source_sha256':SOURCE,'whole_source_sha256':sha(s),'header_sha256':HEADER,'original_bytes':568,'whole_unit_bytes':2256,'pool_bytes':20,'unit_text_relocations':125,'pool_relocations':5,'prior_elf_sha256':PRIOR,'native_elf_sha256':NATIVE,'shadow_elf_sha256':SHADOW,'expanded_sha1':ROM,'retail_sha1':RETAIL,'expanded_bytes':33554432,'retail_bytes':16777216,'function_identities':7376,'stable_globals':26714,'prior_relocations':82098,'native_relocations':82080,'relocation_sha256':rn[2],'relocation_delta_sha256':sha((B/'relocation-delta.json').read_bytes()),'inventory':inv,'assembly_caller_contract':{'table_entry_rom':0x59544,'jalr_rom':0x2ca0,'sole_symbol_reference':True,'incoming_a0_overwritten':True,'live_c_callers_or_declarations':0,'historical_c_prototype':'UNKNOWN'},'compiler_outcome':'EXISTING_QUIRK_REPRODUCED','gameplay':'NOT_RUN'};(w/'proof.json').write_text(json.dumps(proof,indent=2)+'\n');return proof
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--checkout',type=Path,required=True);p.add_argument('--baseline',type=Path,required=True);p.add_argument('--work',type=Path,required=True);p.add_argument('--uv',required=True);p.add_argument('--ledger',type=Path,required=True);p.add_argument('--jobs',type=int,default=4);a=p.parse_args();print(json.dumps(run(a.checkout,a.baseline,a.work,a.uv,a.ledger,a.jobs),indent=2))
