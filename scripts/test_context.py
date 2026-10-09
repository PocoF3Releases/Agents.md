"""Representative cold-start retrieval and containment checks; no remote calls."""
import tempfile
import unittest
from pathlib import Path
from context import bundle, catalog, read_record, search_topics, headings, select_section

ROOT = Path(__file__).resolve().parents[1]


class ContextTests(unittest.TestCase):
    def test_discovery_routes(self):
        index = catalog(ROOT)
        for query, expected in [
            ('gesture vibration', 'haptics'), ('AC4 VNDK', 'audio'),
            ('camera ultrawide 4k60', 'camera'), ('Windows WSL restore', 'recovery'),
            ('Android16 release changelog', 'release'), ('Vulkan Endfield', 'graphics'),
            ('proximity touch translation', 'parts'), ('Ghidra LLVM', 'tools'),
            ('repoindex database', 'indexing'), ('Astra prompt tokens', 'guidance')]:
            with self.subTest(query=query):
                self.assertEqual(search_topics(index, query)[0][0], expected)

    def test_topic_reads_no_startup_or_archive_by_default(self):
        result = bundle(ROOT, 'haptics')
        self.assertEqual([f['path'] for f in result['files']], ['memory/haptics.md'])
        self.assertEqual(result['bytes'], len(result['files'][0]['text'].encode('utf-8')))

    def test_startup_is_bounded(self):
        result = bundle(ROOT, 'camera', startup=True)
        self.assertEqual([f['path'] for f in result['files']],
                         ['AGENTS.md', 'CURRENT_STATE.md', 'memory/miuicamera.md'])
        self.assertFalse(any(f['path'].startswith('archive/') for f in result['files']))
        index = catalog(ROOT)
        self.assertLessEqual(sum(len(f['text'].encode()) for f in result['files'][:2]),
                             index['budgets']['startup_bytes'])

    def test_sources_are_scoped(self):
        import json
        result = bundle(ROOT, 'camera', sources=True)
        sources = json.loads(result['files'][-1]['text'])['repositories']
        self.assertEqual({p for r in sources for p in r['source_tree_paths']},
                         {'device/xiaomi/camera', 'vendor/xiaomi/camera'})

    def test_unknown_topic_does_not_become_path(self):
        with self.assertRaises(ValueError):
            bundle(ROOT, '../AGENTS.md')

    def test_reader_rejects_archive_and_external(self):
        for path in ['../AGENTS.md', 'https://example.com', 'archive/README.md']:
            with self.subTest(path=path), self.assertRaises(ValueError):
                read_record(ROOT, path)

    def test_symlink_cannot_escape_context_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'hub'; root.mkdir()
            outside = Path(tmp) / 'private'; outside.write_text('not context')
            try:
                (root / 'link').symlink_to(outside)
            except OSError:
                self.skipTest('symlinks unavailable')
            with self.assertRaises(ValueError):
                read_record(root, 'link')

    def test_section_retains_intro_nested_content_and_ignores_fences(self):
        text = '# Title\nScope: host-tested.\n## First\nA\n### Nested\nB\n```md\n## Fake\n```\n## Last\nC\n'
        self.assertEqual([x[2] for x in headings(text)], ['First', 'Nested', 'Last'])
        selected = select_section(text, 'first')
        self.assertIn('Scope: host-tested.', selected)
        self.assertIn('### Nested', selected)
        self.assertNotIn('## Last', selected)

    def test_unknown_or_ambiguous_section_is_rejected(self):
        for text, name in [('## A\n', 'missing'), ('## A\n## A\n', 'A')]:
            with self.assertRaises(ValueError):
                select_section(text, name)

    def test_section_leaves_startup_intact(self):
        full = bundle(ROOT, 'guidance', startup=True)
        section = headings(full['files'][-1]['text'])[0][2]
        selected = bundle(ROOT, 'guidance', startup=True, section=section)
        self.assertEqual(full['files'][:2], selected['files'][:2])
        self.assertLess(selected['bytes'], full['bytes'])

    def test_byte_limit_checks_utf8_and_never_truncates(self):
        result = bundle(ROOT, 'guidance')
        self.assertEqual(bundle(ROOT, 'guidance', max_bytes=result['bytes']), result)
        for limit in (0, -1, result['bytes'] - 1):
            with self.assertRaises(ValueError):
                bundle(ROOT, 'guidance', max_bytes=limit)

    def test_cli_limit_emits_no_partial_bundle(self):
        import subprocess
        import sys
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/context.py'),
                                 'guidance', '--max-bytes', '1', '--json'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, '')
        self.assertIn('no content was emitted', result.stderr)

    def test_all_topics_exist_and_fit_budget(self):
        index = catalog(ROOT)
        for topic in index['subsystems']:
            with self.subTest(topic=topic):
                result = bundle(ROOT, topic)
                self.assertLessEqual(result['bytes'], index['budgets']['topic_bytes'])


if __name__ == '__main__':
    unittest.main()
