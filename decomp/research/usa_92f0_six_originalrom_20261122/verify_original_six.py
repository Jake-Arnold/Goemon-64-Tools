#!/usr/bin/env python3
"""Reproduce four USA original-upstream SGI IDO C functions in aligned mixed units.

Private input ROM, original ASM, objects and ELFs never leave the scratch checkout.
This checks pinned original-upstream ROM/ELF, NOT canonical multi-accepted-C decomp G2.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

PIN = '7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
RETAIL = 'df8083a54296b8c151917c5333e1c85f014a2a66'
EXPANDED = '6ea0ed71032ce08fc2745f412d84936382197494'
EXPECTED_A548_SOURCE_SHA256 = '5fa2a51008147b456e2231f2312472b44d449a7da2d90f484d07868f9b0a44fe'
EXPECTED_A5C4_SOURCE_SHA256 = 'db144ba1eccbef05fff6247d9ee8fe3769e793ba0f87ddcce345b9502122df8e'
EXPECTED_MENU_SOURCE_SHA256 = '37eb14efded2671ea86242caffecd292c2f71c5595b0a5e51bba0c2662decbd0'

TARGETS = {
 'func_8000A18C_AD8C': (0xAD8C, 48, 'a494dc6ba7f3ed16e1aa8232fd8e54d8948e40a7f8d2b22b80df3f6a3686a385'),
 'func_8000AAE8_B6E8': (0xB6E8, 40, '790033f931cf2f15ea0e5d16204cd3caf6cec02a22e4ff55531aa196e9bcff77'),
 'func_8000AB30_B730': (0xB730, 68, '3919d906ca430e5f56cc9c36a2e3320e5563166409bfb71756249445bd1f1531'),
 'func_8000A548_B148': (0xB148, 124, 'c1cf2ee8a02922b916b67119f9e294b5aa65705d15be52a1cc89820abcd3a687'),
 'func_8000A5C4_B1C4': (0xB1C4, 80, '0f5842049608e62a458f580c7c3c10ea13681eb33fd1529593b76e7c0c902277'),
 'func_800108BC_114BC': (0x114BC, 40, '2b856135c3b09dccc933210170254d59c20068d60330c224d0f25eab42320aa7'),
}
NEIGHBOR = 'func_8000AFA8_BBA8'
NEIGHBOR_ROM = 0xBBA8
NEIGHBOR_SIZE = 0x2F0
BEA0 = 0xBEA0


def sha(path, name='sha256'):
 h = hashlib.new(name)
 with path.open('rb') as handle:
  for block in iter(lambda: handle.read(1 << 20), b''):
   h.update(block)
 return h.hexdigest()


def run(cmd, cwd, env, logfile):
 with logfile.open('w') as handle:
  status = subprocess.run(cmd, cwd=cwd, env=env, stdout=handle, stderr=subprocess.STDOUT)
 if status.returncode:
  raise RuntimeError('Private build command failed; see ' + str(logfile) + ' (exit ' + str(status.returncode) + ')')


def inspect_elf(path):
 functions, relocations = [], []
 for line in subprocess.check_output(['readelf', '-sW', str(path)], text=True).splitlines():
  match = re.match(r'^\s*\d+:\s+([0-9a-fA-F]+)\s+(\d+)\s+FUNC\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)', line)
  if match and int(match.group(2)) > 0:
   functions.append((match.group(6), int(match.group(1), 16), int(match.group(2)), match.group(3), match.group(4), match.group(5)))
 section = None
 for line in subprocess.check_output(['readelf', '-rW', str(path)], text=True).splitlines():
  sm = re.match(r"^Relocation section '([^']+)'", line)
  if sm: section = sm.group(1)
  match = re.match(r'^\s*([0-9a-fA-F]+)\s+[0-9a-fA-F]+\s+(R_MIPS_\S+)\s+[0-9a-fA-F]+\s+(\S+)', line)
  if match:
   assert section is not None
   relocations.append((section, int(match.group(1), 16), match.group(2), match.group(3)))
 return functions, relocations


def remove_unowned_padding(generated_asm):
 """Remove Splat's trailing NOPs from the *embedded pragma*; linker restores alignment.

 This never changes a function instruction. Splat regenerates the ASM, so do this
 AFTER the Splat split, not before. Fail closed on any changed source structure.
 """
 content = generated_asm.read_text()
 marker = 'endlabel ' + NEIGHBOR
 assert content.count(marker) == 1, 'Unexpected original function-end structure'
 before, after = content.split(marker)
 tail = [line for line in after.splitlines() if line.strip()]
 # Exactly two 4-byte NOP instructions, lying *after* the original endlabel.
 pattern = re.compile(r'^\s*/\*\s*([0-9A-Fa-f]+)\s+[0-9A-Fa-f]+\s+00000000\s*\*/\s+nop\s*$')
 assert len(tail) == 2, 'Unexpected additional code after endlabel'
 offsets = []
 for line in tail:
  match = pattern.fullmatch(line)
  assert match is not None, 'Unexpected nonpadding instruction after endlabel'
  offsets.append(int(match.group(1), 16))
 assert offsets == [NEIGHBOR_ROM + NEIGHBOR_SIZE, NEIGHBOR_ROM + NEIGHBOR_SIZE + 4], offsets
 generated_asm.write_text(before + marker + '\n')
 return {'trailing_padding_bytes': 8, 'original_padding_rom_range': ['0xBE98', '0xBEA0'],
         'removed_from_embedded_original_function': True, 'reintroduced_by_original_linker_alignment': True}


def main():
 ap = argparse.ArgumentParser(description=__doc__)
 for key in ('checkout', 'deps', 'runtime', 'out'):
  ap.add_argument('--' + key, required=True, type=Path)
 ap.add_argument('--jobs', type=int, default=16)
 opt = ap.parse_args()
 checkout, deps, runtime, out = (getattr(opt, key).resolve() for key in ('checkout', 'deps', 'runtime', 'out'))
 if out.exists(): raise SystemExit('Output already exists: ' + str(out))
 assert 1 <= opt.jobs <= 64
 assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=checkout, text=True).strip() == PIN
 assert not subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=checkout).strip(), 'Dirty pinned upstream tracked files'
 original_retail = checkout / 'config/usa/baserom.z64'
 original_expanded = checkout / 'config/usa/baserom.decompressed.z64'
 original_rebuilt = checkout / 'build/usa/mnsg.z64'
 original_elf = checkout / 'build/usa/mnsg.elf'
 assert original_retail.stat().st_size == 16777216 and sha(original_retail, 'sha1') == RETAIL
 assert original_expanded.stat().st_size == 33554432 and sha(original_expanded, 'sha1') == EXPANDED
 assert sha(original_rebuilt, 'sha1') == EXPANDED
 assert original_rebuilt.read_bytes() == original_expanded.read_bytes()
 assert original_elf.exists() and (checkout / 'tools/ido-5.3/cc').is_file()
 original = original_expanded.read_bytes()
 for name, (rom_offset, code_size, digest) in TARGETS.items():
  assert hashlib.sha256(original[rom_offset:rom_offset + code_size]).hexdigest() == digest, name
 root = Path(__file__).resolve().parent
 out.mkdir(parents=True)
 work = out / 'private_original_checkout_copy'
 shutil.copytree(checkout, work, symlinks=True)
 cfile = work / 'src/92F0.c'
 src_text = cfile.read_text()
 target = '#pragma GLOBAL_ASM("asm/usa/nonmatchings/92F0/func_8000A18C_AD8C.s")'
 assert src_text.count(target) == 1
 csource = (root / 'source/func_8000A18C_AD8C.c').read_text()
 assert csource.startswith('#include "common.h"\n')
 # Preserve the native-sensitive three separate C statements. Moving a newline
 # changes the original MIPS schedule at 0xB1CC and 0xB1D0.
 a5 = '#pragma GLOBAL_ASM("asm/usa/nonmatchings/92F0/func_8000A5C4_B1C4.s")'
 assert src_text.count(a5) == 1
 a5_source = (root / 'source/func_8000A5C4_B1C4.c').read_text()
 assert sha(root / 'source/func_8000A5C4_B1C4.c') == EXPECTED_A5C4_SOURCE_SHA256, 'Compilation sensitive to source line breaks'
 new_src = src_text.replace(target, csource.split('\n', 1)[1].strip())
 assert new_src.count(a5) == 1
 new_src = new_src.replace(a5, a5_source.split('\n', 1)[1].strip())
 # Preserve the exact source-line grouping that yields the original stack,
 # branch-delay and register scheduling for the inclusive range loop.
 a548 = '#pragma GLOBAL_ASM("asm/usa/nonmatchings/92F0/func_8000A548_B148.s")'
 assert new_src.count(a548) == 1
 a548_source = (root / 'source/func_8000A548_B148.c').read_text()
 assert sha(root / 'source/func_8000A548_B148.c') == EXPECTED_A548_SOURCE_SHA256, 'A548 line grouping changed'
 new_src = new_src.replace(a548, a548_source.split('\n',1)[1].strip())
 cfile.write_text(new_src)
 cfg = work / 'config/usa/splat.yaml'
 cfg_text = cfg.read_text()
 assert cfg_text.count('    - [0xB280, asm]') == 1
 assert cfg_text.count('    - [0xBEA0, asm]') == 1
 assert cfg_text.count('    - [0xC1D0, asm]') == 1
 cfg_text = cfg_text.replace('    - [0xB280, asm]', '    - [0xB280, c, research_mixed_b280]', 1)
 assert cfg_text.count('    - [0x10D80, asm]') == 1
 cfg_text = cfg_text.replace('    - [0x10D80, asm]', '    - [0x10D80, asm]\n    - [0x112F0, c, research_menu_112f0]\n    - [0x11580, asm]', 1)
 cfg.write_text(cfg_text)
 raw = (checkout / 'asm/usa/B280.s').read_text()
 names = re.findall(r'^nonmatching (func_\w+),', raw, re.M)
 assert len(names) == 11 and len(names) == len(set(names)), names
 assert 'func_8000AAE8_B6E8' in names and 'func_8000AB30_B730' in names
 output_source = '#include "common.h"\n\n'
 for name in names:
  if name in TARGETS:
   source = (root / 'source' / (name + '.c')).read_text()
   assert source.startswith('#include "common.h"\n')
   output_source += source.split('\n', 1)[1].strip() + '\n\n'
  else:
   output_source += '#pragma GLOBAL_ASM("asm/usa/nonmatchings/research_mixed_b280/' + name + '.s")\n'
 (work / 'src/research_mixed_b280.c').write_text(output_source)
 # Preserve jump-table-bearing menu graphics as original ASM, mixing only six
 # functions between original 16-byte-aligned boundaries.
 assert sha(root / 'source/func_800108BC_114BC.c') == EXPECTED_MENU_SOURCE_SHA256, 'IDO scheduling sensitive to source line breaks; pinned C text changed'
 menu_asm = (checkout / 'asm/usa/10D80.s').read_text()
 menu_names = re.findall(r'^nonmatching (func_\w+),', menu_asm, re.M)
 first = menu_names.index('func_800106F0_112F0')
 last = menu_names.index('func_80010980_11580')
 window = menu_names[first:last]
 assert window == [
  'func_800106F0_112F0','func_80010784_11384','func_8001080C_1140C',
  'func_80010864_11464','func_800108BC_114BC','func_800108E4_114E4']
 menu_source = '#include "common.h"\n\n'
 for menu_name in window:
  if menu_name == 'func_800108BC_114BC':
   c_source = (root / 'source' / (menu_name + '.c')).read_text()
   assert c_source.startswith('#include "common.h"\n')
   menu_source += c_source.split('\n', 1)[1].strip() + '\n\n'
  else:
   menu_source += '#pragma GLOBAL_ASM("asm/usa/nonmatchings/research_menu_112f0/' + menu_name + '.s")\n'
 (work / 'src/research_menu_112f0.c').write_text(menu_source)

 env = os.environ.copy()
 env['PYTHONHOME'] = str(runtime / 'python')
 env['PYTHONPATH'] = str(deps / '.venv/lib/python3.12/site-packages')
 env['PATH'] = str(deps / 'bin') + os.pathsep + env.get('PATH', '')
 env['LD_LIBRARY_PATH'] = str(runtime / 'lib') + (os.pathsep + env['LD_LIBRARY_PATH'] if env.get('LD_LIBRARY_PATH') else '')
 py = str(runtime / 'python/bin/python3.12')
 splat = str(deps / '.venv/bin/splat')
 run([py, splat, 'split', 'config/usa/splat.yaml'], work, env, out / 'private_splat.log')
 generated = work / 'asm/usa/nonmatchings/research_mixed_b280' / (NEIGHBOR + '.s')
 assert generated.is_file(), 'Splat did not produce the required neighboring ASM'
 for menu_name in window:
  if menu_name != 'func_800108BC_114BC':
   assert (work / 'asm/usa/nonmatchings/research_menu_112f0' / (menu_name + '.s')).is_file(), menu_name
 padding_proof = remove_unowned_padding(generated)
 for name in names:
  if name not in TARGETS:
   assert (work / 'asm/usa/nonmatchings/research_mixed_b280' / (name + '.s')).exists(), name
 run(['make', '-j' + str(opt.jobs), 'VERSION=usa', 'build/usa/mnsg.z64'], work, env, out / 'private_native_build.log')
 candidate = work / 'build/usa/mnsg.z64'
 candidate_elf = work / 'build/usa/mnsg.elf'
 assert candidate.stat().st_size == len(original) and sha(candidate, 'sha1') == EXPANDED
 assert candidate.read_bytes() == original, 'Complete original ROM differs'
 old_funcs, old_relocs = inspect_elf(original_elf)
 new_funcs, new_relocs = inspect_elf(candidate_elf)
 assert len(old_funcs) == len(new_funcs) == 7376, (len(old_funcs), len(new_funcs))
 assert Counter(old_funcs) == Counter(new_funcs), 'Original ELF positive-sized FUNC identity multiset differs'
 assert len(old_relocs) == len(new_relocs) == 82216, (len(old_relocs), len(new_relocs))
 assert Counter(old_relocs) == Counter(new_relocs), 'Original ELF relocation identity multiset differs'
 for name, (rom_offset, code_size, _) in TARGETS.items():
  match = [f for f in new_funcs if f[0] == name]
  assert len(match) == 1 and match[0][1] == (rom_offset - 0xC00 + 0x80000000) and match[0][2] == code_size, (name, match)
 neighbor = [f for f in new_funcs if f[0] == NEIGHBOR]
 assert len(neighbor) == 1 and neighbor[0][1] == 0x8000AFA8 and neighbor[0][2] == NEIGHBOR_SIZE, neighbor
 result = {
  'classification': 'RESEARCH_ONLY_SIX_FULL_ORIGINAL_UPSTREAM_ROM_ELF_EXACT',
  'pin': PIN, 'region': 'USA', 'original_retail_sha1': RETAIL,
  'original_expanded_sha1': EXPANDED, 'candidate_expanded_sha1': sha(candidate, 'sha1'),
  'complete_original_rom_byte_identity': len(original),
  'elf_positive_FUNC_count_both': len(new_funcs),
  'positive_FUNC_identity_multiset_exact': True,
  'original_upstream_elf_relocations_both': len(new_relocs),
  'original_relocations_multiset_exact': True,
  'original_elf_sha256': sha(original_elf), 'candidate_elf_sha256': sha(candidate_elf),
  'compiler_sha256': sha(work / 'tools/ido-5.3/cc'),
  'asm_processor_sha256': sha(work / 'tools/asm-processor/asm-processor'),
  'padding_quirk': padding_proof,
  'targets': [
   {'name': name, 'rom_offset': hex(off), 'vma': hex(0x80000000 + off - 0xC00),
    'code_bytes': size, 'source_sha256': sha(root / 'source' / (name + '.c'))}
   for name, (off, size, _) in TARGETS.items()],
  'canonical_decomp_verify': 'NOT_RUN', 'canonical_82103_semantic_relocations': 'NOT_RUN',
  'canonical_inventory': 'NOT_RUN', 'canonical_full_local_ci': 'NOT_RUN',
  'canonical_accepted_function_delta': 0,
 }
 (out / 'sanitized_report.json').write_text(json.dumps(result, indent=2) + '\n')
 print('PASS complete original upstream USA ROM, 33,554,432 / 33,554,432 bytes, SHA-1 ' + EXPANDED)
 print('PASS 7,376/7,376 positive-size original ELF FUNC identities')
 print('PASS 82,216/82,216 original-upstream ELF relocations')
 print('PASS six previously ASM-owned C, 400/400 original code bytes')
 print('RESEARCH_ONLY. Modern accepted-C decomp.verify/inventory/full local_ci NOT_RUN')

if __name__ == '__main__':
 main()
