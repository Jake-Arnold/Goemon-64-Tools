import unittest
from practice.backends.memory import Rdram
from tests.test_checkpoint import TestCheckpoint
from practice.inspector import get_watches, checkpoint_differences
from practice.checkpoints import capture_checkpoint, MAP_ADDR, PHASE_ADDR, GAMEDATA_ADDR
from practice.scenes import SCENES, scene_label
from practice.scene_controls import open_native_debug_menu


class TestInspector(unittest.TestCase):
    def sample(self):
        return TestCheckpoint().sample()

    def test_live_resources_and_inventory(self):
        proc, ram=self.sample()
        ram.write_guest(0x8015C6BF, b'\x01')
        ram.write_guest(0x8015C5F3, b'\x03')
        rows={r.name:r for r in get_watches(ram,ram.snapshot(),SCENES)}
        self.assertEqual(rows['Ryo'].raw,'0x00000064')
        self.assertEqual(rows['Lives'].value,'3')
        self.assertEqual(rows['Chain Pipe'].raw,'0x01')
        self.assertEqual(rows['Item slot 1 code'].value,'3')
        self.assertEqual(rows['Equipped weapon index'].addr,0x8015C607)
        self.assertEqual(rows['Equipped weapon index'].status,'CHECK')
        self.assertEqual(rows['Map overlay state (observed)'].addr,0x8015C574)
        self.assertEqual(rows['Map ID'].raw,'0x0023')

    def test_rom_grounded_vm_watches_are_read_only_and_distinct(self):
        _, ram = self.sample()
        ram.write_guest(0x80077858, (0x8003D000).to_bytes(4, 'big'))
        ram.write_guest(0x801C77E0, (5).to_bytes(4, 'big'))
        ram.write_guest(0x801C78E8, (1234).to_bytes(4, 'big'))
        ram.write_guest(0x801C78FC, b'\xff')
        rows = {r.name: r for r in get_watches(ram, ram.snapshot(), SCENES)}
        self.assertNotIn('Event/script VM lock', rows)
        self.assertEqual(rows['Script cursor (VM)'].raw, '0x8003D000')
        self.assertEqual(rows['Script VM state'].raw, '0x00000005')
        self.assertEqual(rows['Script resource ID'].addr, 0x801C78E8)
        self.assertEqual(rows['Script VM pause byte'].value, '-1')
        self.assertIn('inferred', rows['Script cursor (VM)'].source)


    def test_vm_state_and_gameplay_submode_labels_are_qualified(self):
        _, ram = self.sample()
        ram.write_guest(0x801C77E0, (2).to_bytes(4, 'big'))
        ram.write_guest(0x800C7AA4, b'\x04')
        rows = {r.name: r for r in get_watches(ram, ram.snapshot(), SCENES)}
        self.assertIn('interactive selection observed', rows['Script VM state'].value)
        self.assertIn('Impact gameplay observed', rows['Gameplay submode'].value)
        self.assertIn('observations', rows['Script VM state'].source)
        # Evidence-backed map-category labels, not verified original enum names.
        for submode, expected in (
            (0, 'dungeon areas observed'),
            (1, 'overworld areas observed'),
            (2, 'towns / villages observed'),
            (3, 'building interiors observed'),
            (4, 'Impact gameplay observed'),
            (7, 'Impact introduction observed'),
        ):
            with self.subTest(submode=submode):
                ram.write_guest(0x800C7AA4, bytes([submode]))
                observed = {r.name: r for r in get_watches(ram, ram.snapshot(), SCENES)}
                self.assertIn(expected, observed['Gameplay submode'].value)
                self.assertEqual(observed['Gameplay submode'].raw, f'0x{submode:02X}')
        ram.write_guest(0x800C7AA4, b'\x04')

        ram.write_guest(0x801C77E0, (7).to_bytes(4, 'big'))
        rows = {r.name: r for r in get_watches(ram, ram.snapshot(), SCENES)}
        self.assertIn('scripted dialogue', rows['Script VM state'].value)
        ram.write_guest(0x801C77E0, (6).to_bytes(4, 'big'))
        rows = {r.name: r for r in get_watches(ram, ram.snapshot(), SCENES)}
        self.assertIn('meaning unknown', rows['Script VM state'].value)

        ram.write_guest(0x800C7A94, b'\x06')
        rows = {r.name: r for r in get_watches(ram, ram.snapshot(), SCENES)}
        self.assertIn('outside ordinary gameplay', rows['Gameplay submode'].value)

    def test_story_flags_are_not_duplicated_in_live_memory(self):
        _,ram=self.sample()
        rows=get_watches(ram,ram.snapshot(),SCENES)
        self.assertFalse(any(row.name.startswith('Story: ') for row in rows))
        self.assertNotIn('Fortune Doll progress (low byte)',{r.name for r in rows})
        self.assertEqual(len(rows),len({r.name for r in rows}))
        # Same stored byte; distinct bits, not redundant flags.
        self.assertIn('Sasuke battery 1 collected',{r.name for r in rows})
        self.assertIn('Sasuke battery 2 cutscene finished (observed)',{r.name for r in rows})

    def test_sasuke_battery_bit_live_watch(self):
        _,ram=self.sample()
        ram.write_guest(0x8015C609,b'\x85')
        rows={r.name:r for r in get_watches(ram,ram.snapshot(),SCENES)}
        self.assertEqual(rows['Sasuke battery 1 collected'].value,'No (bit 0x20)')
        ram.write_guest(0x8015C609,b'\xA5')
        rows={r.name:r for r in get_watches(ram,ram.snapshot(),SCENES)}
        self.assertEqual(rows['Sasuke battery 1 collected'].value,'Yes (bit 0x20)')
        self.assertEqual(rows['Sasuke battery 1 collected'].raw,'0xA5')

    def test_weapon_index_and_map_overlay_live_values(self):
        _,ram=self.sample()
        ram.write_guest(0x8015C607,b'\x02')
        ram.write_guest(0x8015C574,b'\x01')
        watches={r.name:r for r in get_watches(ram,ram.snapshot(),SCENES)}
        self.assertEqual(watches['Equipped weapon index'].raw,'0x02')
        self.assertEqual(watches['Equipped weapon index'].status,'OK')
        self.assertIn('visible',watches['Map overlay state (observed)'].value)
        ram.write_guest(0x8015C607,b'\x04')
        watches={r.name:r for r in get_watches(ram,ram.snapshot(),SCENES)}
        self.assertEqual(watches['Equipped weapon index'].status,'CHECK')
        self.assertIn('fallback',watches['Equipped weapon index'].value)

    def test_confirmed_inventory_slots_and_weapon_sources(self):
        from practice.inspector import INVENTORY
        by_name={name:(addr,hint) for name,addr,_w,_max,hint in INVENTORY}
        self.assertEqual([by_name[name][0] for name in ('Item slot 1 code','Item slot 2 code',
                'Item slot 2 quantity','Item slot 3 code','Item slot 3 quantity')],
                [0x8015C5F3,0x8015C5F7,0x8015C5FB,0x8015C5FF,0x8015C603])
        _,ram=self.sample()
        rows={w.name:w for w in get_watches(ram,ram.snapshot(),SCENES)}
        for name in ('Goemon pipe upgrade','Ebisumaru hammer upgrade','Sasuke kunai upgrade',
                     'Yae katana upgrade','Chain Pipe','Meat Saw Hammer','Fire Cracker Bomb',
                     'Flute','Windup Camera','Ice Kunai','Bazooka','Medal of Flames',
                     'Sudden Impact','Mini Ebisumaru','Super Jump','Magic Mermaid',
                     'Item slot 1 code','Item slot 2 code','Item slot 2 quantity',
                     'Item slot 3 code','Item slot 3 quantity'):
            self.assertTrue(rows[name].source.startswith('confirmed:'), name)

    def test_miracle_shape_labels_match_unlocks(self):
        _,ram=self.sample()
        rows={v.name:v for v in get_watches(ram,ram.snapshot(),SCENES)}
        for name,addr in {'Star':0x8015C85B,'Moon':0x8015C85F,
                          'Flower':0x8015C863,'Snowflake':0x8015C866}.items():
            self.assertEqual(rows[name].addr,addr)
            self.assertTrue(rows[name].source.startswith('confirmed:'))

    def test_native_menu_category_main_is_zero(self):
        from practice.native_menu_categories import NATIVE_MENU_CATEGORIES, native_menu_category
        from practice.native_debug_trace import selection_values
        self.assertEqual(NATIVE_MENU_CATEGORIES[:5], ('MAIN','SIRO','DOUCHU','MACHI','SHOP'))
        self.assertEqual(native_menu_category(13), 'GAMEOVER')
        self.assertEqual([selection_values(x)['category_index'] for x in (90,300,353,465)], [1,2,3,4])
        _,ram=self.sample()
        ram.write_guest(0x800C7A94,b'\x0a')
        ram.write_guest(0x800C7AA4,b'\x00')
        rows={r.name:r for r in get_watches(ram,ram.snapshot(),SCENES)}
        self.assertIn('MAIN',rows['Native menu category'].value)

    def test_invalid_resource_flags_not_silently_accepted(self):
        _, ram=self.sample()
        ram.write_guest(0x8015C5E8,(12000).to_bytes(4,'big'))
        ram.write_guest(0x8015C69F,b'\xAA')
        watches={w.name:w for w in get_watches(ram,ram.snapshot(),SCENES)}
        self.assertEqual(watches['Ryo'].status,'CHECK')
        self.assertEqual(watches['Goemon in party'].status,'CHECK')

    def test_checkpoint_differences_and_stale_mirror(self):
        _,ram=self.sample()
        checkpoint=capture_checkpoint(ram,'test')
        ram.write_guest(GAMEDATA_ADDR + 0x70,b'\x11') # stale mirror, ignored
        comparison=checkpoint_differences(ram,checkpoint)
        self.assertEqual(comparison['total'],0)
        ram.write_guest(GAMEDATA_ADDR+0x140,b'\xAA')
        comparison=checkpoint_differences(ram,checkpoint)
        self.assertEqual(comparison['counts']['gamedata'],1)
        self.assertEqual(comparison['rows'][0][1],f'0x{GAMEDATA_ADDR+0x140:08X}')
        ram.write_guest(MAP_ADDR,b'\x00\x24')
        self.assertFalse(checkpoint_differences(ram,checkpoint)['map_matches'])

    def test_native_debug_state_write_only_when_safe(self):
        _,ram=self.sample()
        self.assertEqual(open_native_debug_menu(ram),10)
        self.assertEqual(ram.u8(0x800C7A94),10)
        self.assertEqual(ram.u16(MAP_ADDR),0x23) # map is never overwritten
        # Entering debug twice is idempotent, not an invalid gameplay state.
        self.assertEqual(open_native_debug_menu(ram), 10)

    def test_scene_labels_are_grounded(self):
        self.assertEqual(SCENES[465],"South Oedo - Goemon's House")
        self.assertIn('Unknown',scene_label(0x777))



    def test_fortune_doll_progress_is_a_word_outside_event_bank(self):
        _,ram=self.sample()
        for value in (0,1,2,3,4,5):
            ram.write_guest(0x8015C704,value.to_bytes(4,'big'))
            ram.write_guest(0x8015C708,(12).to_bytes(4,'big'))
            rows={r.name:r for r in get_watches(ram,ram.snapshot(),SCENES)}
            row=rows['Fortune Doll progress (quarters)']
            self.assertEqual(row.addr,0x8015C704)
            self.assertEqual(row.raw,f'0x{value:08X}')
            self.assertEqual(row.status,'OK' if value<=4 else 'CHECK')
            if value==2:self.assertEqual(row.value,'2/4 (1/2)')
            self.assertEqual(rows['Fortune Dolls obtained (annotated total)'].value,'12')

    def test_all_builtin_watch_names_are_unique_with_same_room_dolls(self):
        _,ram=self.sample()
        rows=get_watches(ram,ram.snapshot(),SCENES)
        names=[r.name for r in rows]
        self.assertEqual(len(names),len(set(names)))

if __name__=='__main__':unittest.main()
