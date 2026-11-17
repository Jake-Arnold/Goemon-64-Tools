"""Fail-closed 39-C Japanese rev-0 original-address staging.

Extends, but never modifies, the canonical historical 34-C source stage.
ROM images and generated source/ASM stay local and are never published.
"""
from __future__ import annotations
from pathlib import Path
import re,hashlib,subprocess
from . import japan_thirtyfour_c as prior
from .japan_relocation_policy import verify_text_relocations
CONFIG=Path('config/japan_0/splat_thirtynine_c.local.yaml')
SOURCE_NAMES=prior.SOURCE_NAMES+('jp_if_a7ac','jp_if_a7d0','jp_if_aa34','jp_if_aa74','jp_if_aa98')
REVIEWED=prior.REVIEWED
NEXT_FIVE=(('jp_if_a7ac','func_80039BAC_3A7AC',0x3A7AC),
           ('jp_if_a7d0','func_80039BD0_3A7D0',0x3A7D0),
           ('jp_if_aa34','func_80039E34_3AA34',0x3AA34),
           ('jp_if_aa74','func_80039E74_3AA74',0x3AA74),
           ('jp_if_aa98','func_80039E98_3AA98',0x3AA98))
OLD='    - [0x39604, asm, main_39604]'
NEW='\n'.join((OLD,
    '    - [0x3A7AC, c, jp_if_a7ac]',
    '    - [0x3A7D0, c, jp_if_a7d0]',
    '    - [0x3A7F4, asm, main_3A7F4]',
    '    - [0x3AA34, c, jp_if_aa34]',
    '    - [0x3AA58, asm, main_3AA58]',
    '    - [0x3AA74, c, jp_if_aa74]',
    '    - [0x3AA98, c, jp_if_aa98]',
    '    - [0x3AABC, asm, main_3AABC]'))


def render_config(original: str) -> str:
    expected=prior.render_config(original)
    if expected.count(OLD)!=1:raise ValueError('Original Japanese main-code boundary drift')
    final=expected.replace(OLD,NEW,1)
    if final.count(', c,')!=35 or final.count('jp_if_a7ac')!=1 or final.count('jp_if_aa98')!=1:
        raise ValueError('Unexpected Japanese 39-C source layout')
    return final


def stage_config(root:Path)->Path:
    output=render_config((root/'config/japan_0/splat.yaml').read_text())
    target=root/CONFIG
    if target.exists() and target.read_text()!=output:raise FileExistsError('Japanese 39-C Splat stage drift')
    target.write_text(output)
    return target


def install_sources(root:Path,source_root:Path=Path(__file__).resolve().parent):
    installed=prior.install_sources(root,source_root)
    for stem,fun,offset in NEXT_FIVE:
        source=(source_root/'japan_matching'/(stem+'.c')).read_bytes()
        if fun.encode() not in source or b'GLOBAL_ASM' in source:raise ValueError('Invalid new C source: '+stem)
        target=root/'src'/(stem+'.c')
        if target.exists():
            existing=target.read_text()
            markers=re.findall(r'#pragma GLOBAL_ASM\("([^"]+)"\)',existing)
            if target.read_bytes()!=source and not (markers and all('asm/japan_0/nonmatchings/' in v for v in markers)):
                raise FileExistsError('Unexpected new source collision: '+stem)
        target.write_bytes(source)
        installed.append(str(target))
    assert len(installed)==35
    return installed


def prepare_layout(root:Path,objdump:str)->dict:
    # Original 24 reviewed C, five new 36-byte C, original nine original ASM
    # slices excluding the now-split main_39604, plus its four exact sub-slices.
    prepared=[]
    for stem,fn,size in prior.REVIEWED:
        path=root/'build/japan_0/src'/(stem+'.c.o')
        symbols=subprocess.check_output([objdump,'-t',str(path)],text=True)
        pattern=r'(?m)^0{1,8}\s+g\s+F\s+\.text\s+'+f'{size:08x}'+r'\s+'+re.escape(fn)+r'\s*$'
        if len(re.findall(pattern,symbols))!=1:raise ValueError('Wrong accepted Japanese C symbol: '+fn)
        reloc=subprocess.check_output([objdump,'-r','-j','.text',str(path)],text=True)
        expected=verify_text_relocations('japan_matching/'+stem+'.c',reloc)
        obj,meta=prior.pack_text_metadata(path.read_bytes(),size)
        if meta['relocations_preserved']!=expected:raise ValueError('Accepted Japanese relocation drift: '+fn)
        path.write_bytes(obj)
        prepared.append({'object':str(path.relative_to(root)),'function':fn,'size':size,**meta})
    for stem,fn,offset in NEXT_FIVE:
        path=root/'build/japan_0/src'/(stem+'.c.o')
        symbols=subprocess.check_output([objdump,'-t',str(path)],text=True)
        pattern=r'(?m)^0{1,8}\s+g\s+F\s+\.text\s+00000024\s+'+re.escape(fn)+r'\s*$'
        if len(re.findall(pattern,symbols))!=1:raise ValueError('Wrong new Japanese C symbol: '+fn)
        reloc=subprocess.check_output([objdump,'-r','-j','.text',str(path)],text=True)
        expected=verify_text_relocations('japan_matching/'+stem+'.c',reloc)
        obj,meta=prior.pack_text_metadata(path.read_bytes(),36)
        if expected!=4 or meta['relocations_preserved']!=expected:raise ValueError('Unexpected new C relocations '+fn)
        path.write_bytes(obj)
        prepared.append({'object':str(path.relative_to(root)),'function':fn,'size':36,**meta})
    reviewed_asm=(('main_370D0',0xA8,8),('main_37198',0x3E4,12),
                  ('main_376A4',0x1CC,4),('main_37DB8',0x134,12),
                  ('main_38240',0x184,12),('main_383E8',0x94,12),
                  ('main_38490',0x7C,4),('main_38F50',0x634,12),
                  ('main_39604',0x11A8,8),('main_3A7F4',0x240,0),
                  ('main_3AA58',0x1C,4),('main_3AABC',0x124,12))
    for stem,size,zero in reviewed_asm:
        path=root/'build/japan_0/asm/japan_0'/(stem+'.s.o')
        obj,meta=prior.pack_text_metadata(path.read_bytes(),size)
        if meta['zero_bytes_trimmed']!=zero:raise ValueError('New ASM section padding mismatch: '+stem)
        path.write_bytes(obj)
        prepared.append({'object':str(path.relative_to(root)),'assembly_slice':True,**meta})
    ld=root/'.splat/japan_0/mnsg.ld';before=ld.read_text()
    old='.main 0x80000450 : AT(main_ROM_START) SUBALIGN(16)'
    if before.count(old)!=1:raise ValueError('Japanese linker text alignment drift')
    after=before.replace(old,'.main 0x80000450 : AT(main_ROM_START) SUBALIGN(4)',1)
    ld.write_text(after)
    if len(prepared)!=41:raise ValueError('Wrong 39-C reviewed object count')
    return {'format':'japan-thirtynine-elf-layout-v1','objects':prepared,
            'linker_original_sha256':hashlib.sha256(before.encode()).hexdigest(),
            'linker_staged_sha256':hashlib.sha256(after.encode()).hexdigest(),
            'main_subalign_changed_from':16,'main_subalign_changed_to':4}


def main(argv=None):
    import argparse,json
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('operation',choices=('stage','install','layout'))
    ap.add_argument('checkout',type=Path)
    ap.add_argument('--objdump',default='mips-linux-gnu-objdump')
    ap.add_argument('--report',type=Path)
    args=ap.parse_args(argv)
    root=args.checkout.resolve(strict=True)
    result=(str(stage_config(root)) if args.operation=='stage'
            else install_sources(root) if args.operation=='install'
            else prepare_layout(root,args.objdump))
    if args.report:
        with args.report.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    else:print(json.dumps(result,indent=2))

if __name__=='__main__':main()
