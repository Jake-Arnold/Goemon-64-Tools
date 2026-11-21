#!/usr/bin/env python3
"""Verify a 464-byte contiguous, four-function Japanese gameplay callback C unit.

Original IDO 5.3, MIPS ld, original linked VMA and full original code bytes.
An isolated 464-byte match is NOT full-ROM G2 acceptance.
"""
from __future__ import annotations
import argparse,hashlib,os,subprocess,tempfile
from pathlib import Path
SHA1='6f8745fecc3a5e7d4918c7a73353eb0726116ded'
SHA256='95030527ce8cf70a35cd44ebf1d7f7c85b8267b277765557ac02b62c671c0062'
START=0x8001F580;ROM_BASE=0x7FFFF400;SIZE=464
EXTERNAL={
 'g_system':0x800924B0,'D_800CD52C':0x800CD52C,'g_system_ptr':0x80161DB8,
 'D_80071210_71E10':0x80071210,'D_80072E08_73A08':0x80072E08,
 'func_80020110_20D10':0x80020110,'func_8000339C_3F9C':0x8000339C,
 'func_8000B654_C254':0x8000B654,'func_8001F750_20350':0x8001F750,
 'func_80038838_39438':0x80038838,'func_8003EE44_3FA44':0x8003EE44,
 'func_80004170_4D70':0x80004170,'func_80034B68_35768':0x80034B68}
def run(cmd,env):
 p=subprocess.run(list(map(str,cmd)),env=env,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(f'Command failed {p.returncode}: {p.args}\n{p.stdout}\n{p.stderr}')
def main():
 ap=argparse.ArgumentParser();
 for a in ('japan','ido','ld','objcopy'):ap.add_argument('--'+a,required=True,type=Path)
 args=ap.parse_args();rom=args.japan.read_bytes()
 assert len(rom)==33554432 and hashlib.sha1(rom).hexdigest()==SHA1, 'Wrong Japan ROM identity'
 with tempfile.TemporaryDirectory(prefix='jp4-native-') as t:
  p=Path(t);env=dict(os.environ)
  src=Path(__file__).resolve().parent/'jp_gameplay_callback_four_combined.c'
  (p/'link.ld').write_text(f'SECTIONS {{ .text 0x{START:08X} : SUBALIGN(4) {{ *(.text) }} .rodata : SUBALIGN(4) {{ *(.rodata) }} .data : SUBALIGN(4) {{ *(.data) }} .bss (NOLOAD) : SUBALIGN(4) {{ *(.bss) }} }}')
  run([args.ido,'-c','-G','0','-non_shared','-Xfullwarn','-Xcpluscomm','-Wab,-r4300_mul','-woff','649,838,712','-O2','-mips2','-o',p/'combined.o',src],env)
  ld=[args.ld,'-m','elf32btsmip','-T',p/'link.ld','--emit-relocs','-o',p/'combined.elf',p/'combined.o']
  for name,addr in EXTERNAL.items():ld+=['--defsym',f'{name}=0x{addr:08X}']
  run(ld,env)
  run([args.objcopy,'-O','binary','-j','.text',p/'combined.elf',p/'combined.bin'],env)
  code=(p/'combined.bin').read_bytes();orig=rom[START-ROM_BASE:START-ROM_BASE+SIZE]
  assert len(code)==SIZE, f'Wrong combined code length {len(code)}, expected {SIZE}'
  diffs=[i for i in range(0,SIZE,4) if code[i:i+4]!=orig[i:i+4]]
  assert not diffs, f'FAILED_NATIVE: mismatching original instructions at offsets {[hex(i) for i in diffs[:20]]}'
  assert hashlib.sha256(code).hexdigest()==SHA256, 'Wrong original code hash'
  print('PASS Japanese combined original-address C: 4 contiguous functions, 464/464 bytes, 116/116 MIPS words, original SHA-256')
  print('ISOLATED_EXACT / RESEARCH_ONLY; no full 32MiB ROM, ELF-relocation/inventory/CI gate')
if __name__=='__main__':main()
