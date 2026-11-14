"""Synthetic fail-closed reference and ELF checks for USA file_12."""
import hashlib
from unittest import TestCase, mock
import struct

from decomp import overlay_file12 as mod
from decomp.elf_layout import pack_file12_callback_text
from decomp.probe import Elf32


def linked_file12_elf(data, function_name, function_vma, function_size,
                      *, section_name='.file_12', section_vma=None,
                      section_size=None, relocation_target='target',
                      alias=False, overlap=False):
    section_vma = mod.VMA_START if section_vma is None else section_vma
    section_size = len(data) if section_size is None else section_size
    section_names = (b'\0' + section_name.encode() + b'\0.rel.file_12\0'
                     b'.file_12_alias\0.unexpected_overlap\0.symtab\0'
                     b'.strtab\0.shstrtab\0')
    symbol_names = b'\0' + function_name.encode() + b'\0target\0'
    name_offsets = {name: symbol_names.index(name + b'\0')
                    for name in (function_name.encode(), b'target')}
    content = bytearray(52)

    def append(payload, alignment=4):
        content.extend(bytes((-len(content)) % alignment))
        offset = len(content)
        content.extend(payload)
        return offset

    sections = [(0,) * 10]
    overlay_offset = append(data[:section_size], 16)
    sections.append((section_names.index(section_name.encode() + b'\0'),
                     1, 7, section_vma, overlay_offset, section_size,
                     0, 0, 16, 0))
    if alias:
        alias_offset = append(data[:4], 4)
        sections.append((section_names.index(b'.file_12_alias\0'), 1, 7,
                         section_vma, alias_offset, 4, 0, 0, 4, 0))
    if overlap:
        overlap_offset = append(data[:4], 4)
        sections.append((section_names.index(b'.unexpected_overlap\0'),
                         1, 2, section_vma + 4, overlap_offset, 4,
                         0, 0, 4, 0))
    relocation_offset = append(struct.pack(
        '>II', function_vma, (2 << 8) | 4
    ))
    relocation_section_index = len(sections)
    sections.append((section_names.index(b'.rel.file_12\0'), 9, 0x40, 0,
                     relocation_offset, 8, 0, 1, 4, 8))
    symbols = [bytes(16)]
    symbols.append(struct.pack('>IIIBBH', name_offsets[function_name.encode()],
                               function_vma, function_size, 0x12, 0, 1))
    symbols.append(struct.pack('>IIIBBH', name_offsets[b'target'],
                               0x80150000, 4, 0x11, 0, 0xFFF1))
    symtab_index = len(sections)
    symtab_offset = append(b''.join(symbols), 4)
    sections.append((section_names.index(b'.symtab\0'), 2, 0, 0,
                     symtab_offset, 16 * len(symbols), 0, 1, 4, 16))
    sections[relocation_section_index] = (
        sections[relocation_section_index][0], 9, 0x40, 0,
        relocation_offset, 8, symtab_index, 1, 4, 8,
    )
    strtab_offset = append(symbol_names, 1)
    strtab_index = len(sections)
    sections.append((section_names.index(b'.strtab\0'), 3, 0, 0,
                     strtab_offset, len(symbol_names), 0, 0, 1, 0))
    sections[symtab_index] = (
        sections[symtab_index][0], 2, 0, 0, symtab_offset,
        16 * len(symbols), strtab_index, 1, 4, 16,
    )
    shstrtab_offset = append(section_names, 1)
    shstrtab_index = len(sections)
    sections.append((section_names.index(b'.shstrtab\0'), 3, 0, 0,
                     shstrtab_offset, len(section_names), 0, 0, 1, 0))
    struct.pack_into('>I', content, relocation_offset + 4, (2 << 8) | 4)
    section_headers = append(b''.join(struct.pack('>10I', *section)
                                      for section in sections), 4)
    content[:16] = b'\x7fELF\x01\x02\x01' + bytes(9)
    struct.pack_into('>HHIIIIIHHHHHH', content, 16, 2, 8, 1, 0, 0,
                     section_headers, 0, 52, 0, 0, 40, len(sections),
                     shstrtab_index)
    return bytes(content)


def relocatable_file12_callback(code, *, tail=bytes(12), text_alignment=16,
                                relocations=None,
                                function_name='func_80222034_5DD504',
                                symbol_shapes=None):
    name = function_name
    shnames = b'\0.text\0.rel.text\0.symtab\0.strtab\0.shstrtab\0'
    relocations = relocations or (
        (0, 5, 'D_8015C5E8'), (4, 6, 'D_8015C5E8'),
        (8, 5, 'D_801C7750_1C8350'), (16, 6, 'D_801C7750_1C8350'),
    )
    target_names = sorted({target for _, _, target in relocations})
    labels = ['.text', name, *target_names]
    strings = b'\0' + b'\0'.join(label.encode() for label in labels) + b'\0'
    symbol_offsets = {label: strings.index(label.encode() + b'\0') for label in labels}
    content = bytearray(52)

    def append(payload, alignment=4):
        content.extend(bytes((-len(content)) % alignment))
        offset = len(content)
        content.extend(payload)
        return offset

    text_payload = code + tail
    text_offset = append(text_payload, 16)
    target_indices = {target: 3 + index for index, target in enumerate(target_names)}
    rel_offset = append(b''.join(
        struct.pack('>II', offset, (target_indices[target] << 8) | kind)
        for offset, kind, target in relocations
    ))
    symbols = [
        bytes(16),
        struct.pack('>IIIBBH', symbol_offsets['.text'], 0, len(text_payload),
                    0x03, 0, 1),
        struct.pack('>IIIBBH', symbol_offsets[name], 0, len(code),
                    0x12, 0, 1),
    ]
    for target in target_names:
        kinds = {relocation_type for _, relocation_type, name in relocations
                 if name == target}
        shape = (symbol_shapes or {}).get(target)
        if shape is None:
            shape = ((2, 0) if kinds == {4} else
                     (1, 1 if target == 'D_801C7743' else 4))
        kind, size = shape
        symbols.append(struct.pack(
            '>IIIBBH', symbol_offsets[target], 0, size,
            (1 << 4) | kind, 0, 0,
        ))
    sym_offset = append(b''.join(symbols), 4)
    string_offset = append(strings, 1)
    shstr_offset = append(shnames, 1)
    sections = [
        (0,) * 10,
        (shnames.index(b'.text\0'), 1, 6, 0, text_offset,
         len(text_payload), 0, 0, text_alignment, 0),
        (shnames.index(b'.rel.text\0'), 9, 0, 0, rel_offset,
         8 * len(relocations), 3, 1, 4, 8),
        (shnames.index(b'.symtab\0'), 2, 0, 0, sym_offset,
         16 * len(symbols), 4, 3, 4, 16),
        (shnames.index(b'.strtab\0'), 3, 0, 0, string_offset,
         len(strings), 0, 0, 1, 0),
        (shnames.index(b'.shstrtab\0'), 3, 0, 0, shstr_offset,
         len(shnames), 0, 0, 1, 0),
    ]
    shoff = append(b''.join(struct.pack('>10I', *section)
                             for section in sections), 4)
    content[:16] = b'\x7fELF\x01\x02\x01' + bytes(9)
    struct.pack_into('>HHIIIIIHHHHHH', content, 16, 1, 8, 1, 0, 0,
                     shoff, 0, 52, 0, 0, 40, len(sections), 5)
    return bytes(content), text_offset


class OverlayFile12Tests(TestCase):
    def setUp(self):
        self.data = bytes(range(64))
        self.function = 'func_8020D2A4_0004'
        self.function_bytes = self.data[4:12]
        self.function_sha = hashlib.sha256(self.function_bytes).hexdigest()
        self.constants = mock.patch.multiple(
            mod,
            ROM_BYTES=len(self.data),
            ROM_SHA1=hashlib.sha1(self.data).hexdigest(),
            ROM_START=0,
            ROM_TEXT_END=16,
            ROM_END=32,
            TEXT_SHA256=hashlib.sha256(self.data[:16]).hexdigest(),
            DATA_SHA256=hashlib.sha256(self.data[16:32]).hexdigest(),
            REFERENCE_ELF_SHA256='0' * 64,
        )
        self.constants.start()
        self.functions = mock.patch.dict(
            mod.FUNCTIONS,
            {self.function: (mod.VMA_START + 4, 4, 8, self.function_sha)},
            clear=True,
        )
        self.functions.start()
        self.relocations = mock.patch.dict(
            mod.FUNCTION_RELOCATIONS,
            {self.function: ((0, 4, 'target'),)},
            clear=True,
        )
        self.relocations.start()
        self.addCleanup(self.constants.stop)
        self.addCleanup(self.functions.stop)
        self.addCleanup(self.relocations.stop)
        self.elf = linked_file12_elf(
            self.data[:32], self.function, mod.VMA_START + 4, 8,
        )
        self.constants = mock.patch.object(
            mod, 'REFERENCE_ELF_SHA256', hashlib.sha256(self.elf).hexdigest()
        )
        self.constants.start()
        self.addCleanup(self.constants.stop)

    def config(self):
        return (f"sha1: {mod.ROM_SHA1}\nsegments:\n"
                "  - name: file_11\n"
                "  - name: file_12\n" +
                "\n".join("    " + line for line in mod.EXPECTED_SEGMENT_LINES) + "\n"
                "  - name: file_13\n    start: 0x5F6840\n"
                "  - name: file_14\n")

    def test_reference_layout_and_text_data_contract(self):
        contract = mod.validate_reference_inputs(self.config(), self.data,
                                                 (self.function,))
        self.assertEqual(contract['input_contract']['overlay'], 'file_12')
        self.assertEqual(contract['input_contract']['layout']['ram_id'],
                         'static_overlay_2')
        self.assertEqual(contract['input_contract']['layout']['data_bytes'], 16)
        self.assertFalse(contract['reference_validation']['promoted_matching_c'])

    def test_relocation_metadata_normalizations_are_narrow_and_fail_closed(self):
        data_original = (0, 5, 'D_8015C5E8', 0x8015C5E8, '.data',
                         0, 1, False, 0)
        data_candidate = (*data_original[:5], 1, *data_original[6:])
        normalized = mod._relocation_metadata_normalizations(
            (data_original,), (data_candidate,),
        )
        self.assertEqual(normalized['notype_to_object_data_symbols'], 1)
        self.assertEqual(normalized['absolute_to_overlay_tail_alias'], 0)

        tail_vma = mod.VMA_START + mod.TEXT_END_ALIAS[0] - mod.ROM_START
        tail_name = mod.TEXT_END_ALIAS[2]
        tail_original = (4, 5, tail_name, tail_vma, 'SHN_FFF1',
                         0, 1, False, 0)
        tail_candidate = (*tail_original[:4], '.file_12', *tail_original[5:])
        normalized = mod._relocation_metadata_normalizations(
            (tail_original,), (tail_candidate,),
        )
        self.assertEqual(normalized['notype_to_object_data_symbols'], 0)
        self.assertEqual(normalized['absolute_to_overlay_tail_alias'], 1)

        rejected = (
            (*tail_candidate[:3], tail_candidate[3] + 4, *tail_candidate[4:]),
            (*tail_candidate[:1], tail_candidate[1] + 1, *tail_candidate[2:]),
            (*tail_candidate[:2], 'unrelated_alias', *tail_candidate[3:]),
            (*tail_candidate[:6], tail_candidate[6] + 1, *tail_candidate[7:]),
            (*tail_candidate[:4], '.other_overlay', *tail_candidate[5:]),
        )
        for candidate in rejected:
            with self.subTest(candidate=candidate):
                with self.assertRaisesRegex(
                    ValueError, 'metadata changed beyond approved aliases',
                ):
                    mod._relocation_metadata_normalizations(
                        (tail_original,), (candidate,),
                    )

    def test_callback_packer_trims_only_zero_tail_size_and_alignment_metadata(self):
        code = bytes(range(20))
        expected_relocations = (
            (0, 5, 'D_8015C5E8'), (4, 6, 'D_8015C5E8'),
            (8, 5, 'D_801C7750_1C8350'),
            (16, 6, 'D_801C7750_1C8350'),
        )
        original, text_offset = relocatable_file12_callback(code)
        packed, evidence = pack_file12_callback_text(
            original, 'func_80222034_5DD504', 20, expected_relocations,
        )
        elf = Elf32(packed)
        text_index = elf.names.index('.text')
        self.assertEqual(elf.sections[text_index][5], 20)
        self.assertEqual(elf.sections[text_index][8], 4)
        self.assertEqual(original[text_offset:text_offset + 32],
                         packed[text_offset:text_offset + 32])
        self.assertEqual(evidence['zero_padding_bytes'], 12)
        self.assertEqual(evidence['relocations_retained'], 4)
        changed = [offset for offset, (before, after) in
                   enumerate(zip(original, packed)) if before != after]
        header = struct.unpack_from('>I', original, 32)[0]
        allowed = (set(range(header + text_index * 40 + 20,
                             header + text_index * 40 + 24)) |
                   set(range(header + text_index * 40 + 32,
                             header + text_index * 40 + 36)))
        self.assertTrue(changed)
        self.assertTrue(all(offset in allowed for offset in changed))

    def test_callback_packer_checks_call_and_signed_byte_relocation_shapes(self):
        name='func_80222168_5DD638'
        relocations=(
            (8,5,'D_801C7743'),
            (16,6,'D_801C7743'),
            (12,4,'func_801DCD48_598C58'),
        )
        raw,_=relocatable_file12_callback(
            bytes(range(36)), relocations=relocations, function_name=name,
            symbol_shapes=mod.FUNCTION_RELOCATION_SYMBOLS[name],
        )
        expected=((8,5,'D_801C7743'),(12,4,'func_801DCD48_598C58'),
                  (16,6,'D_801C7743'))
        with mock.patch.dict(mod.FUNCTION_RELOCATIONS,{name:expected},clear=True):
            packed,evidence=pack_file12_callback_text(
                raw,name,36,expected,mod.FUNCTION_RELOCATION_SYMBOLS[name],
            )
        elf=Elf32(packed)
        text=elf.sections[elf.names.index('.text')]
        self.assertEqual((text[5],text[8]),(36,4))
        self.assertEqual(evidence['relocations_retained'],3)
        wrong_shapes=dict(mod.FUNCTION_RELOCATION_SYMBOLS[name])
        wrong_shapes['D_801C7743']=(1,4)
        with self.assertRaisesRegex(ValueError,'relocation symbol'):
            with mock.patch.dict(mod.FUNCTION_RELOCATIONS,{name:expected},clear=True):
                pack_file12_callback_text(raw,name,36,expected,wrong_shapes)

    def test_callback_packer_rejects_nonzero_padding_and_wrong_relocations(self):
        code = bytes(range(20))
        expected = ((0, 5, 'D_8015C5E8'), (4, 6, 'D_8015C5E8'),
                    (8, 5, 'D_801C7750_1C8350'),
                    (16, 6, 'D_801C7750_1C8350'))
        source, text_offset = relocatable_file12_callback(code)
        changed = bytearray(source)
        changed[text_offset + 20] = 1
        with self.assertRaisesRegex(ValueError, 'Unexpected file_12 callback padding'):
            pack_file12_callback_text(
                bytes(changed), 'func_80222034_5DD504', 20, expected,
            )
        wrong = ((0, 5, 'D_8015C5E8'), (4, 6, 'D_8015C5E8'),
                 (8, 5, 'D_801C7750_1C8350'),
                 (24, 6, 'D_801C7750_1C8350'))
        with self.assertRaisesRegex(ValueError, 'relocation signatures'):
            pack_file12_callback_text(
                source, 'func_80222034_5DD504', 20, wrong,
            )

    def test_layout_rejects_duplicate_segment_or_wrong_neighbor(self):
        duplicate = self.config().replace(
            "  - name: file_13\n", "  - name: file_12\n  - name: file_13\n"
        )
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            mod.validate_layout(duplicate)
        shifted = self.config().replace('0x5F6840', '0x5F6850')
        with self.assertRaisesRegex(ValueError, 'ROM end'):
            mod.validate_layout(shifted)

    def test_linked_provenance_accepts_exact_section_function_and_relocation(self):
        proof = mod.validate_linked_elf_provenance(
            self.config(), self.data, self.elf, self.elf, (self.function,)
        )['linked_elf_provenance']
        self.assertEqual(proof['reference_section']['size'], 32)
        self.assertTrue(proof['full_section_relocations_match'])
        self.assertEqual(proof['functions'][0]['relocation_count'], 1)
        self.assertFalse(proof['promoted_matching_c'])

    def test_linked_provenance_rejects_alias_overlap_and_relocation_change(self):
        alias = linked_file12_elf(
            self.data[:32], self.function, mod.VMA_START + 4, 8, alias=True,
        )
        with self.assertRaisesRegex(ValueError, 'section aliases'):
            mod.validate_linked_elf_provenance(
                self.config(), self.data, self.elf, alias, (self.function,)
            )
        overlap = linked_file12_elf(
            self.data[:32], self.function, mod.VMA_START + 4, 8, overlap=True,
        )
        with self.assertRaisesRegex(ValueError, 'overlapping .file_12'):
            mod.validate_linked_elf_provenance(
                self.config(), self.data, self.elf, overlap, (self.function,)
            )
        changed_reloc = bytearray(self.elf)
        elf = Elf32(changed_reloc)
        rel_index = elf.names.index('.rel.file_12')
        rel = elf.sections[rel_index]
        struct.pack_into('>I', changed_reloc, rel[4] + 4, (1 << 8) | 4)
        with self.assertRaisesRegex(ValueError, 'relocation target'):
            mod.validate_linked_elf_provenance(
                self.config(), self.data, self.elf, bytes(changed_reloc),
                (self.function,),
            )

    def test_linked_provenance_rejects_whole_section_byte_change(self):
        changed_data = bytearray(self.data[:32])
        changed_data[24] ^= 1
        changed = linked_file12_elf(
            bytes(changed_data), self.function, mod.VMA_START + 4, 8,
        )
        with self.assertRaisesRegex(ValueError, r'whole|\.file_12 bytes'):
            mod.validate_linked_elf_provenance(
                self.config(), self.data, self.elf, changed, (self.function,)
            )


if __name__ == '__main__':
    import unittest
    unittest.main()
