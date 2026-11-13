"""Synthetic fail-closed layout guards; no private ROM or generated ASM needed."""
import hashlib
from pathlib import Path
from unittest import TestCase, main, mock

try:
    from . import overlay_file43 as mod
except ImportError:
    import overlay_file43 as mod


class OverlayFile43Tests(TestCase):
    @staticmethod
    def config():
        return ("name: Mystical Ninja Starring Goemon (USA)\n"
                f"sha1: {mod.ROM_SHA1}\n"
                "segments:\n"
                "  - name: file_42\n"
                "    type: code\n"
                "    start: 0x6F0210\n"
                "  - name: file_43\n"
                + "\n".join("    " + line for line in mod.EXPECTED_SEGMENT_LINES) + "\n"
                "  - name: file_44\n"
                "    type: code\n"
                "    start: 0x6FB200\n")

    def setUp(self):
        self.data = bytes(range(64))
        self.h = hashlib.sha256
        self.name = 'func_080001BC_6F369C'
        changes = dict(ROM_BYTES=len(self.data),
                       ROM_SHA1=hashlib.sha1(self.data).hexdigest(),
                       ROM_START=0, ROM_TEXT_END=32, ROM_END=48,
                       VMA_START=0x08000000,
                       TEXT_SHA256=self.h(self.data[:32]).hexdigest(),
                       RODATA_SHA256=self.h(self.data[32:48]).hexdigest())
        self.constants = mock.patch.multiple(mod, **changes)
        self.constants.start()
        self.funcs = mock.patch.dict(mod.FUNCTIONS,
                                     {self.name: (0x08000004, 4, 8,
                                                  self.h(self.data[4:12]).hexdigest())},
                                     clear=True)
        self.funcs.start()
        self.addCleanup(self.constants.stop)
        self.addCleanup(self.funcs.stop)

    def test_original_splat_layout_accepted(self):
        result = mod.validate_layout(self.config())
        self.assertEqual(result['overlay'], 'file_43')
        self.assertEqual(result['rom_start'], 0)

    def test_reference_input_contract_binds_splat_rom_and_sections(self):
        result = mod.validate_reference_inputs(self.config(), self.data, (self.name,))
        contract = result['input_contract']
        self.assertEqual(contract['format'], 'goemon-overlay-reference-input-v1')
        self.assertEqual(contract['overlay'], 'file_43')
        self.assertEqual(contract['splat_source_sha1'], mod.ROM_SHA1)
        self.assertEqual(contract['reference_rom_sha1'], mod.ROM_SHA1)
        self.assertEqual(contract['reference_rom_bytes'], len(self.data))
        self.assertEqual(contract['layout']['vma_start'], 0x08000000)
        self.assertEqual(contract['text_sha256'], self.h(self.data[:32]).hexdigest())
        self.assertEqual(contract['rodata_sha256'], self.h(self.data[32:48]).hexdigest())
        self.assertEqual(contract['function_instruction_sha256'][self.name],
                         mod.FUNCTIONS[self.name][3])
        self.assertEqual(result['reference_validation']['verified_original_functions'][0]['bytes'], 8)
        self.assertFalse(result['reference_validation']['promoted_matching_c'])

    def test_reference_input_contract_rejects_changed_segment_order(self):
        config = self.config()
        file43 = config.index('  - name: file_43')
        file44 = config.index('  - name: file_44')
        reordered = config[:file43] + config[file44:] + config[file43:file44]
        with self.assertRaisesRegex(ValueError, 'neighboring file_44|section layout'):
            mod.validate_reference_inputs(reordered, self.data, (self.name,))

    def test_reference_input_contract_rejects_wrong_vma(self):
        changed = self.config().replace('vram: 0x8000000', 'vram: 0x8000004')
        with self.assertRaisesRegex(ValueError, 'section layout'):
            mod.validate_reference_inputs(changed, self.data, (self.name,))

    def test_reference_input_contract_rejects_wrong_source_sha1(self):
        changed = self.config().replace(mod.ROM_SHA1, '0' * 40)
        with self.assertRaisesRegex(ValueError, 'SHA-1'):
            mod.validate_reference_inputs(changed, self.data, (self.name,))

    def test_reference_input_contract_rejects_wrong_rom_length(self):
        with self.assertRaisesRegex(ValueError, 'size or SHA-1'):
            mod.validate_reference_inputs(self.config(), self.data[:-1], (self.name,))

    def test_reference_input_contract_rejects_wrong_text_hash(self):
        with mock.patch.object(mod, 'TEXT_SHA256', 'a' * 64):
            with self.assertRaisesRegex(ValueError, 'text/rodata'):
                mod.validate_reference_inputs(self.config(), self.data, (self.name,))

    def test_reference_input_contract_rejects_wrong_rodata_hash(self):
        with mock.patch.object(mod, 'RODATA_SHA256', 'b' * 64):
            with self.assertRaisesRegex(ValueError, 'text/rodata'):
                mod.validate_reference_inputs(self.config(), self.data, (self.name,))

    def test_reference_input_contract_rejects_wrong_reference_sha1(self):
        changed = self.data[:-1] + bytes([self.data[-1] ^ 1])
        with self.assertRaisesRegex(ValueError, 'size or SHA-1'):
            mod.validate_reference_inputs(self.config(), changed, (self.name,))

    def test_splat_reference_sha_rejected(self):
        with self.assertRaisesRegex(ValueError,'SHA-1'):
            mod.validate_layout(self.config().replace(mod.ROM_SHA1, '0'*40))

    def test_wrong_overlay_id_rejected(self):
        with self.assertRaisesRegex(ValueError,'segment ID'):
            mod.validate_layout(self.config().replace('name: file_43','name: file_34'))

    def test_duplicate_overlay_rejected(self):
        with self.assertRaisesRegex(ValueError,'segment ID'):
            mod.validate_layout(self.config().replace('  - name: file_44',
                                                      '  - name: file_43\n  - name: file_44'))

    def test_wrong_vma_rejected(self):
        with self.assertRaisesRegex(ValueError,'section layout'):
            mod.validate_layout(self.config().replace('vram: 0x8000000','vram: 0x8000004'))

    def test_wrong_rodata_section_rejected(self):
        with self.assertRaisesRegex(ValueError,'section layout'):
            mod.validate_layout(self.config().replace('0x6F9CE0, rodata','0x6F9CE4, rodata'))

    def test_extra_data_section_rejected(self):
        s=self.config().replace('  - name: file_44', '    - [0x6F9CE8, data, file_43]\n  - name: file_44')
        with self.assertRaisesRegex(ValueError,'section layout'):
            mod.validate_layout(s)

    def test_moved_overlay_end_rejected(self):
        with self.assertRaisesRegex(ValueError,'overlaps or leaves a gap'):
            mod.validate_layout(self.config().replace('start: 0x6FB200','start: 0x6FB300'))

    def test_neighbor_overlay_reordered_rejected(self):
        with self.assertRaisesRegex(ValueError,'neighboring file_44'):
            mod.validate_layout(self.config().replace('  - name: file_44',
                                                      '  - name: file_45\n  - name: file_44'))

    def test_verified_original_reference_not_promotion(self):
        proof=mod.verify_reference(self.data, (self.name,))
        self.assertFalse(proof['promoted_matching_c'])
        self.assertEqual(proof['verified_original_functions'][0]['bytes'],8)

    def test_duplicate_or_empty_claim_rejected(self):
        for names in ((),(self.name,self.name)):
            with self.subTest(names=names),self.assertRaisesRegex(ValueError,'empty or duplicated'):
                mod.verify_reference(self.data,names)

    def test_unreviewed_function_rejected(self):
        with self.assertRaisesRegex(ValueError,'unreviewed'):
            mod.verify_reference(self.data, ('unknown_overlay_function',))

    def test_original_bad_bytes_rejected(self):
        changed=list(self.data);changed[4]^=1
        altered=bytes(changed)
        with self.assertRaisesRegex(ValueError,'SHA-1'):
            mod.verify_reference(altered,(self.name,))
        with mock.patch.object(mod,'ROM_SHA1',hashlib.sha1(altered).hexdigest()),\
             mock.patch.object(mod,'TEXT_SHA256',self.h(altered[:32]).hexdigest()):
            with self.assertRaisesRegex(ValueError,'instruction bytes'):
                mod.verify_reference(altered,(self.name,))

    def test_wrong_mapping_rejected(self):
        with mock.patch.dict(mod.FUNCTIONS,{self.name:(0x08000008,4,8,self.h(self.data[4:12]).hexdigest())}):
            with self.assertRaisesRegex(ValueError,'ROM-to-VMA'):
                mod.verify_reference(self.data,(self.name,))

    def test_cross_text_section_rejected(self):
        with mock.patch.dict(mod.FUNCTIONS,{self.name:(0x0800001C,28,8,self.h(self.data[28:36]).hexdigest())}):
            with self.assertRaisesRegex(ValueError,'crosses'):
                mod.verify_reference(self.data,(self.name,))

    def test_wrong_text_rodata_hash_rejected(self):
        with mock.patch.object(mod,'TEXT_SHA256','a'*64):
            with self.assertRaisesRegex(ValueError,'text/rodata'):
                mod.verify_reference(self.data,(self.name,))

    def test_incomplete_candidate_full_rom_rejected(self):
        with self.assertRaisesRegex(ValueError,'candidate full'):
            mod.compare_full_rom(self.data,self.data[:-4])

    def test_changed_candidate_full_rom_rejected(self):
        shifted=self.data[:-1]+bytes([self.data[-1]^1])
        with self.assertRaisesRegex(ValueError,'candidate full'):
            mod.compare_full_rom(self.data,shifted)

    def test_identical_candidate_full_rom_acceptance_is_not_c_proof(self):
        self.assertIsNone(mod.compare_full_rom(self.data,bytes(self.data)))
        self.assertFalse(mod.verify_reference(self.data,(self.name,))['promoted_matching_c'])


if __name__=='__main__':
    main()
