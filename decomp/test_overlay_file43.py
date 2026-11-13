"""Synthetic fail-closed layout guards; no private ROM or generated ASM needed."""
import hashlib
from pathlib import Path
import struct
from unittest import TestCase, main, mock

try:
    from . import overlay_file43 as mod
except ImportError:
    import overlay_file43 as mod


def linked_overlay_elf(data, *, section_name='.file_43', section_vma=0x08000000,
                       section_size=48, section_alias=False, include_function=True,
                       function_vma=0x08000004, function_size=8,
                       function_alias=False, relocation_target=2,
                       relocation_target_section=1, overlap_section=False,
                       sibling_overlay=False):
    """Build a small linked MIPS ELF carrying a file_43 section and REL table."""
    shnames = (b'\0' + section_name.encode() +
               b'\0.rel.file_43\0.file_43_alias\0.file_44\0.unexpected_overlap\0'
               b'.symtab\0.strtab\0.shstrtab\0')
    names = b'\0func_08000004_0004\0func_alias\0target\0target2\0'
    string_offsets = {name: names.index(name + b'\0') for name in (
        b'func_08000004_0004', b'func_alias', b'target', b'target2')}
    content = bytearray(52)

    def append(payload, alignment=4):
        content.extend(bytes((-len(content)) % alignment))
        offset = len(content)
        content.extend(payload)
        return offset

    sections = [(0,) * 10]
    section_offset = append(data[:section_size], 16)
    sections.append((shnames.index(section_name.encode() + b'\0'), 1, 7, section_vma,
                     section_offset, section_size, 0, 0, 16, 0))
    if sibling_overlay:
        sibling_offset = append(data[12:16], 4)
        sections.append((shnames.index(b'.file_44\0'), 1, 7, section_vma,
                         sibling_offset, 4, 0, 0, 4, 0))
    relocation_offset = append(struct.pack('>II', function_vma,
                                           (relocation_target << 8) | 2))
    relocation_section_index = len(sections)
    sections.append((shnames.index(b'.rel.file_43\0'), 9, 0x40, 0,
                     relocation_offset, 8, 0, 1, 4, 8))
    if section_alias:
        alias_offset = append(data[4:8], 4)
        sections.append((shnames.index(b'.file_43_alias\0'), 1, 7,
                         section_vma + 4, alias_offset, 4, 0, 0, 4, 0))
    if overlap_section:
        overlap_offset = append(data[8:12], 4)
        sections.append((shnames.index(b'.unexpected_overlap\0'), 1, 7,
                         section_vma + 8, overlap_offset, 4, 0, 0, 4, 0))

    symbols = [bytes(16)]
    if include_function:
        symbols.append(struct.pack('>IIIBBH', string_offsets[b'func_08000004_0004'],
                                   function_vma, function_size, 0x12, 0, 1))
        if function_alias:
            symbols.append(struct.pack('>IIIBBH', string_offsets[b'func_alias'],
                                       function_vma, function_size, 0x12, 0, 1))
    target_index = len(symbols)
    symbols.append(struct.pack('>IIIBBH', string_offsets[b'target'],
                               0x08000030 if relocation_target_section else 0,
                               4, 0x12, 0, relocation_target_section))
    second_target_index = len(symbols)
    symbols.append(struct.pack('>IIIBBH', string_offsets[b'target2'],
                               0x08000034, 4, 0x12, 0, 1))
    relocation_symbol_index = target_index if relocation_target == 2 else (
        second_target_index if relocation_target == 3 else relocation_target)
    struct.pack_into('>I', content, relocation_offset + 4,
                     (relocation_symbol_index << 8) | 2)

    symtab_index = len(sections)
    symtab_offset = append(b''.join(symbols), 4)
    sections.append((shnames.index(b'.symtab\0'), 2, 0, 0, symtab_offset,
                     16 * len(symbols), 0, 1, 4, 16))
    sections[relocation_section_index] = (
        sections[relocation_section_index][0], sections[relocation_section_index][1],
        sections[relocation_section_index][2], sections[relocation_section_index][3],
        sections[relocation_section_index][4], sections[relocation_section_index][5],
        symtab_index, sections[relocation_section_index][7],
        sections[relocation_section_index][8], sections[relocation_section_index][9])
    strtab_offset = append(names, 1)
    sections.append((shnames.index(b'.strtab\0'), 3, 0, 0, strtab_offset,
                     len(names), 0, 0, 1, 0))
    strtab_index = len(sections) - 1
    sections[symtab_index] = (sections[symtab_index][0], sections[symtab_index][1],
                              sections[symtab_index][2], sections[symtab_index][3],
                              sections[symtab_index][4], sections[symtab_index][5],
                              strtab_index, sections[symtab_index][7],
                              sections[symtab_index][8], sections[symtab_index][9])
    shstrtab_offset = append(shnames, 1)
    sections.append((shnames.index(b'.shstrtab\0'), 3, 0, 0, shstrtab_offset,
                     len(shnames), 0, 0, 1, 0))
    shstrtab_index = len(sections) - 1
    section_headers = append(b''.join(struct.pack('>10I', *section)
                                      for section in sections), 4)
    content[:16] = b'\x7fELF\x01\x02\x01' + bytes(9)
    struct.pack_into('>HHIIIIIHHHHHH', content, 16, 2, 8, 1, 0, 0,
                     section_headers, 0, 52, 0, 0, 40, len(sections), shstrtab_index)
    return bytes(content)


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
        self.name = 'func_08000004_0004'
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

    def test_reference_input_contract_rejects_wrong_id_rodata_shift_and_padding(self):
        configs = (
            self.config().replace('  - name: file_43', '  - name: file_34'),
            self.config().replace('0x6F9CE0, rodata', '0x6F9CE4, rodata'),
            self.config().replace('subalign: 16', 'subalign: 8'),
            self.config().replace(
                '  - name: file_44',
                '  - name: file_43_alias\n    type: code\n    start: 0x6FB200\n'
                '  - name: file_44'),
        )
        for changed in configs:
            with self.subTest(config=changed), self.assertRaises(ValueError):
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

    def test_linked_elf_provenance_accepts_exact_overlay_symbols_and_relocations(self):
        reference_elf = linked_overlay_elf(self.data, sibling_overlay=True)
        with mock.patch.object(mod, 'REFERENCE_ELF_SHA256',
                               hashlib.sha256(reference_elf).hexdigest()):
            result = mod.validate_linked_elf_provenance(
                self.config(), self.data, reference_elf, reference_elf, (self.name,)
            )
        proof = result['linked_elf_provenance']
        self.assertEqual(proof['reference_section']['vma_start'], '0x08000000')
        self.assertEqual(proof['reference_section']['size'], 48)
        self.assertEqual(proof['functions'][0]['section'], '.file_43')
        self.assertTrue(proof['functions'][0]['candidate_code_matches_original'])
        self.assertTrue(proof['functions'][0]['candidate_relocations_match_reference'])
        self.assertEqual(proof['functions'][0]['relocation_count'], 1)
        self.assertEqual(proof['functions'][0]['relocations'][0]['symbol'], 'target')
        self.assertFalse(proof['promoted_matching_c'])

    def test_linked_elf_rejects_unpinned_reference_elf_identity(self):
        reference_elf = linked_overlay_elf(self.data)
        with mock.patch.object(mod, 'REFERENCE_ELF_SHA256', 'f' * 64):
            with self.assertRaisesRegex(ValueError, 'reference linked ELF identity'):
                mod.validate_linked_elf_provenance(
                    self.config(), self.data, reference_elf, reference_elf, (self.name,)
                )

    def test_linked_elf_rejects_shifted_overlay_vma(self):
        reference_elf = linked_overlay_elf(self.data)
        candidate_elf = linked_overlay_elf(self.data, section_vma=0x08000004)
        with mock.patch.object(mod, 'REFERENCE_ELF_SHA256',
                               hashlib.sha256(reference_elf).hexdigest()):
            with self.assertRaisesRegex(ValueError, 'VMA, flags'):
                mod.validate_linked_elf_provenance(
                    self.config(), self.data, reference_elf, candidate_elf, (self.name,)
                )

    def test_linked_elf_rejects_wrong_overlay_section_size(self):
        reference_elf = linked_overlay_elf(self.data)
        candidate_elf = linked_overlay_elf(self.data, section_size=44)
        with mock.patch.object(mod, 'REFERENCE_ELF_SHA256',
                               hashlib.sha256(reference_elf).hexdigest()):
            with self.assertRaisesRegex(ValueError, 'VMA, flags'):
                mod.validate_linked_elf_provenance(
                    self.config(), self.data, reference_elf, candidate_elf, (self.name,)
                )

    def test_linked_elf_rejects_file43_id_alias_and_overlay_padding(self):
        reference_elf = linked_overlay_elf(self.data)
        candidates = (
            (linked_overlay_elf(self.data, section_name='.file_34'),
             'one .file_43 output section'),
            (linked_overlay_elf(self.data, section_alias=True),
             'section aliases'),
            (linked_overlay_elf(self.data, overlap_section=True),
             'allocated section overlapping'),
            (linked_overlay_elf(self.data, section_size=52),
             'VMA, flags'),
        )
        with mock.patch.object(mod, 'REFERENCE_ELF_SHA256',
                               hashlib.sha256(reference_elf).hexdigest()):
            for candidate_elf, message in candidates:
                with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                    mod.validate_linked_elf_provenance(
                        self.config(), self.data, reference_elf, candidate_elf, (self.name,)
                    )

    def test_linked_elf_rejects_changed_unclaimed_text_or_rodata_bytes(self):
        reference_elf = linked_overlay_elf(self.data)
        # Exercise bytes outside the requested function at both section tails:
        # the text tail (offset 31) and a rodata byte (offset 40).
        for offset in (31, 40):
            changed = bytearray(self.data)
            changed[offset] ^= 1
            candidate_elf = linked_overlay_elf(bytes(changed))
            with mock.patch.object(mod, 'REFERENCE_ELF_SHA256',
                                   hashlib.sha256(reference_elf).hexdigest()):
                with self.subTest(offset=offset), self.assertRaisesRegex(
                        ValueError, r'candidate ELF \.file_43 bytes differ'):
                    mod.validate_linked_elf_provenance(
                        self.config(), self.data, reference_elf, candidate_elf, (self.name,)
                    )

    def test_linked_elf_rejects_missing_function_symbol(self):
        reference_elf = linked_overlay_elf(self.data)
        candidate_elf = linked_overlay_elf(self.data, include_function=False)
        with mock.patch.object(mod, 'REFERENCE_ELF_SHA256',
                               hashlib.sha256(reference_elf).hexdigest()):
            with self.assertRaisesRegex(ValueError, 'Missing/ambiguous function'):
                mod.validate_linked_elf_provenance(
                    self.config(), self.data, reference_elf, candidate_elf, (self.name,)
                )

    def test_linked_elf_rejects_changed_relocation_target(self):
        reference_elf = linked_overlay_elf(self.data)
        candidate_elf = linked_overlay_elf(self.data, relocation_target=3)
        with mock.patch.object(mod, 'REFERENCE_ELF_SHA256',
                               hashlib.sha256(reference_elf).hexdigest()):
            with self.assertRaisesRegex(ValueError, 'relocation target differs'):
                mod.validate_linked_elf_provenance(
                    self.config(), self.data, reference_elf, candidate_elf, (self.name,)
                )

    def test_linked_elf_rejects_changed_undefined_relocation(self):
        reference_elf = linked_overlay_elf(self.data)
        candidate_elf = linked_overlay_elf(self.data, relocation_target_section=0)
        with mock.patch.object(mod, 'REFERENCE_ELF_SHA256',
                               hashlib.sha256(reference_elf).hexdigest()):
            with self.assertRaisesRegex(ValueError, 'relocation target differs'):
                mod.validate_linked_elf_provenance(
                    self.config(), self.data, reference_elf, candidate_elf, (self.name,)
                )

    def test_linked_elf_rejects_duplicate_function_bounds(self):
        reference_elf = linked_overlay_elf(self.data)
        candidate_elf = linked_overlay_elf(self.data, function_alias=True)
        with mock.patch.object(mod, 'REFERENCE_ELF_SHA256',
                               hashlib.sha256(reference_elf).hexdigest()):
            with self.assertRaisesRegex(ValueError, 'overlapping function alias'):
                mod.validate_linked_elf_provenance(
                    self.config(), self.data, reference_elf, candidate_elf, (self.name,)
                )

    def test_linked_elf_rejects_function_symbol_size_lie(self):
        reference_elf = linked_overlay_elf(self.data)
        candidate_elf = linked_overlay_elf(self.data, function_size=4)
        with mock.patch.object(mod, 'REFERENCE_ELF_SHA256',
                               hashlib.sha256(reference_elf).hexdigest()):
            with self.assertRaisesRegex(ValueError, 'symbol/section differs'):
                mod.validate_linked_elf_provenance(
                    self.config(), self.data, reference_elf, candidate_elf, (self.name,)
                )

    def test_linked_elf_rejects_changed_function_bytes(self):
        reference_elf = linked_overlay_elf(self.data)
        changed = bytearray(self.data)
        changed[4] ^= 1
        candidate_elf = linked_overlay_elf(bytes(changed))
        with mock.patch.object(mod, 'REFERENCE_ELF_SHA256',
                               hashlib.sha256(reference_elf).hexdigest()):
            with self.assertRaisesRegex(ValueError, 'candidate ELF function bytes differ'):
                mod.validate_linked_elf_provenance(
                    self.config(), self.data, reference_elf, candidate_elf, (self.name,)
                )

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
