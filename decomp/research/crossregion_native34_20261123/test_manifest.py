"""ROM-free manifest integrity test; genuine native replay is in the same-chat source-only ZIP."""
import json
from pathlib import Path
p=Path(__file__).with_name('manifest.json')
m=json.loads(p.read_text())
a=m['functions']
assert len(a)==34 and sum(x['size'] for x in a)==1364
assert len({(x['region'],x['original_rom_offset']) for x in a})==34
assert sum(x['previous_native_research']=='PR_183' for x in a)==5
assert sum(x['symbolic_original_vma_linked'] for x in a)==8
assert sum(x['tier']=='A' for x in a)==24
assert sum(x['tier']=='B' for x in a)==2
assert sum(x['tier']=='C' for x in a)==8
assert m['canonical_C_unchanged']=={'usa':2164,'japan_0':2398}
assert m['new_full_original_ROM_G2']=='NOT_RUN'
print('native34 source-only index: PASS')
