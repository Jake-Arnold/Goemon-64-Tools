"""Synthetic negative controls for the file_12 original-layout gate."""
import hashlib
from unittest import TestCase, mock

from decomp import probe_file12_callbacks as mod


class File12ProbeTests(TestCase):
    def setUp(self):
        self.rom = bytes(range(64))
        self.patches = mock.patch.multiple(
            mod, ROM_SIZE=64, ROM_SHA1=hashlib.sha1(self.rom).hexdigest(),
            ROM_START=0, TEXT_END=32, ROM_END=64,
            TEXT_SHA256=hashlib.sha256(self.rom[:32]).hexdigest(),
            DATA_SHA256=hashlib.sha256(self.rom[32:]).hexdigest())
        self.patches.start()
        self.addCleanup(self.patches.stop)

    def config(self):
        return (f"sha1: {mod.ROM_SHA1}\nsegments:\n"
                "  - name: file_11\n"
                "  - name: file_12\n"
                "    type: code\n"
                "    start: 0x5C8770\n"
                "    vram: 0x8020D2A0\n"
                "    bss_size: 0xE0\n"
                "    subalign: 16\n"
                "    overlay: yes\n"
                "    exclusive_ram_id: static_overlay_2\n"
                "    subsegments:\n"
                "    - [0x5C8770, asm]\n"
                "    - [0x5E3C90, data]\n"
                "  - name: file_13\n"
                "    start: 0x5F6840\n"
                "  - name: file_14\n")

    def test_pinned_layout_accepts_reference(self):
        mod.verify_layout(self.config(), self.rom)

    def test_shifted_vma_rejected(self):
        with self.assertRaisesRegex(ValueError, "section layout"):
            mod.verify_layout(self.config().replace("0x8020D2A0", "0x8020D2B0"), self.rom)

    def test_changed_section_bytes_rejected(self):
        changed = self.rom[:40] + bytes([self.rom[40] ^ 1]) + self.rom[41:]
        with mock.patch.object(mod, "ROM_SHA1", hashlib.sha1(changed).hexdigest()):
            with self.assertRaisesRegex(ValueError, "reference section hash"):
                mod.verify_layout(self.config(), changed)

    def test_duplicate_overlay_rejected(self):
        config = self.config().replace("  - name: file_13\n",
                                       "  - name: file_12\n  - name: file_13\n")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            mod.verify_layout(config, self.rom)

    def test_wrong_end_rejected(self):
        with self.assertRaisesRegex(ValueError, "ROM end"):
            mod.verify_layout(self.config().replace("0x5F6840", "0x5F6850"), self.rom)
