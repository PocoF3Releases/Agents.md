import copy
import unittest
from validate_knowledge import privacy_errors, repository_errors


class SourcePrivacyTests(unittest.TestCase):
    def record(self):
        return {'schema_version': 4, 'observed': '2026-09-30', 'repositories': [
            {'repository': 'https://github.com/org/source', 'selected_ref': 'main',
             'refs': {'main': 'a' * 40}, 'source_tree_paths': ['hardware/example'],
             'local_a17': 'matches_selected_ref'}]}

    def test_valid_source(self):
        self.assertEqual(repository_errors(self.record()), [])

    def test_missing_selected_ref(self):
        data = self.record(); data['repositories'][0]['selected_ref'] = 'absent'
        self.assertTrue(repository_errors(data))

    def test_moving_ref_is_not_identity(self):
        data = self.record(); data['repositories'][0]['refs']['main'] = 'HEAD'
        self.assertTrue(repository_errors(data))

    def test_duplicate_source_path(self):
        data = self.record(); entry = copy.deepcopy(data['repositories'][0])
        entry['repository'] += '-other'; data['repositories'].append(entry)
        self.assertTrue(repository_errors(data))

    def test_invalid_local_observation(self):
        data = self.record(); data['repositories'][0]['local_a17'] = {'head': 'main'}
        self.assertTrue(repository_errors(data))

    def test_portable_paths_and_public_urls(self):
        self.assertEqual(privacy_errors('~/evo17 https://github.com/johnmart19/repoindex'), [])
        self.assertEqual(privacy_errors('/home/<linux-user>/evo17'), [])

    def test_personal_paths(self):
        for text in ['/home/example_person/evo17', r'C:\Users\ExamplePerson\Desktop']:
            with self.subTest(text=text):
                self.assertTrue(privacy_errors(text))

    def test_private_key_and_token_patterns(self):
        self.assertTrue(privacy_errors('-----BEGIN OPENSSH PRIVATE KEY-----'))
        self.assertTrue(privacy_errors('ghp_' + 'x' * 25))


if __name__ == '__main__':
    unittest.main()
