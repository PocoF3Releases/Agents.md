#!/usr/bin/env python3
"""Validate routed knowledge, without fetching archives or contacting the network."""
from __future__ import annotations

import argparse
import json
import posixpath
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

GOVERNANCE = (
    'AGENTS.md', 'START_HERE.md', 'README.md', 'OFFLOAD_PROTOCOL.md',
    'memory/agent-memory-workflow.md', 'memory/git-history-conventions.md',
    'templates/chat-offload-template.md',
)
PATH_KEYS = {'memory', 'primary_today', 'related_today', 'preparation_today',
             'semantic_delta_index', 'heads', 'tracked_heads', 'index'}
AGENTS_BUDGET = 8 * 1024  # Project policy, not OpenAI's combined instruction limit.


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate mapping keys rather than silently losing a route."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise ValueError('INDEX.yaml mapping keys must be strings')
        if key in result:
            raise ValueError(f'duplicate YAML key: {key}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                             unique_mapping)


def load_index(text: str) -> dict:
    data = yaml.load(text, Loader=UniqueLoader)
    if not isinstance(data, dict) or type(data.get('schema_version')) is not int:
        raise ValueError('INDEX.yaml requires an integer schema_version')
    if data['schema_version'] != 1:
        raise ValueError('unsupported INDEX.yaml schema_version')
    for key in ('entrypoints', 'subsystems', 'read_order', 'maintenance'):
        if not isinstance(data.get(key), dict):
            raise ValueError(f'INDEX.yaml requires a {key} mapping')
    if not data['entrypoints'] or not data['subsystems']:
        raise ValueError('entrypoints and subsystems must not be empty')
    normal = data['read_order'].get('normal')
    if not isinstance(normal, list) or not all(isinstance(p, str) for p in normal):
        raise ValueError('read_order.normal must be a list of strings')
    if 'INDEX.yaml' in normal:
        raise ValueError('INDEX.yaml is optional; do not require it in normal reads')
    for name, record in data['subsystems'].items():
        if not isinstance(record, dict) or not isinstance(record.get('status'), str):
            raise ValueError(f'subsystem {name} requires a status string')
        if not isinstance(record.get('memory'), str):
            raise ValueError(f'subsystem {name} requires a memory path')
    return data


def index_paths(data: dict):
    """Only path-bearing schema fields; repository_roles are NOT local paths."""
    yield from data['entrypoints'].values()
    for field in ('normal', 'offload_or_write'):
        values = data['read_order'].get(field, [])
        if not isinstance(values, list):
            raise ValueError(f'read_order.{field} must be a list')
        for value in values:
            if not isinstance(value, str):
                raise ValueError(f'read_order.{field} entries must be strings')
            if value.endswith(('.md', '.yaml', '.json')):
                yield value
    if 'optional_router' in data['read_order']:
        yield data['read_order']['optional_router']
    archives = data.get('cold_archives', [])
    if not isinstance(archives, list):
        raise ValueError('cold_archives must be a list')
    for record in archives:
        if not isinstance(record, dict) or 'path' not in record:
            raise ValueError('each cold archive requires a path')
        yield record['path']
    records = list(data['subsystems'].values()) + list(data['maintenance'].values())
    for record in records:
        if not isinstance(record, dict):
            raise ValueError('maintenance records must be mappings')
        for key, value in record.items():
            if key in PATH_KEYS:
                yield from value if isinstance(value, list) else [value]


def local_target(source: str, target: str) -> str | None:
    if not isinstance(target, str) or not target.strip():
        raise ValueError('empty or non-string path')
    parsed = urlsplit(target)
    if parsed.scheme in {'https', 'http', 'mailto'} or target.startswith('//'):
        return None
    if parsed.scheme:
        raise ValueError(f'unsupported link scheme: {target}')
    path = unquote(parsed.path)
    if not path:
        return None  # Anchor-only link; anchor existence is outside this checker.
    if path.startswith('/') or '\\' in path or '\x00' in path:
        raise ValueError(f'unsafe repository path: {target}')
    result = posixpath.normpath(posixpath.join(posixpath.dirname(source), path))
    if result == '..' or result.startswith('../'):
        raise ValueError(f'path escapes repository: {target}')
    return result


def markdown_targets(text: str):
    """Extract ordinary inline links/reference definitions, excluding code."""
    lines, fence = [], None
    for line in text.splitlines():
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if marker:
            run = marker.group(1)
            if fence is None:
                fence = run
            elif run[0] == fence[0] and len(run) >= len(fence):
                fence = None
            continue
        if fence is None:
            lines.append(line)
    prose = '\n'.join(lines)
    prose = re.sub(r'<!--.*?-->', '', prose, flags=re.S)
    prose = re.sub(r'(`+).*?\1', '', prose, flags=re.S)
    inline = r'\[[^\]\n]+\]\(\s*(?:<([^>\n]+)>|([^\s)]+))(?:\s+"[^"\n]*")?\s*\)'
    reference = r'^ {0,3}\[[^\]\n]+\]:\s*(?:<([^>\n]+)>|(\S+))'
    for pattern in (inline, reference):
        for match in re.finditer(pattern, prose, flags=re.M):
            yield match.group(1) or match.group(2)


def validate(root: Path, extra: tuple[str, ...] = (),
             inventory: set[str] | None = None) -> tuple[list[str], int]:
    root = root.resolve()
    errors, count = [], 0

    def check(source: str, target: str, require_local=False):
        nonlocal count
        try:
            path = local_target(source, target)
            if path is None:
                if require_local:
                    raise ValueError('index routes must be repository-local paths')
                return
            count += 1
            resolved = (root / path).resolve()
            if not resolved.is_relative_to(root):
                raise ValueError(f'symlink escapes repository: {path}')
            exists = path in inventory if inventory is not None else resolved.exists()
            if not exists:
                raise ValueError(f'missing target: {path}')
        except (ValueError, OSError) as exc:
            errors.append(f'{source}: {exc}')

    try:
        data = load_index((root / 'INDEX.yaml').read_text(encoding='utf-8'))
        for path in index_paths(data):
            check('INDEX.yaml', path, require_local=True)
    except (OSError, UnicodeError, ValueError, yaml.YAMLError) as exc:
        errors.append(f'INDEX.yaml: {exc}')
    for source in dict.fromkeys((*GOVERNANCE, *extra)):
        try:
            safe = local_target('', source)
            if safe is None or not (root / safe).resolve().is_relative_to(root):
                raise ValueError('source must be inside the repository')
            text = (root / safe).read_text(encoding='utf-8')
            if safe == 'AGENTS.md' and len(text.encode('utf-8')) > AGENTS_BUDGET:
                errors.append('AGENTS.md: exceeds the project 8 KiB budget')
            for target in markdown_targets(text):
                check(safe, target)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f'{source}: {exc}')
    return errors, count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='*', help='additional repository-relative Markdown files')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--inventory', type=Path, help='connector snapshot JSON: revision, paths')
    args = parser.parse_args()
    inventory, mode = None, 'filesystem'
    try:
        if args.inventory:
            data = json.loads(args.inventory.read_text(encoding='utf-8'))
            if not isinstance(data, dict) or not re.fullmatch(r'[0-9a-f]{40}', str(data.get('revision', ''))):
                raise ValueError('inventory requires an immutable 40-hex revision')
            paths = data.get('paths')
            if not isinstance(paths, list) or not all(isinstance(p, str) for p in paths):
                raise ValueError('inventory.paths must be a list of repository paths')
            inventory = set()
            for path in paths:
                normalized = local_target('', path)
                if normalized is None:
                    raise ValueError('inventory paths must be local')
                inventory.add(normalized)
            candidates = data.get('candidate_paths', [])
            if not isinstance(candidates, list):
                raise ValueError('inventory.candidate_paths must be a list')
            for candidate in candidates:
                normalized = local_target('', candidate)
                if normalized is None:
                    raise ValueError('candidate paths must be local')
                local = (args.root / normalized).resolve()
                if not local.is_relative_to(args.root.resolve()) or not local.is_file():
                    raise ValueError(f'candidate file is unavailable: {candidate}')
                inventory.add(normalized)
            mode = (f"connector metadata at {data['revision']} + {len(candidates)} candidate files "
                    '(unchanged target contents not audited)')
        errors, count = validate(args.root, tuple(args.files), inventory)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1
    for error in errors:
        print(f'ERROR: {error}', file=sys.stderr)
    print(f'{"FAIL" if errors else "PASS"}: {count} local references; {mode}')
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
