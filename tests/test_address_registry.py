"""ROM-free source-of-truth and safety tests for canonical Goemon addresses."""
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch

from practice.address_registry import (
    guest_address, guest_bit, lookup, load_registry, registry_records,
)
from practice.address_catalogue import (
    SNAPSHOT, EXTERNAL, MENTIONS, DISCOVERIES, audit_catalogue,
    build_catalogue, decode_read, search_entries, validate_catalogue,
    validate_entry,
)
from practice.address_catalogue_remote import (
    validate_discoveries, discovery_to_record, merge_remote_catalogue,
    refresh_address_discoveries, load_cached_discoveries,
    refresh_canonical_catalogue, load_cached_catalogue,
    load_catalogue_cache_info, merge_remote_metadata, canonical_url,
)
from practice.unlocks import UNLOCKS
from practice.story_progress import FLAGS
from practice.region_memory_crosswalk import CROSS_REGION_FIELDS


class GuestRAM:
    def __init__(self):
        self.buffer = {}

    def set(self, address, value):
        for i, b in enumerate(value):
            self.buffer[address+i] = b

    def read_guest(self, address, length):
        return bytes(self.buffer.get(address+i, 0) for i in range(length))


class RegistryTests(unittest.TestCase):
    def test_manifest_complete_and_versioned(self):
        payload, ids = load_registry()
        validate_catalogue(payload)
        self.assertEqual(payload["format"], "goemon-address-catalogue-v1")
        self.assertGreaterEqual(len(payload["entries"]), 440)
        self.assertGreaterEqual(len(ids), len(payload["entries"]))
        self.assertEqual(len(registry_records()), len(payload["entries"]))
        stats = audit_catalogue(payload)
        self.assertEqual(stats["total_records"], len(payload["entries"]))
        self.assertGreaterEqual(stats["experimental_japan_flags"], 58)
        self.assertGreaterEqual(stats["live_readable"], 330)
        self.assertGreaterEqual(stats["research_only"], 75)

    def test_every_menu_item_resolves_only_registry_addresses(self):
        self.assertEqual(len(UNLOCKS), 34)
        for entry in UNLOCKS:
            self.assertEqual(entry.address, guest_address(
                "unlock:usa:" + entry.slug, region="usa", width=1))
        self.assertEqual(guest_address("unlock:usa:mini_ebisumaru"),
                         0x8015C6F3)

    def test_story_progress_flags_take_address_and_mask_from_registry(self):
        self.assertEqual(len(FLAGS), 142)
        for flag in FLAGS:
            self.assertEqual((flag.address, flag.mask), guest_bit(
                "story:usa:" + flag.key, region="usa"))
        self.assertEqual(guest_bit("story:usa:benkei_encounter"),
                         (0x8015C60C, 0x20))

    def test_counterparts_and_snowflake_exception(self):
        for field in CROSS_REGION_FIELDS:
            self.assertEqual(field.usa, guest_address(
                "crosswalk:usa:" + field.key, region="usa",
                width=field.width))
            self.assertEqual(field.japan, guest_address(
                "crosswalk:japan:" + field.key, region="japan",
                width=field.width))
        snow = lookup("crosswalk:japan:unlock:snowflake")
        self.assertEqual(snow["address"], "0x80162057")
        self.assertEqual(snow["counterpart"], "0x8015C866")
        self.assertEqual(int(snow["address"], 16) - int(snow["counterpart"], 16),
                         0x57F1)
        self.assertEqual(lookup("crosswalk:japan:static:pause_byte")
                         ["confidence"], "disputed")

    def test_every_japan_story_bit_stays_accessible_without_evidence_gate(self):
        from practice.unlock_flag_catalog import JAPAN_FLAGS, flags_for_region
        self.assertEqual(len(JAPAN_FLAGS), 58)
        for flag in flags_for_region("japan"):
            self.assertEqual((flag.address, flag.mask), guest_bit(
                "crosswalk:japan:" +
                ("plasma:" if flag.key.startswith("plasma_") else "event:") +
                flag.key, region="japan"))
            self.assertTrue(flag.editable)

    def test_external_leads_repeat_and_code_category(self):
        catalogue = load_registry()[0]
        external = json.loads(EXTERNAL.read_text(encoding="utf-8"))
        self.assertEqual(len(external["new_usa_address_leads"]), 25)
        for i, lead in enumerate(external["new_usa_address_leads"]):
            row = lookup(f"external:usa:{i:02d}")
            self.assertEqual(row["address"].lower(), lead["address"].lower())
            self.assertFalse(row["live_readable"])
        slots = [lookup(f"external:warp_slot:{i:02d}")
                 for i in range(1, 12)]
        self.assertEqual([int(x["address"], 16) for x in slots],
                         [0x8015C8B7 + i * 4 for i in range(11)])
        for row in catalogue["entries"]:
            if row["category"] in ("overlay_patch", "cheat_format", "code_vma"):
                self.assertFalse(row["live_readable"])

    def test_vm_research_separate_from_experimental_transformation(self):
        expected = {
            "vm_text_stream_cursor": (0x801C77E8, "u32"),
            "vm_loaded_resource_base": (0x801C77FC, "u32"),
            "vm_relocation_delta": (0x801C78F0, "u32"),
            "vm_active_countdown": (0x801C77F8, None),
            "vm_countdown_input": (0x801C7740, None),
            "vm_text_pacing": (0x801C77A0, None),
            "vm_segment": (0x801C78EC, None),
            "vm_choice_record": (0x801C7800, "u32"),
            "vm_dialogue_windows": (0x80167C48, None),
        }
        for key, (address, kind) in expected.items():
            row = lookup("research:" + key)
            self.assertEqual(int(row["address"], 16), address)
            self.assertEqual(row["data_type"], kind)
        self.assertEqual(lookup("research:ebisumaru_active_timer")
                         ["data_type"], "s16")
        self.assertEqual(lookup("research:ebisumaru_size_byte")
                         ["address"], "0x801C159A")
        self.assertNotEqual(
            lookup("research:ebisumaru_active_timer")["address"],
            lookup("unlock:usa:mini_ebisumaru")["address"])

    def test_duplicate_story_source_provenance_collapses_to_one_field(self):
        matches = [
            row for row in registry_records()
            if row['region'] == 'usa' and
            row['address'] == '0x8015C62D' and
            row.get('mask') == '0x20'
        ]
        self.assertEqual(len(matches), 1)
        row = matches[0]
        self.assertEqual(row['id'], 'story:usa:lord_event_enabled')
        alias = 'crosswalk:usa:event:lord_event_enabled'
        self.assertIn(alias, row.get('id_aliases', []))
        self.assertIs(lookup(alias), lookup(row['id']))
        tags = {item['confidence'] for item in
                row.get('confidence_sources', [])}
        self.assertTrue({'usa_source', 'research_observed'} <= tags)
        # Bits with distinct masks in a shared saved byte are not conflated.
        same_byte = [
            item for item in registry_records()
            if item['region'] == 'usa' and
            item['address'] == row['address'] and
            item.get('mask') != row['mask']
        ]
        self.assertTrue(same_byte)

    def test_overlaps_are_not_lost(self):
        rows = registry_records()
        names = {(r["region"], r["address"], r.get("mask"))
                 for r in rows}
        self.assertGreaterEqual(len(rows), len(names))
        benkei_address = [
            r for r in rows if r["address"] == "0x8015C60C"
            and r["region"] == "usa"]
        self.assertGreaterEqual(len(benkei_address), 2)

    def test_big_endian_guest_values_and_signed_fields(self):
        ram = GuestRAM()
        pointer = lookup("research:vm_text_stream_cursor")
        ram.set(int(pointer["address"], 16), b"\x80\x1c\x77\xe8")
        decoded, raw = decode_read(ram, pointer)
        self.assertEqual(decoded, str(0x801C77E8))
        self.assertEqual(raw, "0x801C77E8")
        timer = lookup("research:ebisumaru_active_timer")
        ram.set(int(timer["address"], 16), struct.pack(">h", -2))
        value, raw = decode_read(ram, timer)
        self.assertEqual(value, "-2")
        self.assertEqual(raw, "0xFFFE")
        # The guest adapter supplies canonical big-endian bytes independent
        # of whether the host's emulator buffer uses a swapped word layout.
        swapped_host = b"\xe8\x77\x1c\x80"
        self.assertNotEqual(swapped_host, bytes.fromhex(raw[2:]))
        unknown = lookup("external:warp_slot:01")
        self.assertEqual(decode_read(ram, unknown)[0].split(":")[0],
                         "Unavailable")

    def test_filters_search_partial_hex_metadata_and_disputed(self):
        payload = load_registry()[0]
        self.assertIn("research:vm_text_stream_cursor",
                      [r["id"] for r in search_entries(payload, "1c77e8")])
        self.assertIn("research:vm_text_stream_cursor",
                      [r["id"] for r in search_entries(payload, "text-stream")])
        candidates = search_entries(
            payload, region="japan", evidence="candidate")
        self.assertTrue(candidates)
        self.assertTrue(all(r["region"] == "japan" for r in candidates))
        self.assertTrue(search_entries(payload, "pause", evidence="disputed"))

    def test_invalid_type_or_bad_writable_location_rejected(self):
        row = dict(lookup("research:vm_text_stream_cursor"))
        row["data_type"] = "exec"
        with self.assertRaises(ValueError):
            validate_entry(row)
        row = dict(lookup("external:usa:00"))
        row["live_readable"] = True
        with self.assertRaises(ValueError):
            validate_entry(row)

    def test_automatic_registry_generation_is_reproducible(self):
        from scripts.sync_address_catalogue import synchronise
        payload = load_registry()[0]
        out, conflicts, added = synchronise(payload)
        self.assertFalse(conflicts, conflicts)
        self.assertEqual(added, 0)
        self.assertEqual(set(r["id"] for r in payload["entries"]),
                         set(r["id"] for r in out["entries"]))


class RefreshTests(unittest.TestCase):
    def test_remote_manifest_parses_but_never_grants_write_control(self):
        manifest = json.loads(DISCOVERIES.read_text(encoding="utf-8"))
        validate_discoveries(manifest)
        merged, status = merge_remote_catalogue(load_registry()[0], manifest)
        self.assertEqual(status["added"], 0)
        self.assertEqual(len(merged["entries"]), len(registry_records()))
        self.assertIsNone(merged["entries"][
            next(i for i, row in enumerate(merged["entries"])
                 if row["id"] == "research:vm_text_stream_cursor")].get("control"))

    def test_full_canonical_refresh_preserves_original_editors(self):
        base = load_registry()[0]
        remote = json.loads(json.dumps(base))
        item = next(r for r in remote["entries"]
                    if r["id"] == "story:usa:benkei_encounter")
        item["address"] = "0x80150010"
        item["mask"] = "0x01"
        item["confidence"] = "unverified_new_test"
        extra = dict(lookup("research:vm_text_stream_cursor"))
        extra["id"] = "remote:experimental_new_scalar"
        extra["address"] = "0x801C7770"
        extra["name"] = "New read-only runtime discovery"
        extra["control"] = "Unlocks / Items & equipment"
        remote["entries"].append(extra)
        merged, counts = merge_remote_metadata(base, remote)
        retained = next(r for r in merged["entries"]
                        if r["id"] == "story:usa:benkei_encounter")
        self.assertEqual(retained["address"], "0x8015C60C")
        self.assertEqual(retained["mask"], "0x20")
        self.assertEqual(retained["confidence"], "unverified_new_test")
        added = next(r for r in merged["entries"]
                     if r["id"] == "remote:experimental_new_scalar")
        self.assertIsNone(added["control"])
        self.assertTrue(added["live_readable"])
        self.assertEqual(counts["added"], 1)

    def test_full_registry_refresh_is_bounded_cached_and_offline(self):
        payload = SNAPSHOT.read_bytes()
        class Response:
            def __init__(self, url, blob):
                self.url, self.blob = url, blob
            def geturl(self):
                return self.url
            def read(self, limit):
                return self.blob[:limit]
            def close(self):
                pass
        with tempfile.TemporaryDirectory() as folder:
            cache = Path(folder) / "full.json"
            meta = Path(folder) / "info.json"
            url = canonical_url("main")
            doc, info = refresh_canonical_catalogue(
                cache_path=cache, info_path=meta,
                opener=lambda *args, **kwargs: Response(url, payload))
            self.assertEqual(doc["format"], "goemon-address-catalogue-v1")
            self.assertEqual(load_cached_catalogue(cache), doc)
            self.assertEqual(load_catalogue_cache_info(meta)["last_sync"],
                             info["last_sync"])
            self.assertTrue(info["upstream_revision"])
            with self.assertRaises(ValueError):
                refresh_canonical_catalogue(
                    cache_path=cache, info_path=meta,
                    opener=lambda *a, **kw: Response(
                        "https://wrong.example/catalogue", payload))
            self.assertEqual(cache.read_bytes(), payload)
            with self.assertRaises(ValueError):
                refresh_canonical_catalogue(
                    cache_path=cache, info_path=meta,
                    opener=lambda *a, **kw: Response(url, b"bad json"))
            self.assertEqual(cache.read_bytes(), payload)

    def test_rejects_cheat_as_live_reader(self):
        manifest = json.loads(DISCOVERIES.read_text(encoding="utf-8"))
        invalid = dict(manifest)
        invalid["entries"] = [dict(manifest["entries"][0],
                                   category="code_vma",
                                   live_readable=True)]
        with self.assertRaises(ValueError):
            validate_discoveries(invalid)

    def test_invalid_network_refresh_keeps_old_cache(self):
        from practice.address_catalogue_remote import remote_url
        url = remote_url("main")
        class FakeResponse:
            def __init__(self, data, location=url):
                self.data = data
                self.location = location
            def read(self, length):
                return self.data[:length]
            def geturl(self):
                return self.location
            def close(self):
                pass
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory) / "catalogue.json"
            original = DISCOVERIES.read_bytes()
            cache.write_bytes(original)
            bad = FakeResponse(b'{"format": "wrong"}')
            with self.assertRaises(ValueError):
                refresh_address_discoveries(
                    cache_path=cache,
                    opener=lambda *args, **kwargs: bad)
            self.assertEqual(cache.read_bytes(), original)
            redirect = FakeResponse(original, "https://evil.example/catalogue")
            with self.assertRaises(ValueError):
                refresh_address_discoveries(
                    cache_path=cache,
                    opener=lambda *args, **kwargs: redirect)
            self.assertEqual(cache.read_bytes(), original)
            assert load_cached_discoveries(cache) is not None

    def test_good_remote_cache_is_atomic_and_offline_reusable(self):
        from practice.address_catalogue_remote import remote_url
        class FakeResponse:
            def geturl(self):
                return remote_url("main")
            def read(self, size):
                return DISCOVERIES.read_bytes()[:size]
            def close(self):
                pass
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory) / "catalogue.json"
            doc, info = refresh_address_discoveries(
                cache_path=cache,
                opener=lambda *args, **kwargs: FakeResponse())
            self.assertTrue(info["upstream_revision"])
            self.assertEqual(doc, load_cached_discoveries(cache))


if __name__ == "__main__":
    unittest.main()
