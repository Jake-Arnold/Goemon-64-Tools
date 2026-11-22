#!/usr/bin/env python3
"""Authentic original-USA/Japan file22 IDO dual-region regression (research only).

This script does not contain, emit or distribute copyrighted original MIPS.
It requires externally supplied SHA-1-pinned decompressed ROMs and pinned IDO.
"""
from __future__ import annotations
import argparse,hashlib,json,os,random,math,re,subprocess,struct
from pathlib import Path
from reproduce_compiled_ido import FLAGS,PIN,text_from_elf32_be,code_stats,run_candidate
import trace_original_file22_mips as trace
USA_SHA1=trace.ROM_SHA1
JP_SHA1='6f8745fecc3a5e7d4918c7a73353eb0726116ded'
USA_ROM_OFFSET=0x69ECE4
JP_ROM_OFFSET=0x6A37D4
LENGTH=1808
JP_FUNCTION_SHA256='51a7ff3b9863ee6bcdae6ca0796934ecf91218ace5d39e48b8b1c892cf1084ae'
USA_PTR=0x801D701C
JP_PTR=0x801DC74C
SOURCE='usa_file22_1808_unsigned_cache_DIAGNOSTIC.c'
GLOBAL='D_801D701C_6A9C3C'

def original_region_check(usa,jp):
    if len(usa)!=33554432 or hashlib.sha1(usa).hexdigest()!=USA_SHA1:raise ValueError('Original USA image wrong SHA1')
    if len(jp)!=33554432 or hashlib.sha1(jp).hexdigest()!=JP_SHA1:raise ValueError('Original Japanese image wrong SHA1')
    us=usa[USA_ROM_OFFSET:USA_ROM_OFFSET+LENGTH]
    ja=jp[JP_ROM_OFFSET:JP_ROM_OFFSET+LENGTH]
    if hashlib.sha256(us).hexdigest()!=trace.FUNCTION_SHA256:raise ValueError('USA function slice wrong')
    if hashlib.sha256(ja).hexdigest()!=JP_FUNCTION_SHA256:raise ValueError('Japan function slice wrong')
    differences=[i for i in range(0,LENGTH,4) if us[i:i+4]!=ja[i:i+4]]
    if differences!=[0x40,0x4c]:raise ValueError(f'Unexpected cross-region code differences {differences}')
    def target(code):
        # At +0x40: LUI v1, high-adjusted address; at +0x4c: ADDIU v1,v1, signed low.
        lui,addiu=struct.unpack_from('>II',code,0x40)[0],struct.unpack_from('>I',code,0x4C)[0]
        if lui>>16!=0x3c03 or addiu>>16!=0x2463:raise ValueError('Incorrect symbol materialization opcodes')
        lo=struct.unpack('>h',struct.pack('>H',addiu&65535))[0]
        return ((lui&65535)<<16)+lo & 0xffffffff
    if (target(us),target(ja))!=(USA_PTR,JP_PTR):raise ValueError('The two differences do not resolve to expected cursor symbols')
    # Correct relative start is +0xC64 in both source overlays, not a guessed name match.
    assert (USA_ROM_OFFSET-0x69E080)==(JP_ROM_OFFSET-0x6A2B70)==0xC64
    return us,ja,{'usa_function_rom':f'0x{USA_ROM_OFFSET:X}','jp_function_rom':f'0x{JP_ROM_OFFSET:X}',
      'usa_guest_vma':'0x801CC0C4','jp_guest_vma':'0x801D17F4',
      'code_bytes':LENGTH,'instruction_positions':452,
      'byte_identical_instruction_positions':450,
      'cross_region_relocated_instruction_offsets':[f'0x{x:02X}' for x in differences],
      'usa_cursor':f'0x{USA_PTR:08X}','jp_cursor':f'0x{JP_PTR:08X}',
      'overlay_vma_delta':'0x5730',
      'usa_function_sha256':hashlib.sha256(us).hexdigest(),
      'jp_function_sha256':hashlib.sha256(ja).hexdigest()}

def compiled_for_address(obj,target):
    data=bytearray(text_from_elf32_be(obj))
    s=subprocess.check_output(['readelf','-rW',str(obj)],text=True)
    rows=re.findall(r'(?m)^([0-9a-fA-F]{8})\s+[0-9a-fA-F]{8}\s+(R_MIPS_[A-Z0-9]+)\s+[0-9a-fA-F]{8}\s+(\S+)\s*$',s)
    if len(rows)!=2 or [x[1] for x in rows]!=['R_MIPS_HI16','R_MIPS_LO16'] or any(x[2]!=GLOBAL for x in rows):
        raise ValueError('IDA native object must contain precisely one original HI16/LO16 relocation pair')
    for off_s,kind,name in rows:
        off=int(off_s,16)
        if off%4 or off+4>len(data):raise ValueError('Out-of-range relocation')
        word=int.from_bytes(data[off:off+4],'big')
        if word&65535:raise ValueError('Unexpected nonzero relocation immediate')
        immediate=(((target+0x8000)>>16)&65535) if kind=='R_MIPS_HI16' else target&65535
        data[off:off+4]=((word&0xFFFF0000)|immediate).to_bytes(4,'big')
    return bytes(data)

def geometry_cases():
    rng=random.Random(0x69ece4)
    widths=[32,64,96,128,160,192,224,256,320]
    heights=[32,64,96,128,160,192,224,256]
    layouts=[]
    for _ in range(200):
        w,h=rng.choice(widths),rng.choice(heights)
        cols,rows=math.ceil(320/w),math.ceil(240/h)
        if cols*rows>64:continue
        count=w//32*(h//32)
        if not 1<=count<=80:continue
        maximum=min(3,80//count-1)
        if maximum<0:continue
        pages=[rng.randint(0,maximum) for _ in range(cols*rows)]
        layout=(cols,rows,w,h,pages)
        if layout not in layouts:layouts.append(layout)
        if len(layouts)==64:break
    if len(layouts)!=64:raise ValueError('Deterministic geometry inventory changed')
    return [(i%4,f'geometry_{i:02d}',None,x) for i,x in enumerate(layouts)]

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('usa','japan','checkout','deps','runtime','output'):
        p.add_argument('--'+name,required=True,type=Path)
    args=p.parse_args();out=args.output.resolve()
    if out.exists():raise ValueError('Do not overwrite previous research output')
    checkout=args.checkout.resolve()
    if subprocess.check_output(['git','rev-parse','HEAD'],cwd=checkout,text=True).strip()!=PIN:
        raise ValueError('Wrong pinned upstream version')
    usa=args.usa.read_bytes();jp=args.japan.read_bytes()
    original_us,original_jp,comparison=original_region_check(usa,jp)
    source=Path(__file__).with_name(SOURCE)
    out.mkdir(parents=True)
    cc=checkout/'tools/ido-5.3/cc'
    env=os.environ.copy()
    env['PATH']=str(args.deps.resolve()/'bin')+os.pathsep+env.get('PATH','')
    env['LD_LIBRARY_PATH']=str(args.runtime.resolve()/'lib')+os.pathsep+env.get('LD_LIBRARY_PATH','')
    obj=out/'candidate.o'
    proc=subprocess.run([str(cc),*FLAGS,'-o',str(obj),str(source)],cwd=checkout,env=env,capture_output=True,text=True)
    (out/'ido_compiler.log').write_text(proc.stdout+'\n'+proc.stderr)
    if proc.returncode:raise ValueError('IDO 5.3 failed to compile research C')
    us_code=compiled_for_address(obj,USA_PTR)
    jp_code=compiled_for_address(obj,JP_PTR)
    usa_stat=code_stats(original_us,us_code)
    jp_stat=code_stats(original_jp,jp_code)
    # For function shape, the Japanese original and USA differ only at 2 original relocation words.
    # The candidate remains FAILED_NATIVE in both regions.
    oracle=[(mode,name,rows,layout,trace.run_once(usa,mode,rows,layout)[1])
            for mode,name,rows,layout in geometry_cases()]
    saved_end=trace.END
    try:
        trace.END=trace.ENTRY+len(us_code)
        outcomes=run_candidate(usa,us_code,oracle)
    finally:trace.END=saved_end
    cases_passed=sum(bool(x['pass']) for x in outcomes)
    mismatches=sum(x.get('mismatching_64_bit_commands',0) for x in outcomes)
    report={'status':'RESEARCH_ONLY_NOT_NATIVE_EXACT','reference_check':comparison,
       'candidate_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
       'candidate_source_diagnostic_storage_not_authentic':True,
       'original_USA_vs_compiled_USA':usa_stat,
       'original_JP_vs_compiled_JP':jp_stat,
       'native_relocations':2,
       'expanded_synthetic_cases':len(oracle),
       'expanded_graphics_cases_pass':cases_passed,
       'expanded_graphics_commands_compared':sum(x['original_commands'] for x in outcomes if 'original_commands' in x),
       'expanded_gfx_command_differences':mismatches,
       'expanded_failed_cases':[{'case':x.get('scenario'),'error':x.get('error_type','compare')} for x in outcomes if not x['pass']],
       'native_exact_both_regions':bool(usa_stat['source_code_exact'] and jp_stat['source_code_exact']),
       'promotion':'NONE'}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    if len(oracle)!=64 or cases_passed!=64 or mismatches or report['native_exact_both_regions']:
        raise ValueError('Unexpected input or semantic/native result — review report')
if __name__=='__main__':main()
