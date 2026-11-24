"""Stage verified JP6 proof into local candidate source; never publish or merge."""
from pathlib import Path
import argparse, json
from decomp import japan_cright6_integrity as audit
from decomp import japan_cright6_promotion as stage


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('proof_dir',type=Path);a=p.parse_args()
    proof=json.loads((a.proof_dir/'g2.json').read_text());inventory=json.loads((a.proof_dir/'inventory.json').read_text())
    head_path=stage.ROOT/'regions/japan_0.json';head=json.loads(head_path.read_text())
    stage.require(stage.KEY not in head and not any(p.exists() for p in (audit.REGIONAL,audit.PROOF,audit.INVENTORY)),'candidate already activated or orphaned promotion')
    regional={'format':stage.FORMAT,'region':stage.REGION,'base_c':2528,'matching_c':2534,'assembly_remaining':4842,'original_C_instruction_bytes':138028,'functions':inventory['new_C_functions']}
    new_head={'format':stage.FORMAT,'status':'PASSED_G2_LOCAL','base_original_C':2528,'new_original_C':6,'accepted_original_C':2534,'accepted_original_bytes':138028,'asm_remaining':4842,'canonical_semantic_relocations':80745,'full_original_elf_identities':7376,'source_manifest':'decomp/regions/'+audit.REGIONAL.name,'proof':'decomp/results/'+audit.PROOF.name,'inventory':'decomp/results/'+audit.INVENTORY.name}
    result=audit.validate_documents(new_head,regional,proof,inventory)
    for path,data in ((audit.REGIONAL,regional),(audit.PROOF,proof),(audit.INVENTORY,inventory)):
        with path.open('x') as f:json.dump(data,f,indent=2);f.write('\n')
    head[stage.KEY]=new_head;stage.write(head_path,head)
    print(json.dumps(result,indent=2))
    print('Candidate activation only: full decomp.local_ci and review/merge remain mandatory.')

if __name__=='__main__':main()
