#!/usr/bin/env python3
"""Check active knowledge and frozen provenance; no network or model calls."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import posixpath
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit
import yaml


class UniqueLoader(yaml.SafeLoader):
    """Do not silently discard a duplicated routing key."""


def mapping(loader, node, deep=False):
    result = {}
    for k, v in node.value:
        key = loader.construct_object(k, deep=deep)
        if not isinstance(key, str) or key in result:
            raise ValueError(f'non-string or duplicate YAML key: {key}')
        result[key] = loader.construct_object(v, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)


def load_yaml(text):
    return yaml.load(text, Loader=UniqueLoader)


def git_hash(kind, data):
    return hashlib.sha1(kind.encode() + b' ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def tree_hash(entries):
    names, chunks = set(), []
    for e in sorted(entries, key=lambda x: (x['path'] + ('/' if x['type'] == 'tree' else '')).encode()):
        name = e['path']
        if not isinstance(name, str) or not name or '/' in name or '\0' in name or name in names:
            raise ValueError('invalid or duplicate tree entry')
        names.add(name)
        if e['mode'] not in {'040000', '100644', '100755', '120000'}:
            raise ValueError('unsupported tree mode')
        if (e['mode'] == '040000') != (e['type'] == 'tree') or e['type'] not in {'blob', 'tree'}:
            raise ValueError('tree entry type/mode mismatch')
        if not re.fullmatch('[0-9a-f]{40}', e['sha']):
            raise ValueError('invalid object SHA')
        chunks.append(e['mode'].lstrip('0').encode() + b' ' + name.encode() + b'\0' + bytes.fromhex(e['sha']))
    return git_hash('tree', b''.join(chunks))


def disk_tree(path):
    """Hash symlink text, never follow archive symlinks outside the snapshot."""
    entries = []
    for p in path.iterdir():
        if p.is_symlink():
            mode, typ, sha = '120000', 'blob', git_hash('blob', os.fsencode(os.readlink(p)))
        elif p.is_dir():
            mode, typ, sha = '040000', 'tree', disk_tree(p)
        elif p.is_file():
            mode = '100755' if p.stat().st_mode & 0o111 else '100644'
            typ, sha = 'blob', git_hash('blob', p.read_bytes())
        else:
            raise ValueError(f'nonregular archive entry: {p.name}')
        entries.append(dict(path=p.name, mode=mode, type=typ, sha=sha))
    return tree_hash(entries)


def local_path(source, target):
    if not isinstance(target, str) or not target.strip():
        raise ValueError('empty or non-string path')
    parsed = urlsplit(target)
    if parsed.scheme in {'https', 'http', 'mailto'} or target.startswith('//'):
        return None, ''
    if parsed.scheme:
        raise ValueError('unsupported URL scheme')
    path = unquote(parsed.path)
    if path.startswith('/') or '\\' in path or '\0' in path:
        raise ValueError('unsafe repository path')
    path = posixpath.normpath(posixpath.join(posixpath.dirname(source), path)) if path else source
    if path in {'', '.', '..'} or path.startswith('../'):
        raise ValueError('path escapes repository or is empty')
    return path, unquote(parsed.fragment)


def prose(text):
    lines, fence = [], None
    for line in text.splitlines():
        m = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if m:
            run = m.group(1)
            if fence is None:
                fence = run
            elif run[0] == fence[0] and len(run) >= len(fence):
                fence = None
            continue
        if fence is None:
            lines.append(line)
    return re.sub(r'<!--.*?-->', '', '\n'.join(lines), flags=re.S)


def links(text):
    text = re.sub(r'(`+).*?\1', '', prose(text), flags=re.S)
    patterns = (r'\[[^\]\n]+\]\(\s*(?:<([^>\n]+)>|([^\s)]+))(?:\s+"[^"\n]*")?\s*\)',
                r'^ {0,3}\[[^\]\n]+\]:\s*(?:<([^>\n]+)>|(\S+))')
    for pattern in patterns:
        for m in re.finditer(pattern, text, re.M):
            yield m.group(1) or m.group(2)


def markdown_errors(text):
    """Check the simple Markdown subset used by active knowledge files."""
    errors = []
    if text.startswith('\ufeff') or '\x00' in text:
        errors.append('BOM or NUL in Markdown')
    fence = None
    for line in text.splitlines():
        match = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if not match:
            continue
        run, rest = match.groups()
        if fence is None:
            fence = run
        elif run[0] == fence[0] and len(run) >= len(fence) and not rest.strip():
            fence = None
    if fence:
        errors.append('unclosed fenced code block')
    return errors


def anchors(text):
    result, counts = set(), {}
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', prose(text), re.M):
        slug = re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-')
        n = counts.get(slug, 0)
        result.add(slug + (f'-{n}' if n else ''))
        counts[slug] = n + 1
    return result


def repository_errors(data):
    """Validate portable source identities without trusting them as installed state."""
    errors = []
    if not isinstance(data, dict) or data.get('schema_version') != 4:
        return ['source map requires schema_version 4']
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(data.get('observed', ''))):
        errors.append('source map requires an observation date')
    records = data.get('repositories')
    if not isinstance(records, list):
        return errors + ['source map requires repositories list']
    urls, paths = set(), set()
    for record in records:
        if not isinstance(record, dict):
            errors.append('invalid source record')
            continue
        url = record.get('repository', '')
        if not isinstance(url, str) or not url.startswith('https://') or url in urls:
            errors.append('invalid or duplicate repository URL')
        urls.add(str(url))
        refs = record.get('refs')
        if not isinstance(refs, dict) or record.get('selected_ref') not in refs:
            errors.append('selected source ref missing')
            continue
        for branch, sha in refs.items():
            if not isinstance(branch, str) or not branch or not re.fullmatch(r'[0-9a-f]{40}', str(sha)):
                errors.append('invalid branch or immutable source head')
        source_paths = record.get('source_tree_paths')
        if not isinstance(source_paths, list):
            errors.append('source_tree_paths must be a list')
            continue
        for path in source_paths:
            try:
                norm, frag = local_path('', path)
                if norm is None or frag or norm != path or path in paths:
                    raise ValueError('duplicate or unsafe source tree path')
                paths.add(path)
            except (ValueError, TypeError):
                errors.append('duplicate or unsafe source tree path')
        local = record.get('local_a17')
        if local is not None and local != 'matches_selected_ref':
            if not isinstance(local, dict) or not re.fullmatch(r'[0-9a-f]{40}', str(local.get('head', ''))):
                errors.append('invalid local source observation')
    return errors


def privacy_errors(text):
    """Bounded pattern scan; do not echo possible secrets in diagnostics."""
    checks = {
        'personal home path': r'(?:/home/[A-Za-z0-9_.-]+|[A-Za-z]:[\\/]Users[\\/][A-Za-z0-9_.-]+)',
        'private key': r'-----BEGIN (?:OPENSSH |RSA |EC |DSA )?PRIVATE KEY-----',
        'credential-shaped token': r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-(?:proj-)?[A-Za-z0-9_-]{24,})\b',
    }
    return [name for name, pattern in checks.items() if re.search(pattern, text)]


def validate(root: Path, inventory=None, extra=()):
    root = root.resolve()
    errors, refs = [], 0
    def fail(message):
        errors.append(message)
    def local_file(name):
        path, _ = local_path('', name)
        if path is None or not (root / path).resolve().is_relative_to(root):
            raise ValueError(f'unsafe local source: {name}')
        return root / path
    def read(name):
        return local_file(name).read_text(encoding='utf-8')
    try:
        idx = load_yaml(read('INDEX.yaml'))
        if not isinstance(idx, dict) or type(idx.get('schema_version')) is not int or idx['schema_version'] != 1:
            raise ValueError('INDEX.yaml requires schema_version 1')
        for field in ('entrypoints', 'read_order', 'subsystems', 'maintenance', 'legacy_routes', 'budgets'):
            if not isinstance(idx.get(field), dict):
                raise ValueError(f'INDEX.yaml requires {field} mapping')
        if idx['read_order'].get('normal') != ['AGENTS.md', 'CURRENT_STATE.md']:
            raise ValueError('normal startup must remain AGENTS.md + CURRENT_STATE.md')
        manifest = json.loads(read('archive/manifest.json'))
        sanitized = manifest.get('schema_version') == 2
        if sanitized:
            if manifest.get('status') != 'sanitized_public':
                raise ValueError('sanitized archive requires explicit status')
            if tree_hash(manifest['entries']) != manifest['archive_tree']:
                raise ValueError('sanitized archive manifest hash mismatch')
        else:
            if not re.fullmatch('[0-9a-f]{40}', manifest['source_commit']):
                raise ValueError('archive source commit must be immutable')
            if tree_hash(manifest['source_root_entries']) != manifest['source_tree']:
                raise ValueError('source-tree manifest hash mismatch')
            if tree_hash(manifest['source_root_entries'] + [manifest['added_notice']]) != manifest['archive_tree']:
                raise ValueError('archive-tree manifest hash mismatch')
        cold, _ = local_path('', manifest['archive_path'])
        if cold is None or not cold.startswith('archive/'):
            raise ValueError('snapshot must be inside archive/')
        known = set()
        if inventory is not None:
            if not isinstance(inventory, dict) or inventory.get('revision') != manifest.get('source_commit', manifest['archive_tree']):
                raise ValueError('inventory revision does not match source commit')
            paths = inventory.get('paths')
            if not isinstance(paths, list):
                raise ValueError('inventory.paths must be a list')
            for p in paths:
                norm, frag = local_path('', p)
                if norm is None or frag or not (norm == cold or norm.startswith(cold + '/')):
                    raise ValueError('inventory may establish frozen archive paths only')
                known.add(norm)
            if inventory.get('trees', {}).get(cold) != manifest['archive_tree']:
                raise ValueError('archive tree not verified by connector metadata')
            mode = 'connector archive metadata; original contents not read locally'
        else:
            if disk_tree(local_file(cold)) != manifest['archive_tree']:
                raise ValueError('frozen archive content/mode hash mismatch')
            mode = 'full filesystem archive hash'
        def check(source, target, route=False):
            nonlocal refs
            try:
                path, frag = local_path(source, target)
                if path is None:
                    if route:
                        raise ValueError('route must be local')
                    return
                refs += 1
                p = local_file(path)
                if not p.exists() and path not in known:
                    raise ValueError(f'missing target: {path}')
                if frag and path.endswith('.md') and not path.startswith(cold + '/'):
                    if frag not in anchors(read(path)):
                        raise ValueError(f'missing heading: {path}#{frag}')
            except (OSError, UnicodeError, ValueError) as exc:
                fail(f'{source}: {exc}')
        for field in ('entrypoints', 'legacy_routes'):
            for value in idx[field].values():
                check('INDEX.yaml', value, True)
        check('INDEX.yaml', idx['read_order'].get('optional_router'), True)
        for item in idx['read_order'].get('offload_or_write', []):
            check('INDEX.yaml', item, True)
        for name, record in idx['subsystems'].items():
            if not isinstance(record, dict) or not isinstance(record.get('status'), str):
                raise ValueError(f'invalid subsystem: {name}')
            check('INDEX.yaml', record.get('memory'), True)
            if 'heads' in record:
                check('INDEX.yaml', record['heads'], True)
        for record in idx['maintenance'].values():
            if not isinstance(record, dict):
                raise ValueError('invalid maintenance record')
            check('INDEX.yaml', record.get('memory'), True)
        expected_archive = dict(path=cold, policy='skip_by_default')
        if sanitized:
            expected_archive['archive_tree'] = manifest['archive_tree']
        else:
            expected_archive.update(source_commit=manifest['source_commit'], source_tree=manifest['source_tree'])
        if idx.get('cold_archives') != [expected_archive]:
            raise ValueError('cold archive route must match preservation manifest')
        md = {p.relative_to(root).as_posix() for p in root.glob('*.md')}
        for folder in ('memory', 'operations', 'state', 'references', 'templates', 'evidence'):
            md.update(p.relative_to(root).as_posix() for p in (root / folder).rglob('*.md'))
        md.update({'archive/README.md', 'archive/PRIVACY.md'})
        md.update(extra)
        paragraphs = {}
        for name in sorted(md):
            text = read(name)
            for issue in markdown_errors(text) + privacy_errors(text):
                fail(f'{name}: {issue}')
            for target in links(text):
                check(name, target)
            for para in re.split(r'\n\s*\n', prose(text)):
                normalized = ' '.join(para.split())
                if len(normalized) >= 240 and not normalized.startswith(('#', '|', '>')):
                    if normalized in paragraphs and paragraphs[normalized] != name:
                        fail(f'duplicate substantial paragraph: {paragraphs[normalized]} / {name}')
                    paragraphs[normalized] = name
            if name.startswith(('memory/', 'operations/', 'state/', 'references/')) and len(text.encode()) > idx['budgets']['topic_bytes']:
                fail(f'{name}: topic byte budget exceeded')
        startup = sum(len(read(p).encode()) for p in idx['read_order']['normal'])
        if startup > idx['budgets']['startup_bytes']:
            fail('startup byte budget exceeded')
        if len(read('AGENTS.md').encode()) > idx['budgets']['root_rules_bytes']:
            fail('root instruction byte budget exceeded')
        for p in root.rglob('*.yaml'):
            if not p.relative_to(root).as_posix().startswith('archive/'):
                load_yaml(p.read_text(encoding='utf-8'))
                for issue in privacy_errors(p.read_text(encoding='utf-8')):
                    fail(f'{p.relative_to(root)}: {issue}')
        if 'source_heads' in idx['entrypoints']:
            sources = load_yaml(read(idx['entrypoints']['source_heads']))
            for issue in repository_errors(sources):
                fail(issue)
            owned = {p for record in sources.get('repositories', [])
                     for p in record.get('source_tree_paths', [])}
            for name, record in idx['subsystems'].items():
                if any(p not in owned for p in record.get('source_paths', [])):
                    fail(f'{name}: unknown source-tree owner')
        if any((root / '.github/workflows').glob('*')):
            fail('hosted workflow present; this repository uses local checks')
        for name, expected in manifest.get('preserved_active_blobs', {}).items():
            if git_hash('blob', local_file(name).read_bytes()) != expected:
                fail(f'reused artifact changed: {name}')
        return errors, dict(references=refs, markdown_files=len(md), startup_bytes=startup, archive_mode=mode)
    except (OSError, UnicodeError, ValueError, TypeError, KeyError, yaml.YAMLError) as exc:
        fail(str(exc))
        return errors, dict(references=refs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', action='store_true', help='emit one JSON object for automation')
    parser.add_argument('files', nargs='*', help='additional repository-relative Markdown files')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--inventory', type=Path, help='verified connector archive metadata JSON')
    args = parser.parse_args()
    try:
        inv = json.loads(args.inventory.read_text(encoding='utf-8')) if args.inventory else None
        errors, stats = validate(args.root, inv, args.files)
    except (OSError, ValueError) as exc:
        errors, stats = [str(exc)], {}
    for error in errors:
        print('ERROR: ' + error, file=sys.stderr)
    if args.json:
        print(json.dumps(dict(ok=not errors, errors=errors, stats=stats), sort_keys=True))
    else:
        print(('FAIL: ' if errors else 'PASS: ') + json.dumps(stats, sort_keys=True))
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
