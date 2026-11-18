import copy
import hashlib
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest import mock

from decomp import overlay_file43, overlay_file12, overlay_file13
from decomp.verify import (
    load_manifest, apply_units, parse_symbols, compare_images, claimed_functions,
    main_claimed_functions, validate_file43_stage_definition, validate_file43_stage,
    stage_file43_splat, verify_file43_ownership, append_file43_function_comparison,
    verify_file43_stage_build, require_file43_full_rom_match,
    lower_file43_text_alignment, prepare_file43_stage_objects,
    manifest_file12_stages, file11_stage_mode, stage_file12_splats,
    validate_file12_stage_definition, validate_file12_stage, stage_file12_splat,
    patch_file12_tail_alias_sources,
    _file12_stages_layout,
    lower_file12_text_alignment, prepare_file12_stage_objects,
    verify_file12_ownership, verify_file12_stage_build,
    append_file12_function_comparison, require_file12_full_rom_match,
    manifest_file13_stages, crossregion47_stage,
    validate_file13_stage_definition,
    COLLISION_GATE_PATCH,
)
from decomp.test_overlay_file12 import relocatable_file12_callback

ROOT=Path(__file__).resolve().parents[1]

def cross_claim_count(manifest):
    fixture = crossregion47_stage(manifest)
    return len(fixture['functions']) if fixture else 0


def file43_stage(*, source='candidates/key_spawn_gate.c', source_sha256='a'*64,
                 compiler_object_sha256='c'*64, object_sha256='b'*64):
    name='func_080001BC_6F369C'
    vma, offset, size, _ = overlay_file43.FUNCTIONS[name]
    return {
        'format': 'goemon-file43-c-stage-v1',
        'source': source,
        'source_sha256': source_sha256,
        'compiler_object_sha256': compiler_object_sha256,
        'object_sha256': object_sha256,
        'function': {'name': name, 'rom_offset': offset, 'vma': vma, 'size': size},
    }


def file12_stage(*, name='func_80222034_5DD504',
                 source='candidates/file12_dialogue_copy.c', source_sha256='a'*64,
                 compiler_object_sha256='c'*64, object_sha256='b'*64):
    vma, offset, size, _ = overlay_file12.FUNCTIONS[name]
    return {
        'format': 'goemon-file12-c-stage-v1',
        'source': source,
        'source_sha256': source_sha256,
        'compiler_object_sha256': compiler_object_sha256,
        'object_sha256': object_sha256,
        'function': {'name': name, 'rom_offset': offset, 'vma': vma, 'size': size},
    }


def file13_stage(*, source='impact_hp_clamp.c', source_sha256='a'*64,
                 compiler_object_sha256='c'*64, object_sha256='b'*64):
    name='func_801D3954_5FED34'
    vma, offset, size, _ = overlay_file13.FUNCTIONS[name]
    return {
        'format': 'goemon-file13-c-stage-v1',
        'source': source,
        'source_sha256': source_sha256,
        'compiler_object_sha256': compiler_object_sha256,
        'object_sha256': object_sha256,
        'function': {'name': name, 'rom_offset': offset, 'vma': vma, 'size': size},
    }


def relocatable_function_object(functions=(), *, text_alignment=4):
    """Small ELF32 MIPS object fixture with one executable .text section."""
    symbol_names = [name.encode() for name, _ in functions]
    strtab = b'\0' + b'\0'.join(symbol_names) + (b'\0' if symbol_names else b'')
    sym_offsets = {}
    for name in symbol_names:
        sym_offsets[name] = strtab.index(name + b'\0')
    shnames = b'\0.text\0.symtab\0.strtab\0.shstrtab\0'
    content = bytearray(52)

    def append(payload, alignment=4):
        content.extend(bytes((-len(content)) % alignment))
        offset = len(content)
        content.extend(payload)
        return offset

    text_bytes = b''.join(code for _, code in functions) or bytes(4)
    text_offset = append(text_bytes, 4)
    symbols = [bytes(16)]
    value = 0
    for name, code in functions:
        symbols.append(struct.pack('>IIIBBH', sym_offsets[name.encode()], value,
                                   len(code), 0x12, 0, 1))
        value += len(code)
    symtab_offset = append(b''.join(symbols), 4)
    strtab_offset = append(strtab, 1)
    shstrtab_offset = append(shnames, 1)
    sections = [
        (0,) * 10,
        (shnames.index(b'.text\0'), 1, 6, 0, text_offset, len(text_bytes), 0, 0, text_alignment, 0),
        (shnames.index(b'.symtab\0'), 2, 0, 0, symtab_offset,
         16 * len(symbols), 3, 1, 4, 16),
        (shnames.index(b'.strtab\0'), 3, 0, 0, strtab_offset, len(strtab), 0, 0, 1, 0),
        (shnames.index(b'.shstrtab\0'), 3, 0, 0, shstrtab_offset,
         len(shnames), 0, 0, 1, 0),
    ]
    section_headers = append(b''.join(struct.pack('>10I', *section)
                                      for section in sections), 4)
    content[:16] = b'\x7fELF\x01\x02\x01' + bytes(9)
    struct.pack_into('>HHIIIIIHHHHHH', content, 16, 1, 8, 1, 0, 0,
                     section_headers, 0, 52, 0, 0, 40, len(sections), 4)
    return bytes(content)


def native_claim_count(manifest):
    from decomp.overlay_native87 import load_fixture
    return len(load_fixture()['functions']) if manifest.get('overlay_native87_stage') is not None else 0


class DecompVerificationTests(unittest.TestCase):
    def test_file43_stage_definition_is_explicit_and_fail_closed(self):
        manifest=load_manifest(ROOT/'decomp/manifest.json')
        stage=manifest['overlay_file43_stage']
        self.assertEqual(stage['function']['name'],'func_080001BC_6F369C')
        self.assertIn(stage['function'],claimed_functions(manifest))
        disabled=copy.deepcopy(manifest);disabled['overlay_file43_stage']=None
        self.assertEqual(len(claimed_functions(disabled)),
                         len(main_claimed_functions(disabled))+
                         sum(374 if st['format']=='goemon-file12-registration-374-v1' else 1 for st in manifest_file12_stages(disabled))+(file11_stage_mode(disabled) or 0)+
                         len(manifest_file13_stages(disabled)) + cross_claim_count(disabled) + native_claim_count(disabled))
        self.assertEqual(validate_file43_stage_definition(stage).as_posix(),
                         'candidates/key_spawn_gate.c')
        staged=copy.deepcopy(manifest);staged['overlay_file43_stage']=stage
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'manifest.json'
            path.write_text(json.dumps(staged))
            loaded=load_manifest(path)
            self.assertIn(stage['function'],claimed_functions(loaded))
            self.assertEqual(len(claimed_functions(loaded)),
                             len(main_claimed_functions(loaded))+
                             1+sum(374 if st['format']=='goemon-file12-registration-374-v1' else 1 for st in manifest_file12_stages(loaded))+(file11_stage_mode(loaded) or 0)+
                             len(manifest_file13_stages(loaded)) + cross_claim_count(loaded) + native_claim_count(loaded))
            bad=copy.deepcopy(staged)
            bad['overlay_file43_stage']['function']['vma']+=4
            path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError,'pinned extent'):
                load_manifest(path)
            bad=copy.deepcopy(staged)
            bad['overlay_file43_stage']['source']='../escape.c'
            path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError,'source path'):
                load_manifest(path)
            bad=copy.deepcopy(staged)
            bad['overlay_file43_stage']['object_sha256']='not-a-hash'
            path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError,'object_sha256'):
                load_manifest(path)

    def test_file12_stage_definition_is_explicit_and_fail_closed(self):
        manifest=load_manifest(ROOT/'decomp/manifest.json')
        stages=manifest_file12_stages(manifest)
        promoted=json.loads((ROOT/'decomp/results/usa_file12_spatial_11_promotion_20261117.json').read_text())['functions']
        self.assertEqual([stage['function']['name'] for stage in stages], [
            'file12_registration_374', *(row['name'] for row in promoted),
            'func_80222034_5DD504', 'func_80222168_5DD638',
        ])
        self.assertEqual(validate_file12_stage_definition(stages[0]).as_posix(),
                         'candidates/file12_reg374.c')
        stage=stages[-2]
        self.assertEqual(stage['function']['name'],'func_80222034_5DD504')
        self.assertIn(stage['function'],claimed_functions(manifest))
        self.assertEqual(validate_file12_stage_definition(stage).as_posix(),
                         'candidates/file12_dialogue_copy.c')
        self.assertEqual(validate_file12_stage_definition(stages[-1]).as_posix(),
                         'candidates/file12_dialogue_call.c')
        self.assertEqual(len(claimed_functions(manifest)),
                         len(main_claimed_functions(manifest))+1+sum(374 if st['format']=='goemon-file12-registration-374-v1' else 1 for st in stages)+
                         (file11_stage_mode(manifest) or 0)+len(manifest_file13_stages(manifest)) + cross_claim_count(manifest) + native_claim_count(manifest))
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'manifest.json'
            bad=copy.deepcopy(manifest)
            bad['overlay_file12_stages'][1]['function']['vma']+=4
            path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError,'pinned extent'):
                load_manifest(path)
            bad=copy.deepcopy(manifest)
            bad['overlay_file12_stages'][1]['source']='../escape.c'
            path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError,'source path'):
                load_manifest(path)
            bad=copy.deepcopy(manifest)
            bad['overlay_file12_stages'][1]['object_sha256']='not-a-hash'
            path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError,'object_sha256'):
                load_manifest(path)
            bad=copy.deepcopy(manifest)
            bad['overlay_file12_stages'].reverse()
            path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError,'Overlapping or unordered|Unreviewed file_13 extension'):
                load_manifest(path)
            bad=copy.deepcopy(manifest)
            bad['overlay_file12_stage']=bad['overlay_file12_stages'][0]
            path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError,'only one file_12 stage'):
                load_manifest(path)

    def test_file13_stage_definition_is_explicit_and_fail_closed(self):
        manifest=load_manifest(ROOT/'decomp/manifest.json')
        stages=manifest_file13_stages(manifest)
        self.assertEqual([stage['function']['name'] for stage in stages], [
            'func_801D3954_5FED34', 'func_801D3A44_5FEE24',
        ])
        for stage,source in zip(stages,('impact_hp_clamp.c','impact_hp_floor_return.c')):
            self.assertIn(stage['function'],claimed_functions(manifest))
            self.assertEqual(validate_file13_stage_definition(stage).as_posix(),source)
        self.assertEqual(len(claimed_functions(manifest)),
                         len(main_claimed_functions(manifest))+
                         (manifest.get('overlay_file43_stage') is not None)+
                         sum(374 if st['format']=='goemon-file12-registration-374-v1' else 1 for st in manifest_file12_stages(manifest))+(file11_stage_mode(manifest) or 0)+len(stages) + cross_claim_count(manifest) + native_claim_count(manifest))
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'manifest.json'
            for field,value,pattern in (
                ('vma',stages[1]['function']['vma']+4,'pinned extent'),
                ('source','../escape.c','Unsafe file_13'),
                ('object_sha256','not-a-hash','object_sha256'),
            ):
                bad=copy.deepcopy(manifest)
                if field=='vma':
                    bad['overlay_file13_stages'][1]['function'][field]=value
                else:
                    bad['overlay_file13_stages'][1][field]=value
                path.write_text(json.dumps(bad))
                with self.subTest(field=field),self.assertRaisesRegex(ValueError,pattern):
                    load_manifest(path)
            bad=copy.deepcopy(manifest)
            bad['overlay_file13_stages'].reverse()
            path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError,'Overlapping or unordered|Unreviewed file_13 extension'):
                load_manifest(path)

    def test_file12_splat_split_preserves_data_and_neighbor(self):
        original=(
            'sha1: '+overlay_file12.ROM_SHA1+'\nsegments:\n'
            '  - name: file_12\n'
            '    type: code\n    start: 0x5C8770\n    vram: 0x8020D2A0\n'
            '    bss_size: 0xE0\n    subalign: 16\n    overlay: yes\n'
            '    exclusive_ram_id: static_overlay_2\n    subsegments:\n'
            '    - [0x5C8770, asm]\n    - [0x5E3C90, data]\n'
            '  - name: file_13\n    start: 0x5F6840\n')
        updated,before,after=stage_file12_splat(original,file12_stage())
        self.assertEqual((before,after),
                         ('file_12_before_5DD504','file_12_after_5DD518'))
        self.assertIn('    subalign: null\n',updated)
        self.assertIn('    - [0x5C8770, asm, file_12_before_5DD504]\n'
                      '    - [0x5DD504, c, file12_dialogue_copy]\n'
                      '    - [0x5DD518, asm, file_12_after_5DD518]\n'
                      '    - [0x5E3C90, data, file_12]\n',updated)
        self.assertEqual(updated.split('  - name: file_13\n',1)[1],
                         original.split('  - name: file_13\n',1)[1])
        with self.assertRaisesRegex(ValueError,'VMA, ROM, overlay ID'):
            stage_file12_splat(original.replace('0x5E3C90','0x5E3C94'),file12_stage())

    def test_file12_splat_multiple_callbacks_preserves_intervening_assembly(self):
        original=(
            'sha1: '+overlay_file12.ROM_SHA1+'\nsegments:\n'
            '  - name: file_12\n'
            '    type: code\n    start: 0x5C8770\n    vram: 0x8020D2A0\n'
            '    bss_size: 0xE0\n    subalign: 16\n    overlay: yes\n'
            '    exclusive_ram_id: static_overlay_2\n    subsegments:\n'
            '    - [0x5C8770, asm]\n    - [0x5E3C90, data]\n'
            '  - name: file_13\n    start: 0x5F6840\n')
        stages=[file12_stage(),file12_stage(
            name='func_80222168_5DD638',
            source='candidates/file12_dialogue_call.c',
        )]
        updated,assembly=stage_file12_splats(original,stages)
        self.assertEqual(assembly,(
            'file_12_before_5DD504',
            'file_12_gap_5DD518_5DD638',
            'file_12_after_5DD65C',
        ))
        for line in (
            '    - [0x5DD504, c, file12_dialogue_copy]',
            '    - [0x5DD518, asm, file_12_gap_5DD518_5DD638]',
            '    - [0x5DD638, c, file12_dialogue_call]',
            '    - [0x5DD65C, asm, file_12_after_5DD65C]',
            '    - [0x5E3C90, data, file_12]',
        ):
            self.assertIn(line,updated)
        self.assertEqual(updated.split('  - name: file_13\n',1)[1],
                         original.split('  - name: file_13\n',1)[1])
        with self.assertRaisesRegex(ValueError,'original ROM order'):
            stage_file12_splats(original,list(reversed(stages)))
        with self.assertRaisesRegex(ValueError,'Overlapping'):
            stage_file12_splats(original,[stages[0],stages[0]])

    def test_file12_stage_binds_source_hash_and_reference(self):
        source=b'void func_80222034_5DD504(void) {}\n'
        stage=file12_stage(source_sha256=hashlib.sha256(source).hexdigest())
        with tempfile.TemporaryDirectory() as folder:
            source_root=Path(folder);(source_root/'candidates').mkdir()
            path=source_root/'candidates/file12_dialogue_copy.c'
            path.write_bytes(source)
            with mock.patch.object(overlay_file12,'validate_reference_inputs') as validate:
                result=validate_file12_stage(stage,'pinned Splat',b'ROM',source_root)
            self.assertEqual(result,path)
            validate.assert_called_once_with('pinned Splat',b'ROM',
                                             ('func_80222034_5DD504',))
            stale=copy.deepcopy(stage);stale['source_sha256']='0'*64
            with self.assertRaisesRegex(ValueError,'source hash mismatch'):
                validate_file12_stage(stale,'pinned Splat',b'ROM',source_root)
            path.write_bytes(b'GLOBAL_ASM("hidden")\n')
            hidden=file12_stage(source_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
            with self.assertRaisesRegex(ValueError,'hide assembly ownership'):
                validate_file12_stage(hidden,'pinned Splat',b'ROM',source_root)

    def test_file12_tail_alias_patch_is_local_and_fail_closed(self):
        rom_offset,vma,alias_name,function_name,word=overlay_file12.TEXT_END_ALIAS
        comment=f'    /* {rom_offset:06X} {vma:08X} {word} */  nop\n'
        old=(f'nonmatching {function_name}, 0x4\n\n'
             f'glabel {function_name}\n{comment}endlabel {function_name}\n')
        new=f'  alabel {alias_name}\n{comment}'
        stage=file12_stage()
        with tempfile.TemporaryDirectory() as folder:
            checkout=Path(folder);asm=checkout/'asm/usa';asm.mkdir(parents=True)
            before=asm/'file_12_before_5DD504.s'
            after=asm/'file_12_after_5DD518.s'
            before.write_text(('lui %hi('+function_name+')\n')*4)
            after.write_text('start\n'+old+'tail\n')
            report=patch_file12_tail_alias_sources(checkout,stage)
            self.assertEqual(report['prefix_reference_rewrites'],4)
            self.assertTrue(report['instruction_bytes_changed'] is False)
            self.assertEqual(before.read_text().count(alias_name),4)
            self.assertNotIn(function_name,before.read_text())
            self.assertIn(new,after.read_text())
            self.assertNotIn(function_name,after.read_text())

            before.write_text(('lui %hi('+function_name+')\n')*4)
            original_before=before.read_bytes()
            after.write_text('start\n'+old.replace('nop','break')+'tail\n')
            with self.assertRaisesRegex(ValueError,'suffix tail-alias block'):
                patch_file12_tail_alias_sources(checkout,stage)
            self.assertEqual(before.read_bytes(),original_before)

    def test_file12_alignment_and_object_preparation_are_metadata_only(self):
        assembly=relocatable_function_object(text_alignment=16)
        lowered=lower_file12_text_alignment(assembly)
        differences=[offset for offset,(before,after) in enumerate(zip(assembly,lowered))
                     if before!=after]
        self.assertEqual(len(differences),1)
        with self.assertRaisesRegex(ValueError,'alignment or flags'):
            lower_file12_text_alignment(relocatable_function_object(text_alignment=4))

        source=b'void func_80222034_5DD504(void) {}\n'
        raw,text_offset=relocatable_file12_callback(bytes(range(20)))
        relocs=((0,5,'D_8015C5E8'),(4,6,'D_8015C5E8'),
                (8,5,'D_801C7750_1C8350'),(16,6,'D_801C7750_1C8350'))
        from decomp.elf_layout import pack_file12_callback_text
        packed,_=pack_file12_callback_text(raw,'func_80222034_5DD504',20,relocs)
        stage=file12_stage(source_sha256=hashlib.sha256(source).hexdigest(),
            compiler_object_sha256=hashlib.sha256(raw).hexdigest(),
            object_sha256=hashlib.sha256(packed).hexdigest())
        before,after,_=__import__('decomp.verify',fromlist=['_file12_stage_segments'])._file12_stage_segments(stage)
        with tempfile.TemporaryDirectory() as folder:
            checkout=Path(folder)
            c_path=checkout/'build/usa/src/file12_dialogue_copy.c.o';c_path.parent.mkdir(parents=True)
            c_path.write_bytes(raw)
            before_path=checkout/'build/usa/asm/usa'/f'{before}.s.o';before_path.parent.mkdir(parents=True)
            before_bytes=relocatable_function_object(text_alignment=16)
            before_path.write_bytes(before_bytes)
            after_path=checkout/'build/usa/asm/usa'/f'{after}.s.o'
            after_bytes=relocatable_function_object(text_alignment=16)
            after_path.write_bytes(after_bytes)
            (checkout/'.splat/usa').mkdir(parents=True)
            (checkout/'.splat/usa/mnsg.ld').write_text(
                '.file_12 0x8020d2a0 : AT(file_12_ROM_START) { *(.file_12*) }\n')
            report=prepare_file12_stage_objects(checkout,stage)
            self.assertEqual(c_path.read_bytes(),packed)
            self.assertEqual(before_path.read_bytes(),before_bytes)
            self.assertEqual(hashlib.sha256(after_path.read_bytes()).hexdigest(),
                             report['adjusted_objects'][0]['sha256_after'])
            self.assertEqual(report['callback_layout']['payload_bytes_changed'],0)
            self.assertEqual(report['preserved_prefix_text_alignment'],16)
            self.assertEqual(after_path.read_bytes(),lower_file12_text_alignment(after_bytes))
            changed=bytearray(raw);changed[text_offset+20]=1;c_path.write_bytes(bytes(changed))
            with self.assertRaisesRegex(ValueError,'compiler object hash mismatch'):
                prepare_file12_stage_objects(checkout,stage)

    def test_file12_apply_stages_only_named_callback_and_exact_slices(self):
        source=b'void func_80222034_5DD504(void) {}\n'
        stage=file12_stage(source_sha256=hashlib.sha256(source).hexdigest())
        original=(
            'sha1: '+overlay_file12.ROM_SHA1+'\n'
            '  - name: file_12\n    type: code\n    start: 0x5C8770\n'
            '    vram: 0x8020D2A0\n    bss_size: 0xE0\n    subalign: 16\n'
            '    overlay: yes\n    exclusive_ram_id: static_overlay_2\n'
            '    subsegments:\n    - [0x5C8770, asm]\n    - [0x5E3C90, data]\n'
            '  - name: file_13\n    start: 0x5F6840\n')
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);checkout=root/'candidate'
            (checkout/'config/usa').mkdir(parents=True);(checkout/'src').mkdir()
            (checkout/'Makefile').write_text('build rules\n')
            sources=root/'sources';(sources/'candidates').mkdir(parents=True)
            (sources/'candidates/file12_dialogue_copy.c').write_bytes(source)
            config=checkout/'config/usa/splat.yaml';config.write_text(original)
            manifest={'units':[],'overlay_file12_stage':stage}
            with mock.patch.object(overlay_file12,'validate_reference_inputs'):
                apply_units(checkout,manifest,sources,b'ROM')
            updated=config.read_text()
            self.assertIn('    - [0x5DD504, c, file12_dialogue_copy]',updated)
            self.assertEqual((checkout/'src/file12_dialogue_copy.c').read_bytes(),source)
            make=(checkout/'Makefile').read_text()
            self.assertIn('file_12_before_5DD504.s.o: ASFLAGS += --no-pad-sections',make)
            self.assertIn('file_12_after_5DD518.s.o: ASFLAGS += --no-pad-sections',make)
            self.assertNotIn('file_12',updated.split('  - name: file_13\n',1)[1])

    def test_file12_apply_copies_multiple_callbacks_and_preserves_gap_objects(self):
        first=b'void func_80222034_5DD504(void) {}\n'
        second=b'void func_80222168_5DD638(void) {}\n'
        stages=[
            file12_stage(source_sha256=hashlib.sha256(first).hexdigest()),
            file12_stage(
                name='func_80222168_5DD638',
                source='candidates/file12_dialogue_call.c',
                source_sha256=hashlib.sha256(second).hexdigest(),
            ),
        ]
        original=(
            'sha1: '+overlay_file12.ROM_SHA1+'\n'
            '  - name: file_12\n    type: code\n    start: 0x5C8770\n'
            '    vram: 0x8020D2A0\n    bss_size: 0xE0\n    subalign: 16\n'
            '    overlay: yes\n    exclusive_ram_id: static_overlay_2\n'
            '    subsegments:\n    - [0x5C8770, asm]\n    - [0x5E3C90, data]\n'
            '  - name: file_13\n    start: 0x5F6840\n')
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);checkout=root/'candidate'
            (checkout/'config/usa').mkdir(parents=True)
            (checkout/'src').mkdir()
            (checkout/'Makefile').write_text('build rules\n')
            sources=root/'sources';(sources/'candidates').mkdir(parents=True)
            (sources/'candidates/file12_dialogue_copy.c').write_bytes(first)
            (sources/'candidates/file12_dialogue_call.c').write_bytes(second)
            config=checkout/'config/usa/splat.yaml';config.write_text(original)
            manifest={'units':[],'overlay_file12_stages':stages}
            with mock.patch.object(overlay_file12,'validate_reference_inputs'):
                apply_units(checkout,manifest,sources,b'ROM')
            updated=config.read_text()
            self.assertIn('    - [0x5DD518, asm, file_12_gap_5DD518_5DD638]',updated)
            self.assertEqual((checkout/'src/file12_dialogue_copy.c').read_bytes(),first)
            self.assertEqual((checkout/'src/file12_dialogue_call.c').read_bytes(),second)
            make=(checkout/'Makefile').read_text()
            self.assertIn('file_12_gap_5DD518_5DD638.s.o: ASFLAGS += --no-pad-sections',make)

    def test_file12_ownership_requires_c_object_and_exact_map_placement(self):
        name='func_80222034_5DD504';size=20
        source=b'candidate callback source'
        raw,_=relocatable_file12_callback(bytes(range(size)))
        relocs=((0,5,'D_8015C5E8'),(4,6,'D_8015C5E8'),
                (8,5,'D_801C7750_1C8350'),(16,6,'D_801C7750_1C8350'))
        from decomp.elf_layout import pack_file12_callback_text
        packed,_=pack_file12_callback_text(raw,name,size,relocs)
        stage=file12_stage(source_sha256=hashlib.sha256(source).hexdigest(),
            compiler_object_sha256=hashlib.sha256(raw).hexdigest(),
            object_sha256=hashlib.sha256(packed).hexdigest())
        before,after,_=__import__('decomp.verify',fromlist=['_file12_stage_segments'])._file12_stage_segments(stage)
        c_name='build/usa/src/file12_dialogue_copy.c.o'
        prefix_size=overlay_file12.FUNCTIONS[name][0]-overlay_file12.VMA_START
        suffix_start=overlay_file12.FUNCTIONS[name][0]+size
        text_end_vma=overlay_file12.VMA_START+(
            overlay_file12.ROM_TEXT_END-overlay_file12.ROM_START)
        suffix_size=text_end_vma-suffix_start
        with tempfile.TemporaryDirectory() as folder:
            checkout=Path(folder);(checkout/'src').mkdir()
            (checkout/'src/file12_dialogue_copy.c').write_bytes(source)
            c_path=checkout/c_name;c_path.parent.mkdir(parents=True)
            c_path.write_bytes(packed)
            before_name=f'build/usa/asm/usa/{before}.s.o'
            after_name=f'build/usa/asm/usa/{after}.s.o'
            before_path=checkout/before_name;before_path.parent.mkdir(parents=True)
            before_path.write_bytes(relocatable_function_object(text_alignment=16))
            after_path=checkout/after_name
            after_path.write_bytes(lower_file12_text_alignment(
                relocatable_function_object(text_alignment=16)))
            mapping=(
                '.file_12 0x8020d2a0 0x2e0d0 load address 0x005c8770\n'
                f' {before_name}(.text)\n'
                f' .text 0x{overlay_file12.VMA_START:08x} 0x{prefix_size:x} {before_name}\n'
                f' {c_name}(.text)\n'
                f' .text 0x80222034 0x14 {c_name}\n'
                f' 0x80222034 {name}\n'
                f' {after_name}(.text)\n'
                f' .text 0x{suffix_start:08x} 0x{suffix_size:x} {after_name}\n'
                '.file_12_bss 0x8023b370 0x0 load address 0x005f6840\n')
            (checkout/'build/usa/mnsg.map').write_text(mapping)
            proof=verify_file12_ownership(checkout,stage)
            self.assertEqual(proof['function_vma'],'0x80222034')
            self.assertEqual(proof['file_12_size'],0x2e0d0)
            (checkout/'build/usa/mnsg.map').write_text(mapping.replace(
                f' {c_name}(.text)\n',''))
            with self.assertRaisesRegex(ValueError,'Linked object not placed exactly once'):
                verify_file12_ownership(checkout,stage)

    def test_file12_ownership_verifies_multiple_c_objects_and_original_gap(self):
        from decomp.elf_layout import pack_file12_callback_text
        first_name='func_80222034_5DD504'
        second_name='func_80222168_5DD638'
        first_source=b'first callback source'
        second_source=b'second callback source'
        first_raw,_=relocatable_file12_callback(bytes(range(20)))
        first_relocs=overlay_file12.FUNCTION_RELOCATIONS[first_name]
        first_packed,_=pack_file12_callback_text(
            first_raw,first_name,20,first_relocs,
            overlay_file12.FUNCTION_RELOCATION_SYMBOLS[first_name],
        )
        second_relocs=(
            (8,5,'D_801C7743'),(16,6,'D_801C7743'),
            (12,4,'func_801DCD48_598C58'),
        )
        second_raw,_=relocatable_file12_callback(
            bytes(range(36)),relocations=second_relocs,
            function_name=second_name,
            symbol_shapes=overlay_file12.FUNCTION_RELOCATION_SYMBOLS[second_name],
        )
        second_packed,_=pack_file12_callback_text(
            second_raw,second_name,36,
            overlay_file12.FUNCTION_RELOCATIONS[second_name],
            overlay_file12.FUNCTION_RELOCATION_SYMBOLS[second_name],
        )
        stages=[
            file12_stage(
                source_sha256=hashlib.sha256(first_source).hexdigest(),
                compiler_object_sha256=hashlib.sha256(first_raw).hexdigest(),
                object_sha256=hashlib.sha256(first_packed).hexdigest(),
            ),
            file12_stage(
                name=second_name,source='candidates/file12_dialogue_call.c',
                source_sha256=hashlib.sha256(second_source).hexdigest(),
                compiler_object_sha256=hashlib.sha256(second_raw).hexdigest(),
                object_sha256=hashlib.sha256(second_packed).hexdigest(),
            ),
        ]
        layout=_file12_stages_layout(stages)
        with tempfile.TemporaryDirectory() as folder:
            checkout=Path(folder)
            (checkout/'src').mkdir(parents=True)
            (checkout/'build/usa/src').mkdir(parents=True)
            (checkout/'build/usa/asm/usa').mkdir(parents=True)
            (checkout/'build/usa/src/file12_dialogue_copy.c').write_bytes(first_source)
            (checkout/'build/usa/src/file12_dialogue_call.c').write_bytes(second_source)
            (checkout/'src/file12_dialogue_copy.c').write_bytes(first_source)
            (checkout/'src/file12_dialogue_call.c').write_bytes(second_source)
            (checkout/'build/usa/src/file12_dialogue_copy.c.o').write_bytes(first_packed)
            (checkout/'build/usa/src/file12_dialogue_call.c.o').write_bytes(second_packed)
            for index,segment in enumerate(layout['assembly']):
                obj=relocatable_function_object(text_alignment=16)
                if index:
                    obj=lower_file12_text_alignment(obj)
                (checkout/f'build/usa/asm/usa/{segment}.s.o').write_bytes(obj)

            text_end=overlay_file12.VMA_START+(
                overlay_file12.ROM_TEXT_END-overlay_file12.ROM_START)
            map_lines=[
                '.file_12 0x8020d2a0 0x2e0d0 load address 0x005c8770',
            ]
            cursor=overlay_file12.VMA_START
            assembly_index=0
            for stage in stages:
                function=stage['function']
                if function['vma']>cursor:
                    segment=layout['assembly'][assembly_index]
                    obj=f'build/usa/asm/usa/{segment}.s.o'
                    map_lines.extend((
                        f' {obj}(.text)',
                        f' .text 0x{cursor:08x} 0x{function["vma"]-cursor:x} {obj}',
                    ))
                    assembly_index+=1
                source_name=Path(stage['source']).name
                c_object=f'build/usa/src/{source_name}.o'
                map_lines.extend((
                    f' {c_object}(.text)',
                    f' .text 0x{function["vma"]:08x} 0x{function["size"]:x} {c_object}',
                    f' 0x{function["vma"]:08x} {function["name"]}',
                ))
                cursor=function['vma']+function['size']
            suffix=layout['assembly'][assembly_index]
            suffix_object=f'build/usa/asm/usa/{suffix}.s.o'
            map_lines.extend((
                f' {suffix_object}(.text)',
                f' .text 0x{cursor:08x} 0x{text_end-cursor:x} {suffix_object}',
                '.file_12_bss 0x8023b370 0x0 load address 0x005f6840',
            ))
            map_path=checkout/'build/usa/mnsg.map'
            map_path.write_text('\n'.join(map_lines)+'\n')
            proof=verify_file12_ownership(checkout,stages)
            self.assertEqual([item['function'] for item in proof['callbacks']],
                             [first_name,second_name])
            self.assertIn('file_12_gap_5DD518_5DD638.s.o',
                          '\n'.join(proof['assembly_objects']))
            wrong=map_path.read_text().replace(
                '.text 0x80222048 0x120', '.text 0x8022204c 0x11c')
            map_path.write_text(wrong)
            with self.assertRaisesRegex(ValueError,'Changed original object guest VMA/extent'):
                verify_file12_ownership(checkout,stages)

    def test_file12_claim_append_requires_exact_link_proof_and_full_rom(self):
        stage=file12_stage();name=stage['function']['name']
        expected=overlay_file12.FUNCTIONS[name][3]
        comparison={'full_rom_match':False,'claimed_functions':0,'matched_functions':0,
                    'matched_function_bytes':0,'functions':[]}
        linked={'functions':[{'name':name,'section':'.file_12','vma':'0x80222034',
            'rom_offset':'0x5DD504','bytes':20,'candidate_code_matches_original':True,
            'candidate_relocations_match_reference':True,'original_sha256':expected,
            'candidate_sha256':expected,'relocation_count':4}]}
        append_file12_function_comparison(comparison,stage,linked)
        self.assertEqual(comparison['functions'][0]['guest_address'],'0x80222034')
        self.assertEqual(comparison['matched_function_bytes'],20)
        with self.assertRaisesRegex(ValueError,'complete-ROM comparison'):
            require_file12_full_rom_match(comparison)
        comparison['full_rom_match']=True
        require_file12_full_rom_match(comparison)
        linked['functions'][0]['candidate_relocations_match_reference']=False
        with self.assertRaisesRegex(ValueError,'failed linked provenance'):
            append_file12_function_comparison(comparison,stage,linked)

    def test_file43_splat_split_is_local_and_preserves_rodata_boundary(self):
        original=(
            'sha1: ' + overlay_file43.ROM_SHA1 + '\nsegments:\n'
            '  - name: file_43\n'
            '    type: code\n    start: 0x6F34E0\n    vram: 0x8000000\n'
            '    subalign: 16\n    overlay: yes\n'
            '    exclusive_ram_id: tlb_overlay\n    subsegments:\n'
            '    - [0x6F34E0, asm, file_43]\n'
            '    - [0x6F9CE0, rodata, file_43]\n'
            '  - name: file_44\n    start: 0x6FB200\n')
        updated,before,after=stage_file43_splat(original,file43_stage())
        self.assertEqual((before,after),('file_43_before_6F369C','file_43_after_6F36FC'))
        self.assertIn('    subalign: null\n',updated)
        self.assertIn('    - [0x6F34E0, asm, file_43_before_6F369C]\n'
                      '    - [0x6F369C, c, key_spawn_gate]\n'
                      '    - [0x6F36FC, asm, file_43_after_6F36FC]\n'
                      '    - [0x6F9CE0, rodata, file_43]\n',updated)
        self.assertEqual(updated.split('  - name: file_44\n',1)[1],
                         original.split('  - name: file_44\n',1)[1])
        with self.assertRaisesRegex(ValueError,'Pinned file_43 Splat split anchor'):
            stage_file43_splat(original.replace('0x6F9CE0','0x6F9CE4'),file43_stage())

    def test_file43_alignment_patch_changes_only_one_section_header_word(self):
        original=relocatable_function_object(
            [('func_080001BC_6F369C',bytes(96))],text_alignment=16)
        staged=lower_file43_text_alignment(original)
        differences=[offset for offset,(before,after) in enumerate(zip(original,staged))
                     if before!=after]
        self.assertEqual(len(differences),1)
        self.assertEqual(staged[differences[0]-3:differences[0]+1],b'\0\0\0\x04')
        self.assertEqual(original[differences[0]-3:differences[0]+1],b'\0\0\0\x10')
        with self.assertRaisesRegex(ValueError,'alignment or flags'):
            lower_file43_text_alignment(relocatable_function_object(
                [('func_080001BC_6F369C',bytes(96))],text_alignment=4))
        with self.assertRaisesRegex(ValueError,'Invalid file_43 .text alignment'):
            lower_file43_text_alignment(original,new_alignment=3)

    def test_file43_object_preparation_pins_hashes_and_preserves_prefix(self):
        name='func_080001BC_6F369C';size=96
        original_c=relocatable_function_object([(name,bytes(size))],text_alignment=16)
        staged_c=lower_file43_text_alignment(original_c)
        with tempfile.TemporaryDirectory() as folder:
            checkout=Path(folder)
            c_path=checkout/'build/usa/src/key_spawn_gate.c.o';c_path.parent.mkdir(parents=True)
            before,after,_=__import__('decomp.verify',fromlist=['_file43_stage_segments'])._file43_stage_segments(
                file43_stage())
            before_path=checkout/'build/usa/asm/usa'/f'{before}.s.o';before_path.parent.mkdir(parents=True)
            before_bytes=relocatable_function_object(text_alignment=16)
            before_path.write_bytes(before_bytes)
            after_path=checkout/'build/usa/asm/usa'/f'{after}.s.o'
            after_bytes=relocatable_function_object(text_alignment=16)
            after_path.write_bytes(after_bytes)
            (checkout/'.splat/usa').mkdir(parents=True)
            (checkout/'.splat/usa/mnsg.ld').write_text(
                '.file_43 0x8000000 : AT(file_43_ROM_START) { *(.file_43*) }\n')
            stage=file43_stage(
                compiler_object_sha256=hashlib.sha256(original_c).hexdigest(),
                object_sha256=hashlib.sha256(staged_c).hexdigest())
            c_path.write_bytes(original_c)
            report=prepare_file43_stage_objects(checkout,stage)
            self.assertEqual(c_path.read_bytes(),staged_c)
            self.assertEqual(before_path.read_bytes(),before_bytes)
            self.assertEqual(hashlib.sha256(after_path.read_bytes()).hexdigest(),
                             report['adjusted_objects'][1]['sha256_after'])
            self.assertEqual(report['preserved_prefix_text_alignment'],16)
            self.assertEqual(report['adjusted_text_alignment'],{'from':16,'to':4})

            c_path.write_bytes(original_c);after_path.write_bytes(after_bytes)
            bad=copy.deepcopy(stage);bad['object_sha256']='0'*64
            with self.assertRaisesRegex(ValueError,'staged C object hash mismatch'):
                prepare_file43_stage_objects(checkout,bad)
            self.assertEqual(c_path.read_bytes(),original_c)
            self.assertEqual(after_path.read_bytes(),after_bytes)

    def test_file43_stage_binds_source_and_original_reference_contract(self):
        source=b'void func_080001BC_6F369C(void) { }\n'
        stage=file43_stage(source_sha256=hashlib.sha256(source).hexdigest())
        with tempfile.TemporaryDirectory() as folder:
            source_root=Path(folder);(source_root/'candidates').mkdir()
            (source_root/'candidates/key_spawn_gate.c').write_bytes(source)
            with mock.patch.object(overlay_file43,'validate_reference_inputs') as validate:
                path=validate_file43_stage(stage,'pinned Splat',b'ROM',source_root)
            self.assertEqual(path,source_root/'candidates/key_spawn_gate.c')
            validate.assert_called_once_with('pinned Splat',b'ROM',('func_080001BC_6F369C',))
            stale=copy.deepcopy(stage);stale['source_sha256']='0'*64
            with self.assertRaisesRegex(ValueError,'source hash mismatch'):
                validate_file43_stage(stale,'pinned Splat',b'ROM',source_root)
            (source_root/'candidates/key_spawn_gate.c').write_bytes(b'GLOBAL_ASM("x")\n')
            source_hash=hashlib.sha256(b'GLOBAL_ASM("x")\n').hexdigest()
            hidden_asm=file43_stage(source_sha256=source_hash)
            with self.assertRaisesRegex(ValueError,'hide assembly ownership'):
                validate_file43_stage(hidden_asm,'pinned Splat',b'ROM',source_root)

    def test_file43_apply_stages_source_and_no_padding_slices_atomically(self):
        source=b'void func_080001BC_6F369C(void) { }\n'
        stage=file43_stage(source_sha256=hashlib.sha256(source).hexdigest())
        original=(
            'sha1: ' + overlay_file43.ROM_SHA1 + '\n'
            '  - name: file_43\n    type: code\n    start: 0x6F34E0\n'
            '    vram: 0x8000000\n    subalign: 16\n    overlay: yes\n'
            '    exclusive_ram_id: tlb_overlay\n    subsegments:\n'
            '    - [0x6F34E0, asm, file_43]\n'
            '    - [0x6F9CE0, rodata, file_43]\n'
            '  - name: file_44\n    start: 0x6FB200\n')
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);checkout=root/'candidate';(checkout/'config/usa').mkdir(parents=True)
            (checkout/'src').mkdir();(checkout/'Makefile').write_text('build rules\n')
            sources=root/'sources';(sources/'candidates').mkdir(parents=True)
            (sources/'candidates/key_spawn_gate.c').write_bytes(source)
            config=checkout/'config/usa/splat.yaml';config.write_text(original)
            manifest={'units':[],'overlay_file43_stage':stage}
            with mock.patch.object(overlay_file43,'validate_reference_inputs'):
                apply_units(checkout,manifest,sources,b'ROM')
            self.assertEqual((checkout/'src/key_spawn_gate.c').read_bytes(),source)
            updated=config.read_text()
            self.assertIn('    - [0x6F369C, c, key_spawn_gate]',updated)
            make=(checkout/'Makefile').read_text()
            self.assertIn('file_43_before_6F369C.s.o: ASFLAGS += --no-pad-sections',make)
            self.assertIn('file_43_after_6F36FC.s.o: ASFLAGS += --no-pad-sections',make)
            self.assertNotIn('file_44',updated.split('  - name: file_44\n',1)[1])

            (checkout/'src/key_spawn_gate.c').unlink()
            config.write_text(original);make_before=(checkout/'Makefile').read_bytes()
            bad=copy.deepcopy(manifest);bad['overlay_file43_stage']['source_sha256']='0'*64
            with mock.patch.object(overlay_file43,'validate_reference_inputs'):
                with self.assertRaisesRegex(ValueError,'source hash mismatch'):
                    apply_units(checkout,bad,sources,b'ROM')
            self.assertEqual(config.read_text(),original)
            self.assertEqual((checkout/'Makefile').read_bytes(),make_before)
            self.assertFalse((checkout/'src/key_spawn_gate.c').exists())

    def test_file43_ownership_requires_used_c_object_and_assembly_relinquishment(self):
        stage=file43_stage(source_sha256=hashlib.sha256(b'candidate C').hexdigest())
        name=stage['function']['name'];size=stage['function']['size']
        before,after,_=__import__('decomp.verify',fromlist=['_file43_stage_segments'])._file43_stage_segments(stage)
        c_object_name='build/usa/src/key_spawn_gate.c.o'
        with tempfile.TemporaryDirectory() as folder:
            checkout=Path(folder);source=checkout/'src/key_spawn_gate.c';source.parent.mkdir(parents=True)
            source.write_bytes(b'candidate C')
            c_object=checkout/c_object_name;c_object.parent.mkdir(parents=True)
            c_object.write_bytes(relocatable_function_object([(name,bytes(size))],text_alignment=4))
            stage['object_sha256']=hashlib.sha256(c_object.read_bytes()).hexdigest()
            for segment in (before,after):
                path=checkout/'build/usa/asm/usa'/f'{segment}.s.o';path.parent.mkdir(parents=True,exist_ok=True)
                path.write_bytes(relocatable_function_object(
                    text_alignment=16 if segment==before else 4))
            mapping=(
                '.file_43 0x08000000 0x7d20 load address 0x006f34e0\n'
                f' build/usa/asm/usa/{before}.s.o(.text)\n'
                f' {c_object_name}(.text)\n'
                f' 0x080001bc {name}\n'
                f' build/usa/asm/usa/{after}.s.o(.text)\n'
                '.file_43_bss 0x08007d20 0x0 load address 0x006fb200\n')
            (checkout/'build/usa/mnsg.map').write_text(mapping)
            proof=verify_file43_ownership(checkout,stage)
            self.assertEqual(proof['function_vma'],'0x080001BC')
            self.assertEqual(proof['object_sha256'],stage['object_sha256'])

            (checkout/'build/usa/mnsg.map').write_text(mapping.replace(f' {c_object_name}(.text)\n',''))
            with self.assertRaisesRegex(ValueError,'does not place the expected'):
                verify_file43_ownership(checkout,stage)
            (checkout/'build/usa/mnsg.map').write_text(mapping)
            asm_path=checkout/'build/usa/asm/usa'/f'{before}.s.o'
            asm_path.write_bytes(relocatable_function_object(
                [(name,bytes(size))],text_alignment=16))
            with self.assertRaisesRegex(ValueError,'assembly still owns'):
                verify_file43_ownership(checkout,stage)
            asm_path.write_bytes(relocatable_function_object())
            wrong_hash=copy.deepcopy(stage);wrong_hash['object_sha256']='0'*64
            with self.assertRaisesRegex(ValueError,'object hash mismatch'):
                verify_file43_ownership(checkout,wrong_hash)

    def test_file43_overlay_claim_uses_explicit_mapping_and_cannot_hide_rom_mismatch(self):
        stage=file43_stage()
        expected=bytes(32)
        manifest={'decompressed_sha1':hashlib.sha1(expected).hexdigest(),
                  'units':[],'overlay_file43_stage':stage}
        self.assertEqual(main_claimed_functions(manifest),[])
        self.assertEqual(claimed_functions(manifest),[stage['function']])
        comparison={'full_rom_match':False,'claimed_functions':0,'matched_functions':0,
                    'matched_function_bytes':0,'functions':[]}
        linked={'functions':[{'name':stage['function']['name'],
            'section':'.file_43','vma':'0x080001BC','rom_offset':'0x6F369C','bytes':96,
            'candidate_code_matches_original':True,
            'candidate_relocations_match_reference':True,
            'original_sha256':overlay_file43.FUNCTIONS[stage['function']['name']][3],
            'candidate_sha256':overlay_file43.FUNCTIONS[stage['function']['name']][3],
            'relocation_count':8}]}
        append_file43_function_comparison(comparison,stage,linked)
        self.assertEqual(comparison['functions'][0]['rom_offset'],'0x6F369C')
        self.assertEqual(comparison['functions'][0]['guest_address'],'0x080001BC')
        self.assertEqual(comparison['matched_function_bytes'],96)
        self.assertFalse(comparison['full_rom_match'])
        linked['functions'][0]['candidate_relocations_match_reference']=False
        with self.assertRaisesRegex(ValueError,'failed linked provenance'):
            append_file43_function_comparison(comparison,stage,linked)

    def test_file43_stage_proof_cannot_bypass_full_rom_gate(self):
        comparison={'full_rom_match':False,'claimed_functions':1,'matched_functions':1}
        with self.assertRaisesRegex(ValueError,'complete-ROM comparison'):
            require_file43_full_rom_match(comparison)
        comparison['full_rom_match']=True
        require_file43_full_rom_match(comparison)

    def test_file43_link_proof_uses_original_splat_and_explicit_reference(self):
        stage=file43_stage()
        original=(
            'sha1: ' + overlay_file43.ROM_SHA1 + '\n'
            '  - name: file_43\n    type: code\n    start: 0x6F34E0\n'
            '    vram: 0x8000000\n    subalign: 16\n    overlay: yes\n'
            '    exclusive_ram_id: tlb_overlay\n    subsegments:\n'
            '    - [0x6F34E0, asm, file_43]\n'
            '    - [0x6F9CE0, rodata, file_43]\n'
            '  - name: file_44\n    start: 0x6FB200\n')
        expected_splat,_,_=stage_file43_splat(original,stage)
        linked={'linked_elf_provenance':{'functions':[{'name':stage['function']['name']}]}}
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);baseline=root/'baseline';candidate=root/'candidate'
            for checkout in (baseline,candidate):
                (checkout/'config/usa').mkdir(parents=True)
                (checkout/'build/usa').mkdir(parents=True)
                (checkout/'build/usa/mnsg.elf').write_bytes(relocatable_function_object())
            (baseline/'config/usa/splat.yaml').write_text(original)
            (candidate/'config/usa/splat.yaml').write_text(expected_splat)
            with mock.patch('decomp.verify.verify_file43_ownership',return_value={'owner':'C'}), \
                 mock.patch.object(overlay_file43,'validate_linked_elf_provenance',return_value=linked) as validate:
                result=verify_file43_stage_build(baseline,candidate,stage,b'reference ROM')
            self.assertEqual(result['ownership'],{'owner':'C'})
            self.assertEqual(result['linked_elf_provenance'],linked['linked_elf_provenance'])
            validate.assert_called_once_with(original,b'reference ROM',
                (baseline/'build/usa/mnsg.elf').read_bytes(),
                (candidate/'build/usa/mnsg.elf').read_bytes(),(stage['function']['name'],))

    def test_manifest_bounds_and_symbol_identity(self):
        manifest=load_manifest(ROOT/'decomp/manifest.json')
        unit_functions=sum(len(u['functions']) for u in manifest['units'])
        claims=claimed_functions(manifest)
        # Source patches and staged overlays live outside main translation units.
        # Check structural agreement so promotions do not require pinning counts here.
        self.assertEqual(len(claims),unit_functions+
                         len(manifest.get('existing_source_patches',[]))+
                         (manifest.get('overlay_file43_stage') is not None)+
                         sum(374 if st['format']=='goemon-file12-registration-374-v1' else 1 for st in manifest_file12_stages(manifest))+(file11_stage_mode(manifest) or 0)+
                         len(manifest_file13_stages(manifest)) + cross_claim_count(manifest) + native_claim_count(manifest))
        proof=json.loads((ROOT/'decomp/results/combined.json').read_text())
        inventory=json.loads((ROOT/'decomp/results/inventory.json').read_text())
        self.assertEqual(proof['comparison']['claimed_functions'],len(claims))
        self.assertEqual(proof['comparison']['matched_functions'],len(claims))
        self.assertEqual(inventory['summary']['newly_matching_c'],len(claims))
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'bad.json'
            bad=copy.deepcopy(manifest);bad['units'][0]['source']='../other.c'
            path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError,'source'):load_manifest(path)
            bad=copy.deepcopy(manifest);bad['units'][0]['functions'][0]['rom_offset']+=4
            path.write_text(json.dumps(bad))
            with self.assertRaises(ValueError):load_manifest(path)

    def test_heap_noop_layout_manifest_is_fail_closed(self):
        manifest=load_manifest(ROOT/'decomp/manifest.json')
        self.assertTrue(manifest['heap_noop_text_layout'])
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'manifest.json'
            bad=copy.deepcopy(manifest)
            bad['heap_noop_text_layout']=False
            path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError,'layout preset'):
                load_manifest(path)
            bad=copy.deepcopy(manifest)
            unit=next(u for u in bad['units'] if u['source']=='heap_noop.c')
            unit['asm_no_padding']=[]
            path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError,'split mismatch'):
                load_manifest(path)
            bad=copy.deepcopy(manifest)
            unit=next(u for u in bad['units'] if u['source']=='heap_noop.c')
            unit['splat_replacement']=unit['splat_replacement'].replace('0x3698C','0x36990')
            path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError,'split mismatch'):
                load_manifest(path)

    def test_collision_source_patch_manifest_is_fail_closed(self):
        manifest=load_manifest(ROOT/'decomp/manifest.json')
        self.assertEqual(manifest['existing_source_patches'],[COLLISION_GATE_PATCH])
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'manifest.json'
            bad=copy.deepcopy(manifest)
            bad['existing_source_patches'][0]['function']['rom_offset']+=4
            path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError,'source patch'):load_manifest(path)
            bad=copy.deepcopy(manifest)
            bad['existing_source_patches'][0]['patched_sha256_lf']='0'*64
            path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError,'source patch'):load_manifest(path)
            bad=copy.deepcopy(manifest)
            bad['units'][0]['functions'].append(dict(COLLISION_GATE_PATCH['function']))
            path.write_text(json.dumps(bad))
            with self.assertRaises(ValueError):load_manifest(path)

    def test_collision_source_patch_preflight_is_non_destructive(self):
        from decomp.collision_patch import prepare_collision_gate
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);checkout=root/'candidate';(checkout/'config/usa').mkdir(parents=True)
            (checkout/'src').mkdir();source=root/'sources';source.mkdir()
            (checkout/'config/usa/splat.yaml').write_text('[0x10, asm]\n')
            (source/'unit.c').write_text('int tested(void) { return 1; }\n')
            (checkout/'src/27FE0.c').write_text('#pragma GLOBAL_ASM("asm/nonmatchings/27FE0/func_80029E08_2AA08.s")\n'
                                                    's32 func_80029E58_2AA58(f32 x) { return 0; }\n'
                                                    's32 func_8002A168_2AD68(f32 x,f32 y,f32 z) { return 1; }\n')
            (source/'candidates').mkdir()
            (source/'candidates/collision_gate.c').write_bytes((ROOT/'decomp/candidates/collision_gate.c').read_bytes())
            current=(checkout/'src/27FE0.c').read_bytes()
            patch=dict(COLLISION_GATE_PATCH)
            patch['patched_sha256_lf']='0'*64
            manifest={'units':[dict(source='unit.c',splat_original='[0x10, asm]',splat_replacement='[0x10, c, unit]')],
                      'existing_source_patches':[patch]}
            with self.assertRaisesRegex(ValueError,'patch hash mismatch'):
                apply_units(checkout,manifest,source)
            self.assertEqual((checkout/'src/27FE0.c').read_bytes(),current)
            self.assertFalse((checkout/'src/unit.c').exists())
            self.assertEqual((checkout/'config/usa/splat.yaml').read_text(),'[0x10, asm]\n')

    def test_symbol_parsing_and_tampered_matching_evidence(self):
        data=b'\x11'*16
        manifest={'decompressed_sha1':hashlib.sha1(data).hexdigest(),
                  'units':[{'rom_end':16,'functions':[{'name':'func_80000000_0','rom_offset':0,'size':8}]}]}
        # Synthetic symbols preserve the same guest/ROM relation used by verifier.
        manifest['units'][0]['functions'][0]['name']='func_7FFFF400_0'
        symbols=parse_symbols('7ffff400 T func_7FFFF400_0\n         U external\n')
        result=compare_images(data,data,manifest,symbols)
        self.assertTrue(result['full_rom_match']);self.assertEqual(result['matched_functions'],1)
        changed=data[:9]+b'\x22'+data[10:]
        result=compare_images(data,changed,manifest,symbols)
        self.assertFalse(result['full_rom_match']);self.assertEqual(result['matched_functions'],1)
        result=compare_images(data,b'\x22'+data[1:],manifest,symbols)
        self.assertEqual(result['matched_functions'],0)
        symbols['func_7FFFF400_0.NON_MATCHING']=0x7FFFF400
        self.assertEqual(compare_images(data,data,manifest,symbols)['matched_functions'],0)
        del symbols['func_7FFFF400_0.NON_MATCHING'];symbols['func_7FFFF400_0']+=4
        self.assertEqual(compare_images(data,data,manifest,symbols)['matched_functions'],0)
        with self.assertRaisesRegex(ValueError,'identity'):compare_images(b'other',data,manifest,symbols)

    def test_apply_only_expected_anchor_preserves_existing_files_on_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            checkout=Path(folder)/'candidate';(checkout/'config/usa').mkdir(parents=True)
            (checkout/'src').mkdir();sources=Path(folder)/'sources';sources.mkdir()
            config=checkout/'config/usa/splat.yaml';config.write_text('before [0x10, asm] after\n')
            (sources/'unit.c').write_text('void function(void) {}\n')
            manifest={'units':[{'source':'unit.c','splat_original':'[0x10, asm]',
                                'splat_replacement':'[0x10, c, unit]'}]}
            apply_units(checkout,manifest,sources)
            self.assertIn('before [0x10, c, unit] after',config.read_text())
            (checkout/'src/unit.c').write_text('user work')
            config.write_text('before [0x10, asm] after\n');before=config.read_bytes()
            with self.assertRaises(ValueError):apply_units(checkout,manifest,sources)
            self.assertEqual((checkout/'src/unit.c').read_text(),'user work')
            self.assertEqual(config.read_bytes(),before)

    def test_shared_flag_functions_have_no_assembly_placeholders(self):
        for unit in load_manifest(ROOT/'decomp/manifest.json')['units']:
            source=(ROOT/'decomp'/unit['source']).read_text()
            self.assertEqual(source.count('GLOBAL_ASM'),len(unit.get('assembly_functions',[])))
            for fn in unit['functions']:
                self.assertNotIn('/'+fn['name']+'.s',source)
            self.assertNotIn('__asm__',source)

    def test_assembly_retention_cannot_claim_a_reconstructed_function(self):
        manifest=load_manifest(ROOT/'decomp/manifest.json')
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'manifest.json'
            manifest['units'][0]['assembly_functions']=[manifest['units'][0]['functions'][0]['name']]
            path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError,'assembly placeholder'):load_manifest(path)

    def test_manifest_ownership_rejects_duplicate_claims_and_overlapping_units(self):
        manifest=load_manifest(ROOT/'decomp/manifest.json')
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'manifest.json'
            duplicate=copy.deepcopy(manifest)
            duplicate['units'][0]['functions'].append(
                copy.deepcopy(duplicate['units'][0]['functions'][0]))
            path.write_text(json.dumps(duplicate))
            with self.assertRaisesRegex(ValueError,'duplicate function name'):
                load_manifest(path)

            overlapping=copy.deepcopy(manifest)
            original=overlapping['units'][0]
            overlapping['units'].append({
                'source':'other.c',
                'rom_start':original['rom_start']+4,
                'rom_end':original['rom_end']+4,
                'splat_original':'[0x10, asm]',
                'splat_replacement':'[0x10, c, other]',
                'functions':[],
                'assembly_functions':[],
            })
            path.write_text(json.dumps(overlapping))
            with self.assertRaisesRegex(ValueError,'Overlapping units'):
                load_manifest(path)

    def test_missing_retained_assembly_marker_is_rejected_before_staging(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            checkout=root/'candidate'
            (checkout/'config/usa').mkdir(parents=True)
            (checkout/'src').mkdir()
            sources=root/'sources'
            sources.mkdir()
            config=checkout/'config/usa/splat.yaml'
            config.write_text('[0x10, asm]\n')
            name='func_80000010_10'
            (sources/'unit.c').write_text('void function(void) {}\n')
            manifest={'units':[{
                'source':'unit.c',
                'splat_original':'[0x10, asm]',
                'splat_replacement':'[0x10, c, unit]',
                'assembly_functions':[name],
            }]}
            with self.assertRaisesRegex(ValueError,'Undeclared assembly placeholder'):
                apply_units(checkout,manifest,sources)
            self.assertFalse((checkout/'src/unit.c').exists())
            self.assertEqual(config.read_text(),'[0x10, asm]\n')

    def test_undeclared_placeholder_rejected_without_partial_application(self):
        with tempfile.TemporaryDirectory() as folder:
            checkout=Path(folder)/'candidate';(checkout/'config/usa').mkdir(parents=True)
            (checkout/'src').mkdir();sources=Path(folder)/'sources';sources.mkdir()
            config=checkout/'config/usa/splat.yaml';config.write_text('[0x10, asm]\n')
            (sources/'unit.c').write_text('#pragma GLOBAL_ASM("asm/func_80000000_0.s")\n')
            manifest={'units':[{'source':'unit.c','splat_original':'[0x10, asm]',
                                'splat_replacement':'[0x10, c, unit]'}]}
            with self.assertRaisesRegex(ValueError,'Undeclared'):apply_units(checkout,manifest,sources)
            self.assertFalse((checkout/'src/unit.c').exists())
            self.assertEqual(config.read_text(),'[0x10, asm]\n')

    def test_jump_label_override_is_narrow_and_candidate_only(self):
        manifest=load_manifest(ROOT/'decomp/manifest.json')
        self.assertEqual(manifest['splat_options'],{'asm_jtbl_label_macro':'glabel'})
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'manifest.json'
            bad=copy.deepcopy(manifest);bad['splat_options']={'arbitrary':'setting'}
            path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError,'Splat'):load_manifest(path)
            checkout=Path(folder)/'candidate';(checkout/'config/usa').mkdir(parents=True)
            (checkout/'src').mkdir();sources=Path(folder)/'sources';sources.mkdir()
            config=checkout/'config/usa/splat.yaml';config.write_text('options:\n  compiler: IDO\n[0x10, asm]\n')
            (sources/'unit.c').write_text('void function(void) {}\n')
            small={'splat_options':{'asm_jtbl_label_macro':'glabel'},'units':[{
                'source':'unit.c','splat_original':'[0x10, asm]','splat_replacement':'[0x10, c, unit]'}]}
            apply_units(checkout,small,sources)
            self.assertIn('options:\n  asm_jtbl_label_macro: glabel\n  compiler: IDO',config.read_text())

    def test_promoted_comparator_has_single_manifest_owner(self):
        manifest=load_manifest(ROOT/'decomp/manifest.json')
        vm=next(unit for unit in manifest['units'] if unit['source']=='script_vm.c')
        name='func_8003D9B8_3E5B8'
        self.assertEqual(sum(fn['name']==name for fn in vm['functions']),1)
        self.assertNotIn(name,vm['assembly_functions'])
        self.assertIn('func_8003DE80_3EA80',vm['assembly_functions'])
        self.assertIn('#include "vm_compare_reference.h"', (ROOT/'decomp/script_vm.c').read_text())

    def test_vm_layout_preset_rejects_other_values_and_missing_handler(self):
        manifest=load_manifest(ROOT/'decomp/manifest.json')
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'manifest.json'
            for value in (False,1,'yes',{}):
                bad=copy.deepcopy(manifest);bad['vm_assignment_table_layout']=value
                path.write_text(json.dumps(bad))
                with self.assertRaisesRegex(ValueError,'layout preset'):load_manifest(path)
            bad=copy.deepcopy(manifest)
            vm=next(u for u in bad['units'] if u['source']=='script_vm.c')
            vm['functions']=[f for f in vm['functions'] if f['name']!='func_8003DB0C_3E70C']
            path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError,'pinned assignment|Canonical 210-function claim inventory changed'):load_manifest(path)

    def test_vm_layout_changes_only_selected_main_header_and_table(self):
        with tempfile.TemporaryDirectory() as folder:
            checkout=Path(folder)/'candidate';(checkout/'config/usa').mkdir(parents=True)
            (checkout/'src').mkdir();sources=Path(folder)/'sources';sources.mkdir()
            config=checkout/'config/usa/splat.yaml'
            original=('    start: 0x1050\n    vram: 0x80000450\n    subalign: 16\n    subsegments:\n'
                '    - [0x10, asm]\n    - [0x7B6F0, rodata, main_continued]\n'
                '  - name: other\n    subalign: 16\n')
            config.write_text(original);(checkout/'Makefile').write_text('all:\n\ttrue\n')
            (sources/'unit.c').write_text('void function(void) {}\n')
            manifest={'vm_assignment_table_layout':True,'units':[{'source':'unit.c',
                'splat_original':'[0x10, asm]','splat_replacement':'[0x10, c, unit]'}]}
            apply_units(checkout,manifest,sources)
            updated=config.read_text()
            self.assertIn('    - [0x7DC2C, .rodata, script_vm]\n    - [0x7DC68, rodata, main_continued_after_vm_store]',updated)
            self.assertIn('  - name: other\n    subalign: 16',updated)
            self.assertEqual(updated.count('    subalign: 4'),1)
            self.assertIn('main_continued.rodata.s.o: ASFLAGS += --no-pad-sections',(checkout/'Makefile').read_text())
            # An ambiguous anchor must fail without copying a C file or modifying either build file.
            (checkout/'src/unit.c').unlink()
            config.write_text(original.replace('    subalign: 16\n    subsegments:', '    subalign: 8\n    subsegments:'))
            before=config.read_bytes();make_before=(checkout/'Makefile').read_bytes()
            with self.assertRaisesRegex(ValueError,'subalignment'):apply_units(checkout,manifest,sources)
            self.assertEqual(config.read_bytes(),before)
            self.assertEqual((checkout/'Makefile').read_bytes(),make_before)
            self.assertFalse((checkout/'src/unit.c').exists())
    def test_current_sources_and_manifest_have_matching_build_evidence(self):
        manifest=load_manifest(ROOT/'decomp/manifest.json')
        result=json.loads((ROOT/'decomp/results/combined.json').read_text())
        self.assertEqual(result['status'],'matched')
        self.assertEqual(result['upstream_commit'],manifest['upstream_commit'])
        self.assertTrue(result['comparison']['full_rom_match'])
        verifier=(ROOT/'decomp/verify.py').read_bytes().replace(b'\r\n',b'\n')
        self.assertEqual(result['verifier_source_sha256_lf'],
                         hashlib.sha256(verifier).hexdigest())
        self.assertEqual(hashlib.sha256(verifier).hexdigest(),
                         json.loads((ROOT/'decomp/results/vm_residual_inventory.json').read_text())['current_sources']['verifier_sha256'])
        expected={f['name']:f for f in claimed_functions(manifest)}
        actual={f['name']:f for f in result['comparison']['functions']}
        self.assertEqual(set(expected),set(actual))
        self.assertEqual(result['comparison']['matched_function_bytes'],sum(f['size'] for f in expected.values()))
        for name,fn in actual.items():
            self.assertTrue(fn['matched'],name)
            self.assertEqual(fn['size'],expected[name]['size'])
            self.assertEqual(int(fn['rom_offset'],16),expected[name]['rom_offset'])
            self.assertEqual(fn['candidate_sha256'],fn['expected_sha256'])
        sources={u['source'] for u in manifest['units']}|set(manifest['support_headers'])|{p['source'] for p in manifest.get('existing_source_patches', [])}
        if manifest.get('overlay_file43_stage') is not None:
            sources.add(manifest['overlay_file43_stage']['source'])
        sources.update(stage['source'] for stage in manifest_file12_stages(manifest))
        if manifest.get('overlay_file11_stage') is not None:
            from decomp import overlay_file11, file11_143_stage, file11_144_stage, file11_152_stage, file11_179_stage, file11_183_stage, file11_184_stage, file11_187_stage, file11_269_stage
            from decomp.research import usa_file11_noop_groups
            if file11_stage_mode(manifest) in (143,144,152,179,183,184,187,269):
                adapter = {143:file11_143_stage,144:file11_144_stage,152:file11_152_stage,179:file11_179_stage,183:file11_183_stage,184:file11_184_stage,187:file11_187_stage,269:file11_269_stage}[file11_stage_mode(manifest)]
                sources.update('research/file11_143_candidate/'+chunk['name']+'.c'
                               for chunk in adapter.load_fixture()['chunks'] if chunk['kind']=='c')
            else:
                sources.update('research/'+source for source, _, _, _ in overlay_file11.SOURCE_SPECS)
                if manifest['overlay_file11_stage'] == {'format': usa_file11_noop_groups.STAGE_FORMAT}:
                    sources.update('research/'+name+'.c' for _, _, name in usa_file11_noop_groups.GROUPS)
        sources.update(stage['source'] for stage in manifest_file13_stages(manifest))
        cross = crossregion47_stage(manifest)
        if cross:
            sources.update('research/jp_recomp_to_c/src/'+entry['name']+'.c'
                           for entry in cross['functions'])
        if manifest.get('overlay_native87_stage') is not None:
            from decomp.overlay_native87 import load_fixture
            sources.update('research/usa_main_overlay_87_20261118/sources/'+e['name']+'.c'
                           for e in load_fixture()['functions'])
        self.assertEqual(set(result['sources_sha256_lf']),sources)
        for name in sources:
            patches=[p for p in manifest.get('existing_source_patches', []) if p['source']==name]
            if patches:
                self.assertEqual(result['sources_sha256_lf'][name],patches[0]['patched_sha256_lf'])
            else:
                if name.startswith('research/file11_143_candidate/'):
                    from decomp import file11_143_stage, file11_144_stage, file11_152_stage
                    adapter = {143:file11_143_stage,144:file11_144_stage,152:file11_152_stage,179:file11_179_stage,183:file11_183_stage,184:file11_184_stage,187:file11_187_stage,269:file11_269_stage}[file11_stage_mode(manifest)]
                    stem=name.rsplit('/',1)[-1].removesuffix('.c')
                    data=next(chunk['source'].encode('utf-8') for chunk in adapter.load_fixture()['chunks'] if chunk.get('name')==stem)
                else:
                    data=(ROOT/'decomp'/name).read_bytes().replace(b'\r\n',b'\n')
                self.assertEqual(hashlib.sha256(data).hexdigest(),result['sources_sha256_lf'][name],name)
        self.assertEqual(result['object_layout']['payload_bytes_changed'],0)
        self.assertTrue(result['assignment_table']['matched'])

    def test_assembly_slice_padding_override_is_narrow_and_preserves_payload(self):
        manifest=load_manifest(ROOT/'decomp/manifest.json')
        with tempfile.TemporaryDirectory() as folder:
            bad=copy.deepcopy(manifest);bad['units'][0]['asm_no_padding']=['../escape']
            path=Path(folder)/'bad.json';path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError,'no-padding'):load_manifest(path)
            checkout=Path(folder)/'candidate';(checkout/'config/usa').mkdir(parents=True)
            (checkout/'src').mkdir();(checkout/'Makefile').write_text('original make rules\n')
            sources=Path(folder)/'sources';sources.mkdir();(sources/'unit.c').write_text('void f(void) {}\n')
            (checkout/'config/usa/splat.yaml').write_text('[0x1000, asm]\n')
            payload=checkout/'original.s';payload.write_bytes(b'unchanged assembly')
            small={'units':[dict(source='unit.c',splat_original='[0x1000, asm]',splat_replacement='[0x1000, c, unit]',asm_no_padding=['1000','1014'])]}
            apply_units(checkout,small,sources)
            make=(checkout/'Makefile').read_text()
            self.assertIn('build/usa/asm/usa/1000.s.o: ASFLAGS += --no-pad-sections',make)
            self.assertIn('build/usa/asm/usa/1014.s.o: ASFLAGS += --no-pad-sections',make)
            self.assertTrue(make.startswith('original make rules'))
            self.assertEqual(payload.read_bytes(),b'unchanged assembly')
