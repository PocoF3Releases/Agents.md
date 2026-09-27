"""Isolated fixtures; no repository mutation, network or device access."""
import json
import os
import tempfile
import unittest
from pathlib import Path
import yaml
from validate_knowledge import anchors, disk_tree, git_hash, links, load_yaml, local_path, tree_hash, validate


class KnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'repo'
        self.root.mkdir()
        self.put('AGENTS.md', '# Rules\n')
        self.put('CURRENT_STATE.md', '# State\n[Topic](memory/topic.md)\n')
        self.put('memory/topic.md', '# Topic\n## V-ONE\nTest scope.\n')
        self.put('archive/README.md', '# Archive\n')
        self.put('archive/snapshot/old.txt', 'preserved\n')
        original = [dict(path='old.txt', mode='100644', type='blob', sha=git_hash('blob', b'preserved\n'))]
        self.put('archive/snapshot/AGENTS.override.md', '# Historical\n')
        notice = dict(path='AGENTS.override.md', mode='100644', type='blob', sha=git_hash('blob', b'# Historical\n'))
        self.manifest = dict(source_commit='a'*40, source_tree=tree_hash(original), source_root_entries=original,
                             archive_path='archive/snapshot', archive_tree=tree_hash(original+[notice]), added_notice=notice)
        self.put('archive/manifest.json', json.dumps(self.manifest))
        self.index = dict(schema_version=1, entrypoints={'rules':'AGENTS.md'},
          read_order=dict(normal=['AGENTS.md','CURRENT_STATE.md'],optional_router='INDEX.yaml'),
          subsystems={'topic':dict(status='durable',memory='memory/topic.md')},maintenance={},legacy_routes={},
          cold_archives=[dict(path='archive/snapshot',policy='skip_by_default',source_commit='a'*40,source_tree=self.manifest['source_tree'])],
          budgets=dict(startup_bytes=5000,root_rules_bytes=3000,topic_bytes=10000))
        self.save_index()
        self.inventory=dict(revision='a'*40,paths=['archive/snapshot','archive/snapshot/old.txt'],trees={'archive/snapshot':self.manifest['archive_tree']})

    def put(self,name,text):
        p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')

    def save_index(self):
        self.put('INDEX.yaml',yaml.safe_dump(self.index))

    def errors(self,metadata=False):
        return validate(self.root,self.inventory if metadata else None)[0]

    def make_sanitized(self):
        self.manifest = dict(schema_version=2, status='sanitized_public',
            archive_path='archive/snapshot',
            entries=self.manifest['source_root_entries'] + [self.manifest['added_notice']],
            archive_tree=self.manifest['archive_tree'])
        self.put('archive/manifest.json', json.dumps(self.manifest))
        self.index['cold_archives'] = [dict(path='archive/snapshot', policy='skip_by_default',
            archive_tree=self.manifest['archive_tree'])]
        self.save_index()

    def test_sanitized_archive(self):
        self.make_sanitized()
        self.assertEqual(self.errors(), [])

    def test_sanitized_tampering(self):
        self.make_sanitized()
        self.put('archive/snapshot/old.txt', 'unexpected change')
        self.assertTrue(self.errors())

    def test_sanitized_status_required(self):
        self.make_sanitized()
        self.manifest['status'] = 'original'
        self.put('archive/manifest.json', json.dumps(self.manifest))
        self.assertTrue(self.errors())

    def test_valid_full_archive(self):
        self.assertEqual(self.errors(),[])

    def test_valid_metadata(self):
        (self.root/'archive/snapshot/old.txt').unlink()
        self.assertEqual(self.errors(True),[])

    def test_modified_archive_detected(self):
        self.put('archive/snapshot/old.txt','changed\n')
        self.assertTrue(any('archive content' in x for x in self.errors()))

    def test_missing_archive_detected(self):
        (self.root/'archive/snapshot/old.txt').unlink()
        self.assertTrue(self.errors())

    def test_manifest_tampering(self):
        self.manifest['source_root_entries'][0]['sha']='b'*40
        self.put('archive/manifest.json',json.dumps(self.manifest))
        self.assertTrue(any('manifest hash' in x for x in self.errors()))

    def test_wrong_metadata_tree(self):
        self.inventory['trees']['archive/snapshot']='b'*40
        self.assertTrue(self.errors(True))

    def test_wrong_metadata_revision(self):
        self.inventory['revision']='main'
        self.assertTrue(self.errors(True))

    def test_inventory_cannot_hide_missing_active_file(self):
        (self.root/'memory/topic.md').unlink()
        self.inventory['paths'].append('memory/topic.md')
        self.assertTrue(self.errors(True))

    def test_missing_link(self):
        self.put('memory/topic.md','[bad](absent.md)\n')
        self.assertTrue(any('missing target' in x for x in self.errors()))

    def test_missing_heading(self):
        self.put('README.md','[bad](memory/topic.md#v-missing)\n')
        self.assertTrue(any('missing heading' in x for x in self.errors()))

    def test_valid_validation_heading(self):
        self.put('README.md','[evidence](memory/topic.md#v-one)\n')
        self.assertEqual(self.errors(),[])

    def test_duplicate_yaml_keys(self):
        with self.assertRaises(ValueError):
            load_yaml('a: 1\na: 2\n')

    def test_wrong_schema(self):
        self.index['schema_version']=True;self.save_index()
        self.assertTrue(self.errors())

    def test_old_mandatory_startup_rejected(self):
        self.index['read_order']['normal'].append('INDEX.yaml');self.save_index()
        self.assertTrue(self.errors())

    def test_missing_route(self):
        self.index['subsystems']['topic']['memory']='absent.md';self.save_index()
        self.assertTrue(self.errors())

    def test_external_route_rejected(self):
        self.index['entrypoints']['rules']='https://example.com';self.save_index()
        self.assertTrue(self.errors())

    def test_unsafe_paths(self):
        for value in ('../x','%2e%2e/x','/etc/passwd','C:\\x','file:///tmp/x'):
            with self.subTest(value=value),self.assertRaises(ValueError):local_path('README.md',value)

    def test_external_links_ignored(self):
        for value in ('https://example.com','http://example.com','mailto:maintainer@example.com'):
            self.assertEqual(local_path('README.md',value),(None,''))

    def test_fenced_and_inline_code_excluded(self):
        text='```md\n[x](no.md)\n```\n`[x](no.md)`\n[y](yes.md)'
        self.assertEqual(list(links(text)),['yes.md'])

    def test_reference_link_and_tilde_fence(self):
        self.assertEqual(list(links('~~~\n[x](no.md)\n~~~\n[ref]: <yes.md>')),['yes.md'])

    def test_active_symlink_escape(self):
        outside=self.root.parent/'outside.md';outside.write_text('# Outside')
        try:(self.root/'memory/escape.md').symlink_to(outside)
        except OSError:self.skipTest('symlinks unavailable')
        self.assertTrue(any('unsafe' in x for x in self.errors()))

    def test_archive_symlink_hashes_link_not_target(self):
        p=self.root/'archive/snapshot/link'
        try:p.symlink_to('/nonexistent/unreadable')
        except OSError:self.skipTest('symlinks unavailable')
        self.assertRegex(disk_tree(p.parent),r'^[0-9a-f]{40}$')

    def test_utf8_budget(self):
        self.put('AGENTS.md','é'*1600)
        self.assertTrue(any('instruction byte' in x for x in self.errors()))

    def test_topic_budget(self):
        self.put('memory/topic.md','x'*10001)
        self.assertTrue(any('topic byte' in x for x in self.errors()))

    def test_duplicate_substantial_paragraph(self):
        para='A distinctive factual sentence. '*12
        self.put('memory/one.md',para);self.put('memory/two.md',para)
        self.assertTrue(any('duplicate substantial' in x for x in self.errors()))

    def test_git_empty_tree(self):
        self.assertEqual(tree_hash([]),'4b825dc642cb6eb9a060e54bf8d69288fbee4904')

    def test_duplicate_tree_entry_rejected(self):
        e=self.manifest['source_root_entries'][0]
        with self.assertRaises(ValueError):tree_hash([e,e])

    def test_source_commit_must_be_pinned(self):
        self.manifest['source_commit']='main';self.put('archive/manifest.json',json.dumps(self.manifest))
        self.assertTrue(any('immutable' in x for x in self.errors()))

    def test_duplicate_heading_suffix(self):
        self.assertEqual(anchors('# Test\n## Test\n'),{'test','test-1'})

    def test_extra_markdown_checked(self):
        self.put('extra/info.md','[bad](missing.md)\n')
        self.assertTrue(validate(self.root,None,('extra/info.md',))[0])

if __name__=='__main__':unittest.main()
