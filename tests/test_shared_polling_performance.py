"""Shared toolkit UI scheduling and regional-read efficiency contracts."""
import unittest
from collections import Counter
from types import SimpleNamespace
from unittest.mock import Mock

from practice.region_views import japan_story_crosswalk_rows
from practice.region_memory_crosswalk import CROSS_REGION_FIELDS
from practice.toolkit import Toolkit


class RegionViewReadEfficiencyTests(unittest.TestCase):
    def test_each_event_byte_is_read_once_per_story_refresh(self):
        reads = Counter()
        class Reader:
            def read_guest(self, address, length):
                reads[(address, length)] += 1
                return bytes(length)
        rows = japan_story_crosswalk_rows(Reader())
        events = tuple(f for f in CROSS_REGION_FIELDS
                       if f.key.startswith(('event:', 'plasma:')))
        locations = {(f.japan, f.width) for f in events}
        self.assertEqual(len(rows), 142)
        self.assertEqual(set(reads), locations)
        self.assertTrue(all(count == 1 for count in reads.values()))
        self.assertLess(len(locations), len(rows))


class SharedPollingTests(unittest.TestCase):
    def _app(self, region, panel):
        app = SimpleNamespace(
            active_version=SimpleNamespace(key=region),
            _visible_main_panel=lambda: panel,
            refresh_inspector=Mock(),
            refresh_unlocks=Mock(),
            refresh_story_progress=Mock(),
            refresh_checkpoint_diff=Mock(),
            refresh_japan_party_controls=Mock(),
            last_inspect_at=1.0)
        return app

    def test_hidden_pages_do_not_refresh_in_either_region(self):
        for region in ('usa', 'japan'):
            with self.subTest(region=region):
                app = self._app(region, 'other')
                Toolkit._poll_visible_panels(app)
                for name in ('refresh_inspector', 'refresh_unlocks',
                             'refresh_story_progress', 'refresh_checkpoint_diff',
                             'refresh_japan_party_controls'):
                    getattr(app, name).assert_not_called()

    def test_each_active_page_refreshes_only_its_own_data(self):
        expected = {
            'watches': 'refresh_inspector',
            'unlocks': 'refresh_unlocks',
            'story': 'refresh_story_progress',
            'dashboard': 'refresh_checkpoint_diff',
        }
        for region in ('usa', 'japan'):
            for panel, method in expected.items():
                with self.subTest(region=region, panel=panel):
                    app = self._app(region, panel)
                    Toolkit._poll_visible_panels(app, force=True)
                    getattr(app, method).assert_called_once()
                    for other in expected.values():
                        if other != method:
                            getattr(app, other).assert_not_called()

    def test_force_watches_refresh_invalidates_throttle_only_once(self):
        app = self._app('usa', 'watches')
        Toolkit._poll_visible_panels(app, force=True)
        self.assertEqual(app.last_inspect_at, 0.0)
        app.refresh_inspector.assert_called_once_with({})


if __name__ == '__main__':
    unittest.main()
