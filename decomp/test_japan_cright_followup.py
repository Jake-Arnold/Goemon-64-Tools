"""Strict original native C follow-up: frozen source, inventory, and proof controls."""
import json, unittest
from unittest.mock import patch
from decomp import japan_cright_followup as jp
from decomp import japan_crossregion30_integrity as predecessor

class CRightFollowupTests(unittest.TestCase):
    def test_native_source_manifest_and_control_hashes(self):
        rows=jp.rows()
        self.assertEqual(len(rows),4)
        self.assertEqual(sum(f['size'] for f in rows),316)
        self.assertEqual(sum(f['native_relocation_count'] for f in rows),15)
        self.assertTrue(all(f['negative_first_difference'] is not None for f in rows))
        self.assertTrue(all(a['rom_offset']+a['size']<=b['rom_offset'] for a,b in zip(rows,rows[1:])))
    def test_wrong_manifest_fails_closed(self):
        with patch.object(jp,'MANIFEST_SHA','0'*64):
            with self.assertRaises(ValueError): jp.rows()
    def test_five_original_matches_but_phase_remains_asm(self):
        data=json.loads(jp.MANIFEST.read_text());self.assertEqual(len(data['functions']),5)
        phase=next(f for f in data['functions'] if f['name']=='func_8000339C_3F9C')
        self.assertTrue(phase['isolated_linked_exact']);self.assertFalse(phase['eligible_for_strict_stage'])
        self.assertEqual(phase['original_raw_relocation_count']-phase['native_relocation_count'],6)
    def test_fresh_local_regional_proof_and_inventory(self):
        proof=json.loads((jp.ROOT/'results/japan_0_2432_cright_followup_g2_20261123.json').read_text())
        inv=json.loads((jp.ROOT/'results/japan_0_2432_cright_followup_inventory_20261123.json').read_text())
        reg=json.loads((jp.ROOT/'regions/japan_0_cright_followup_2432.json').read_text())
        self.assertEqual(predecessor.validate()['accepted_C'],2428)
        names={f['name'] for f in jp.rows()}
        self.assertEqual(names,set(proof['new_C_names']));self.assertEqual(names,set(inv['new_C_names']))
        self.assertEqual(names,{f['name'] for f in reg['functions']})
        for k,v in {'before_C':2428,'after_C':2432,'added_C':4,'added_bytes':316,'original_bytes_after':130584,'asm_remaining':4944,'elf_identities_exact':7376,'semantic_relocations_exact':80745,'semantic_relocations_sha256':jp.BASE_RELOC_HASH,'stable_global_symbol_identities_exact':26393,'full_original_expanded_rom_equal':True,'full_original_retail_rom_equal':True}.items():
            self.assertEqual(proof[k],v);self.assertEqual(inv[k],v)
        self.assertEqual(proof['new_relocation_exceptions'],0)
        self.assertEqual(proof['rom_sha1'],jp.ROM_SHA)
        self.assertEqual(proof['retail_sha1'],'9843ee979b5f6c80f5eda85df0baed9ae7c4e73b')
        for f in jp.rows():
            self.assertEqual(inv['source_sha256_by_name'][f['name']],f['source_sha256'])
            self.assertEqual(inv['original_rom_offset_by_name'][f['name']],f['rom_offset'])
        self.assertNotIn('func_8000339C_3F9C',names)
if __name__=='__main__':unittest.main()
