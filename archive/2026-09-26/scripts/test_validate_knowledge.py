"""Regression tests use isolated temporary repositories, never live project files."""
import tempfile
import contextlib
import io
import json
from unittest.mock import patch
import unittest
from pathlib import Path

from validate_knowledge import (AGENTS_BUDGET, GOVERNANCE, index_paths,
                                load_index, local_target, main, markdown_targets, validate)

INDEX = '''schema_version: 1
entrypoints: {rules: AGENTS.md}
read_order: {normal: [AGENTS.md], optional_router: INDEX.yaml}
subsystems:
  sample: {status: durable, memory: memory/sample.md}
maintenance: {}
'''


class KnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repo'
        self.root.mkdir()
        for name in (*GOVERNANCE, 'memory/sample.md'):
            self.write(name, '# Example\n')
        self.write('INDEX.yaml', INDEX)

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')

    def test_valid_repository(self):
        errors, count = validate(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(count, 4)

    def test_duplicate_key_rejected(self):
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            load_index(INDEX + 'entrypoints: {}\n')

    def test_malformed_yaml_reported(self):
        self.write('INDEX.yaml', 'entrypoints: [\n')
        self.assertTrue(validate(self.root)[0])

    def test_wrong_shape_rejected(self):
        for text in ('[]', 'schema_version: true', INDEX.replace('maintenance: {}', 'maintenance: []')):
            with self.subTest(text=text), self.assertRaises(ValueError):
                load_index(text)

    def test_optional_router_not_mandatory(self):
        with self.assertRaisesRegex(ValueError, 'optional'):
            load_index(INDEX.replace('[AGENTS.md]', '[AGENTS.md, INDEX.yaml]'))

    def test_missing_target(self):
        self.write('README.md', '[missing](missing.md)\n')
        self.assertTrue(any('missing target' in e for e in validate(self.root)[0]))

    def test_parent_link_inside_repo(self):
        self.assertEqual(local_target('memory/example.md', '../AGENTS.md#rules'), 'AGENTS.md')

    def test_traversal_and_absolute_paths(self):
        for target in ('../outside.md', '%2e%2e/outside.md', '/tmp/test', 'C:\\test', 'file:///tmp/test'):
            with self.subTest(target=target), self.assertRaises(ValueError):
                local_target('README.md', target)

    def test_symlink_escape(self):
        outside = self.root.parent / 'outside.md'
        outside.write_text('outside')
        try:
            (self.root / 'escape.md').symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest('symlink creation not available')
        self.write('README.md', '[escape](escape.md)')
        self.assertTrue(any('symlink escapes' in e for e in validate(self.root)[0]))

    def test_external_links_and_anchors(self):
        for target in ('https://openai.com/a', 'mailto:maintainer@example.com', '#local', '//example.org/a'):
            self.assertIsNone(local_target('README.md', target))

    def test_index_cannot_use_external_route(self):
        self.write('INDEX.yaml', INDEX.replace('memory/sample.md', 'https://example.org/sample.md'))
        self.assertTrue(any('repository-local' in e for e in validate(self.root)[0]))

    def test_code_and_comments_ignored(self):
        text = '```md\n[x](missing.md)\n```\n`[x](other.md)`\n<!-- [x](secret.md) -->\n[ok](AGENTS.md)'
        self.assertEqual(list(markdown_targets(text)), ['AGENTS.md'])

    def test_tilde_fences_and_references(self):
        text = '~~~md\n[x](missing.md)\n~~~\n[ref]: <AGENTS.md> "Rules"\n[x](START_HERE.md "Start")'
        self.assertEqual(set(markdown_targets(text)), {'AGENTS.md', 'START_HERE.md'})

    def test_budget_is_utf8_bytes(self):
        self.write('AGENTS.md', 'é' * (AGENTS_BUDGET // 2 + 1))
        self.assertTrue(any('8 KiB' in e for e in validate(self.root)[0]))

    def test_metadata_mode_does_not_require_target_contents(self):
        (self.root / 'memory/sample.md').unlink()
        self.assertEqual(validate(self.root, inventory={'AGENTS.md', 'INDEX.yaml', 'memory/sample.md'})[0], [])

    def test_metadata_mode_still_requires_source_contents(self):
        (self.root / 'README.md').unlink()
        self.assertTrue(validate(self.root, inventory={'AGENTS.md', 'INDEX.yaml', 'memory/sample.md'})[0])

    def test_repository_roles_are_not_local_paths(self):
        data = load_index(INDEX)
        data['subsystems']['sample']['repository_roles'] = {'implementation': 'hardware/xiaomi'}
        self.assertNotIn('hardware/xiaomi', list(index_paths(data)))

    def test_bad_route_value_reported(self):
        self.write('INDEX.yaml', INDEX.replace('{rules: AGENTS.md}', '{rules: 42}'))
        self.assertTrue(any('non-string' in e for e in validate(self.root)[0]))

    def test_extra_file_checked(self):
        self.write('today/new.md', '[broken](missing.md)')
        self.assertTrue(any('today/missing.md' in e for e in validate(self.root, ('today/new.md',))[0]))


    def run_cli(self, data):
        path = self.root.parent / 'inventory.json'
        path.write_text(json.dumps(data), encoding='utf-8')
        output = io.StringIO()
        with patch('sys.argv', ['validate', '--root', str(self.root), '--inventory', str(path)]), contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            result = main()
        return result, output.getvalue()

    def test_inventory_cli_with_candidate(self):
        result, output = self.run_cli({'revision': 'a' * 40,
            'paths': ['AGENTS.md', 'INDEX.yaml'],
            'candidate_paths': ['memory/sample.md']})
        self.assertEqual(result, 0)
        self.assertIn('1 candidate files', output)

    def test_inventory_rejects_unavailable_candidate(self):
        result, output = self.run_cli({'revision': 'a' * 40,
            'paths': ['AGENTS.md', 'INDEX.yaml'],
            'candidate_paths': ['missing.md']})
        self.assertEqual(result, 1)
        self.assertIn('unavailable', output)

    def test_inventory_requires_immutable_revision(self):
        result, output = self.run_cli({'revision': 'main', 'paths': []})
        self.assertEqual(result, 1)
        self.assertIn('immutable', output)

if __name__ == '__main__':
    unittest.main()
