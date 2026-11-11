"""Read-only ELF32 MIPS inspection for isolated, relocated function probes."""
from dataclasses import dataclass
from pathlib import Path
import re
import struct


@dataclass(frozen=True)
class Symbol:
    name: str
    value: int
    size: int
    kind: int
    binding: int
    section: int


class Elf32:
    def __init__(self, data):
        self.data = bytes(data)
        if len(data) < 52 or data[:7] != b'\x7fELF\x01\x02\x01':
            raise ValueError('Expected ELF32 big-endian version-1 image')
        self.kind, machine = struct.unpack_from('>HH', data, 16)
        if machine != 8 or self.kind not in (1, 2):
            raise ValueError('Expected relocatable or executable MIPS ELF')
        offset = struct.unpack_from('>I', data, 32)[0]
        width, count, names = struct.unpack_from('>HHH', data, 46)
        if width != 40 or not count or names >= count or offset + width * count > len(data):
            raise ValueError('Invalid ELF section table')
        self.sections = [struct.unpack_from('>10I', data, offset + i * width) for i in range(count)]
        table = self.payload(names)
        self.names = [self.string(table, s[0]) for s in self.sections]
        self.symbols = []
        for section in self.sections:
            if section[1] != 2:
                continue
            if section[9] != 16 or section[5] % 16 or section[6] >= count:
                raise ValueError('Invalid ELF symbol table')
            strings = self.payload(section[6])
            content = self.slice(section[4], section[5])
            for start in range(0, len(content), 16):
                name, value, size, info, _, target = struct.unpack_from('>IIIBBH', content, start)
                self.symbols.append(Symbol(self.string(strings, name), value, size, info & 15, info >> 4, target))

    @staticmethod
    def string(table, start):
        end = table.find(b'\0', start) if 0 <= start < len(table) else -1
        if end < 0:
            raise ValueError('Invalid ELF string offset')
        return table[start:end].decode('ascii')

    def slice(self, start, size):
        if start < 0 or size < 0 or start + size > len(self.data):
            raise ValueError('ELF payload outside file')
        return self.data[start:start + size]

    def payload(self, index):
        if index >= len(self.sections):
            raise ValueError('Invalid ELF section index')
        section = self.sections[index]
        return b'' if section[1] == 8 else self.slice(section[4], section[5])

    def function(self, name):
        matches = [s for s in self.symbols if s.name == name and s.kind == 2 and s.size > 0 and 0 < s.section < len(self.sections)]
        if len(matches) != 1:
            raise ValueError('Missing/ambiguous function: ' + name)
        return matches[0]

    def code(self, symbol):
        section = self.sections[symbol.section]
        relative = symbol.value - section[3]
        if not section[2] & 4 or section[1] == 8 or relative < 0 or relative + symbol.size > section[5]:
            raise ValueError('Function outside executable section')
        return self.slice(section[4] + relative, symbol.size)

    def globals(self):
        result = {}
        for symbol in self.symbols:
            if not symbol.name or symbol.binding not in (1, 2) or symbol.section == 0:
                continue
            if symbol.name in result and result[symbol.name] != symbol.value:
                raise ValueError('Ambiguous global: ' + symbol.name)
            result[symbol.name] = symbol.value
        return result

    def undefined(self):
        return {s.name for s in self.symbols if s.name and s.binding in (1, 2) and s.section == 0}

    def layout_reason(self, name):
        if any(s.section == 0xFFF2 for s in self.symbols):
            return 'generated_common_data'
        functions = [s for s in self.symbols if s.kind == 2 and s.size and s.section]
        if len(functions) != 1 or functions[0].name != name or functions[0].value != 0:
            return 'additional_functions_or_text_layout'
        metadata = {'.reginfo', '.MIPS.abiflags', '.MIPS.options', '.pdr'}
        for label, section in zip(self.names, self.sections):
            if section[2] & 2 and section[5] and label != '.text' and label not in metadata:
                return 'generated_allocated_data:' + label
        return None


def linker_script(name, address, undefined, globals_map):
    safe = re.compile(r'[A-Za-z_.$][A-Za-z0-9_.$]*\Z')
    if not safe.fullmatch(name) or not 0 <= address <= 0xFFFFFFFF:
        raise ValueError('Invalid probe entry')
    missing = sorted(set(undefined) - set(globals_map))
    if missing:
        raise ValueError('Unresolved baseline symbols: ' + ', '.join(missing))
    definitions = []
    for symbol in sorted(undefined):
        if not safe.fullmatch(symbol):
            raise ValueError('Unsupported linker symbol: ' + symbol)
        definitions.append(f'{symbol} = 0x{globals_map[symbol]:08X};')
    return (f'ENTRY({name})\nSECTIONS {{ .text 0x{address:08X} : SUBALIGN(4) {{ *(.text) }} '
            '/DISCARD/ : { *(*) } }\n' + '\n'.join(definitions) + '\n')


def compare_code(expected, actual):
    import hashlib
    offsets = [i for i in range(0, max(len(expected), len(actual)), 4)
               if expected[i:i+4] != actual[i:i+4]]
    return dict(expected_size=len(expected), actual_size=len(actual),
                byte_differences=sum(a != b for a, b in zip(expected, actual)) + abs(len(expected) - len(actual)),
                word_differences=len(offsets), word_mismatch_offsets=offsets,
                first_mismatch_offset=offsets[0] if offsets else None,
                expected_sha256=hashlib.sha256(expected).hexdigest(),
                actual_sha256=hashlib.sha256(actual).hexdigest())
