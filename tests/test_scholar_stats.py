import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

spec = importlib.util.spec_from_file_location('stats', Path(__file__).resolve().parents[1] / 'update_stats.py')
stats = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stats)

PROFILE = '''<div id="gsc_prf_in">Jinchao Song</div>
<table id="gsc_rsb_st"><thead><tr><th></th><th>All</th><th>Since 2021</th></tr></thead>
<tbody><tr><td><a>Citations</a></td><td>1,105</td><td>927</td></tr>
<tr><td>h-index</td><td>11</td><td>10</td></tr>
<tr><td>i10-index</td><td>11</td><td>10</td></tr></tbody></table>'''


class ScholarStatsTests(unittest.TestCase):
    def test_uses_all_time_column_and_parses_thousands(self):
        snapshot = stats.parse_profile(PROFILE)
        self.assertEqual((snapshot['citationCount'], snapshot['hIndex']), (1105, 11))
        self.assertEqual(snapshot['source'], 'Google Scholar')
        self.assertNotIn('i10Index', snapshot)

    def test_rejects_challenge_pages_and_wrong_profiles(self):
        for page in ['<html>CAPTCHA</html>', PROFILE.replace('Jinchao Song','Someone Else')]:
            with self.assertRaises(ValueError):
                stats.parse_profile(page)

    def test_rejects_missing_values_and_reordered_columns(self):
        for page in [PROFILE.replace('1,105','—'), PROFILE.replace('h-index','Other metric'),
                     PROFILE.replace('<th>All</th><th>Since 2021</th>','<th>Since 2021</th><th>All</th>')]:
            with self.assertRaises(ValueError):
                stats.parse_profile(page)

    def test_a_different_source_cannot_overwrite_scholar(self):
        snapshot = stats.parse_profile(PROFILE)
        with self.assertRaises(ValueError):
            stats.validate_stats({**snapshot,'source':'Semantic Scholar'})

    def test_fetch_failure_preserves_previous_snapshot_byte_for_byte(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)/'metrics.json'
            old = json.dumps(stats.parse_profile(PROFILE)).encode()
            destination.write_bytes(old)
            with patch.object(stats,'DESTINATION',destination), patch.object(stats,'urlopen',side_effect=HTTPError(stats.PROFILE_URL,403,'Forbidden',{},None)):
                with self.assertRaises(HTTPError):
                    stats.main()
            self.assertEqual(destination.read_bytes(),old)


if __name__=='__main__':
    unittest.main()
