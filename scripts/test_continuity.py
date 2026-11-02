"""Disposable Git fixtures for public imports and private checkpoint boundaries."""
from pathlib import Path
import subprocess
import tempfile
import unittest
from check_continuity import validate


class ContinuityTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / 'workhub'
        self.root.mkdir()
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        self.put('AGENTS.md', '# Shared rules\n')
        self.put('CLAUDE.md', '@AGENTS.md\n')
        self.put('.gitignore', '/.codex/tasks/\n')
        self.put('.agents/skills/resume/SKILL.md', '# Canonical skill\n')
        adapter = self.root / '.claude/skills/resume'
        adapter.parent.mkdir(parents=True)
        adapter.symlink_to('../../.agents/skills/resume', target_is_directory=True)

    def put(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')

    def test_private_untracked_record_is_allowed(self):
        self.put('.codex/tasks/one.md', 'Local context, never published\n')
        self.assertEqual(validate(self.root), [])

    def test_force_added_private_record_is_rejected(self):
        self.put('.codex/tasks/one.md', 'Local context\n')
        subprocess.run(['git', '-C', str(self.root), 'add', '-f',
                        '.codex/tasks/one.md'], check=True)
        self.assertIn('private task record is tracked in Git', validate(self.root))

    def test_missing_ignore_is_rejected(self):
        self.put('.gitignore', '')
        self.assertIn('private task-record directory is not ignored', validate(self.root))

    def test_missing_import_is_rejected(self):
        self.put('CLAUDE.md', '@missing.md\n')
        self.assertTrue(any('missing Claude import' in e for e in validate(self.root)))

    def test_import_cycle_is_rejected(self):
        self.put('AGENTS.md', '@CLAUDE.md\n')
        self.assertTrue(any('cycle' in e for e in validate(self.root)))

    def test_external_import_is_rejected(self):
        self.put('CLAUDE.md', '@../outside.md\n')
        self.assertIn('Claude import escapes workhub', validate(self.root))

    def test_inline_external_import_is_rejected(self):
        self.put('CLAUDE.md', '@AGENTS.md\nSee @../outside.md for guidance\n')
        self.assertIn('Claude import escapes workhub', validate(self.root))

    def test_bulleted_external_import_is_rejected(self):
        self.put('CLAUDE.md', '@AGENTS.md\n- instructions @../outside.md\n')
        self.assertIn('Claude import escapes workhub', validate(self.root))

    def test_import_literals_stay_inert(self):
        self.put('CLAUDE.md', '@AGENTS.md\n`@../inline.md`\n```\n@../fenced.md\n```\n@"../quoted.md"\n')
        self.assertEqual(validate(self.root), [])

    def test_escaped_space_import_is_loaded(self):
        self.put('docs/extra rules.md', '# Extra rules\n')
        self.put('CLAUDE.md', '@AGENTS.md\n- details @docs/extra\\ rules.md\n')
        self.assertEqual(validate(self.root), [])

    def test_windows_absolute_import_is_rejected_on_linux(self):
        self.put('CLAUDE.md', '@AGENTS.md\n@C:/outside.md\n')
        self.assertIn('Claude import must be a relative workhub path', validate(self.root))

    def test_shared_rules_must_be_imported(self):
        self.put('CLAUDE.md', '# Adapter without shared rules\n')
        self.assertIn('Claude entrypoint does not import shared AGENTS.md', validate(self.root))

    def test_broken_skill_adapter_is_rejected(self):
        (self.root / '.agents/skills/resume/SKILL.md').unlink()
        self.assertTrue(any('broken Claude skill adapter' in e for e in validate(self.root)))

    def test_external_skill_adapter_is_rejected(self):
        adapter = self.root / '.claude/skills/resume'
        adapter.unlink()
        adapter.symlink_to('../../../outside', target_is_directory=True)
        self.assertIn('Claude skill adapter escapes workhub', validate(self.root))
