"""Representative cold-start retrieval and containment checks; no remote calls."""
import tempfile
import unittest
from pathlib import Path
from context import bundle, catalog, read_record, search_topics

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

    def test_all_topics_exist_and_fit_budget(self):
        index = catalog(ROOT)
        for topic in index['subsystems']:
            with self.subTest(topic=topic):
                result = bundle(ROOT, topic)
                self.assertLessEqual(result['bytes'], index['budgets']['topic_bytes'])


if __name__ == '__main__':
    unittest.main()
