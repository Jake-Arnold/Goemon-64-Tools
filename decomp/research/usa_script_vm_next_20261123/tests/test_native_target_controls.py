"""Read-only negative controls over private original native object and ROM."""
import argparse, copy, json, struct, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]));from verify_relocation_targets import audit,sections
p=argparse.ArgumentParser();p.add_argument('object',type=Path);p.add_argument('rom',type=Path);p.add_argument('audit',type=Path);a=p.parse_args()
obj=a.object.read_bytes();rom=a.rom.read_bytes();proof=json.loads(a.audit.read_text());assert audit(obj,rom,proof)['named_to_section_reference_entries_verified']==44
sec,idx,data=sections(obj);cases=[]
# Each mutation is to an in-memory test fixture only, never production object.
for label,offset in [('wrong-table-entry',sec[idx['.rodata']][4]+60),('wrong-float-pool-addend',sec[idx['.text']][4]+0x23e4),('wrong-branch-displacement',sec[idx['.text']][4]+0x1014)]:
    b=bytearray(obj);b[offset+3]^=1;cases.append((label,bytes(b),proof))
wrong=copy.deepcopy(proof);wrong['reloc_added'][0][0][4]='wrong_symbol';cases.append(('unexpected-reloc-symbol',obj,wrong))
wrong=copy.deepcopy(proof);wrong['globals_after']-=1;cases.append(('missing-global',obj,wrong))
wrong=copy.deepcopy(proof);wrong['reloc_after']+=1;cases.append(('wrong-reloc-count',obj,wrong))
for label,b,d in cases:
    try:audit(b,rom,d)
    except ValueError:print(label,'REJECTED')
    else:raise AssertionError(label+' accepted')
print('PASS positive and six fail-closed negative controls')
