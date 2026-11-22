#!/usr/bin/env python3
"""Check public instruction imports and keep private task records out of Git."""
from pathlib import Path, PureWindowsPath
import re
import subprocess
import sys
from validate_knowledge import prose


def validate(root):
    root = Path(root).resolve()
    errors = []
    loaded = set()

    def contained(path):
        return path.resolve().is_relative_to(root)

    def imports(path, ancestors=()):
        if not contained(path):
            errors.append('Claude import escapes workhub')
            return
        if not path.is_file():
            errors.append(f'missing Claude import: {path.relative_to(root)}')
            return
        if path in ancestors or len(ancestors) >= 5:
            errors.append('Claude import cycle or excessive depth')
            return
        loaded.add(path)
        text = re.sub(r'(`+).*?\1', '', prose(path.read_text(encoding='utf-8')),
                      flags=re.S)
        # Public workhub imports use relative paths, with escaped spaces allowed.
        # Scan prose/bullets too; quoted paths and Markdown code stay literal.
        for match in re.finditer(r'''(?<!["'])@((?:\\ |[^\s"'`])+)''', text):
            target = match.group(1).replace('\\ ', ' ')
            if ('\\' in target or Path(target).is_absolute()
                    or PureWindowsPath(target).drive):
                errors.append('Claude import must be a relative workhub path')
                continue
            imports((path.parent / target).resolve(), ancestors + (path,))

    imports(root / 'CLAUDE.md')
    if root / 'AGENTS.md' not in loaded:
        errors.append('Claude entrypoint does not import shared AGENTS.md')
    for adapter in sorted((root / '.claude/skills').glob('*')):
        if adapter.is_symlink():
            if not contained(adapter):
                errors.append('Claude skill adapter escapes workhub')
            elif not (adapter / 'SKILL.md').is_file():
                errors.append(f'broken Claude skill adapter: {adapter.name}')

    indexed = subprocess.run(['git', '-C', str(root), 'ls-files', '-z', '--',
                              '.codex/tasks/'], capture_output=True)
    if indexed.returncode:
        errors.append('could not inspect Git index for private task records')
    elif indexed.stdout:
        errors.append('private task record is tracked in Git')
    ignored = subprocess.run(['git', '-C', str(root), 'check-ignore', '--no-index',
                              '-q', '.codex/tasks/continuity-probe.md'],
                             capture_output=True)
    if ignored.returncode:
        errors.append('private task-record directory is not ignored')
    return errors


if __name__ == '__main__':
    errors = validate(Path(__file__).resolve().parents[1])
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        raise SystemExit(1)
    print('Public continuity imports, skill links and task-record boundary passed')
