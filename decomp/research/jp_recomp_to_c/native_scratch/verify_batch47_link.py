from pathlib import Path
import os
from collections import Counter
import subprocess,re,json,hashlib
ORIG=Path(os.environ['GOEMON_BASELINE'])/'build/usa/mnsg.elf'
CAND=Path(os.environ['GOEMON_CANDIDATE'])/'build/usa/mnsg.elf'
ROM=Path(os.environ['GOEMON_BASELINE'])/'config/usa/baserom.decompressed.z64'
PROD=Path(os.environ['GOEMON_CANDIDATE'])/'build/usa/mnsg.z64'
PROVENANCE=Path(os.environ['GOEMON_CANDIDATE'])/'promotion_scratch_metadata.json'
SECTIONS=['file_12','file_13','file_14','file_15','file_17','file_18','file_19']

def symbols(path):
 s=subprocess.check_output(['readelf','-Ws',str(path)],text=True)
 names=[]
 for row in s.splitlines():
  p=row.split()
  if len(p)>=8 and p[3]=='FUNC' and p[6]!='UND' and int(p[2])>0:
   names.append((p[7],int(p[1],16),int(p[2])))
 return Counter(names)

def reloc(path):
 raw=subprocess.check_output(['readelf','-Wr',str(path)],text=True)
 section=None; result={}
 for row in raw.splitlines():
  m=re.match(r"Relocation section '\.rel\.(file_\d+)' at offset 0x[0-9a-f]+ contains (\d+) entries",row)
  if m: section=m.group(1);result[section]=[];continue
  if row.startswith('Relocation section ') or row.startswith('There are no relocations'):
   section=None;continue
  if section:
   p=row.split()
   if len(p)>=5 and p[2].startswith('R_MIPS_'):
    result[section].append((int(p[0],16),p[2],p[3],p[4],''.join(p[5:])))
 return result

orig_syms=symbols(ORIG);cand_syms=symbols(CAND)
print('REFERENCE_ORIGINAL_POSITIVE_FUNC',sum(orig_syms.values()))
print('CANDIDATE_ORIGINAL_POSITIVE_FUNC',sum(cand_syms.values()))
print('REFERENCE_ONLY',list((orig_syms-cand_syms).elements())[:5])
print('CANDIDATE_ONLY',list((cand_syms-orig_syms).elements())[:5])
assert sum(orig_syms.values())==7376
assert orig_syms==cand_syms
print('ELF_COMPLETE_7376_IDENTITY_PASS')
old,new=reloc(ORIG),reloc(CAND)
rel_count={}
for section in SECTIONS:
 o=Counter(old[section]); c=Counter(new[section]);
 rel_count[section]={'original':len(old[section]),'candidate':len(new[section]),'multiset_equal':o==c}
 print('RELOC',section,'original',len(old[section]),'candidate',len(new[section]),'equal',o==c)
 if o!=c:
  print('BASELINE_ONLY',list((o-c).elements())[:8])
  print('CANDIDATE_ONLY',list((c-o).elements())[:8])
 assert o==c,'Mismatch relocation multiset '+section
print('SEVEN_RELOCATION_MULTISETS_PASS')
b=ROM.read_bytes(); c=PROD.read_bytes()
assert len(b)==33554432 and c==b
print('EXACT_COMPLETE_33554432_ROM_PASS',hashlib.sha1(c).hexdigest())
meta=json.loads(PROVENANCE.read_text())['functions']
assert len(meta)==47 and sum(f['size'] for f in meta)==2220
for f in meta:
 assert (f['name'],int(f['name'].split('_')[1],16),f['size']) in cand_syms
 print('PROVED',f['name'],f['size'])
print('ALL_47_ORIGINAL_FUNCTION_IDENTITIES_PASS')
report={
 'format':'goemon-usa-47-function-original-asm-baseline-linked-native-scratch-v1',
 'status':'LINKED_SCRATCH_PASS_NOT_CANONICAL_G2',
 'native_source_baseline':'unmodified original upstream mnsg ASM (not canonical 315-C mixed build)',
 'rom_sha1':hashlib.sha1(c).hexdigest(),
 'rom_bytes':len(c),
 'complete_rom_bytes_equal':True,
 'original_elf_positive_FUNC_symbols':sum(orig_syms.values()),
 'candidate_elf_positive_FUNC_symbols':sum(cand_syms.values()),
 'exact_original_func_identity_multiset':True,
 'relocations':rel_count,
 'new_c_functions':len(meta),
 'new_c_instruction_bytes':sum(f['size'] for f in meta),
 'functions':[dict(name=f['name'],size=f['size'],section=f['section'],rom_offset=f['rom_offset']) for f in meta],
 'original_elf_sha256':hashlib.sha256(ORIG.read_bytes()).hexdigest(),
 'candidate_elf_sha256':hashlib.sha256(CAND.read_bytes()).hexdigest(),
 'limitations':['Not a combined original 315-C + 47 C decomp G2','Full decomp.local_ci not run in this native checkout','No manifest count increment without combined acceptance']
}
(Path(os.environ['GOEMON_CANDIDATE'])/'promotion_47_native_scratch_proof.json').write_text(json.dumps(report,indent=2)+'\n')
print('RESEARCH_PROOF_WRITTEN')
