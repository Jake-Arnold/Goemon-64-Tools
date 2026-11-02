import unittest
from practice.scenes import SCENES,EXTERNAL_SCENE_NAMES,unidentified_scene_name,scene_label


class SceneNameTests(unittest.TestCase):
    def test_existing_room_labels_remain_and_known_missing_rooms_are_named(self):
        self.assertEqual(SCENES[0],'Oedo Castle 1F Tile Room')
        self.assertEqual(SCENES[353],'Oedo Town (South)')
        self.assertEqual(SCENES[3],'Oedo Castle 1F Swatting Robot Silver Key Room')
        self.assertEqual(SCENES[4],'Oedo Castle 1F Gold Dango Room')
        self.assertEqual(SCENES[11],'Oedo Castle 2F Silver Cat Room')
        self.assertEqual(len(EXTERNAL_SCENE_NAMES),125)
        self.assertEqual(len(SCENES),305)

    def test_unresolved_rooms_are_explicit_and_have_native_menu_indices(self):
        self.assertNotIn(55,SCENES)
        self.assertEqual(unidentified_scene_name(55),'Unidentified room (SIRO 55)')
        self.assertEqual(unidentified_scene_name(342),'Unidentified room (DOUCHU 42)')
        self.assertEqual(unidentified_scene_name(469),'Unidentified room (SHOP 69)')
        self.assertIn('Unidentified',scene_label(55))
        self.assertIn('Swatting Robot',scene_label(3))
