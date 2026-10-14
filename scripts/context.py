#!/usr/bin/env python3
"""Retrieve one workhub topic; no archive scan, network, model or device calls."""
from __future__ import annotations
import argparse
import json
import re
import sys
import yaml
from pathlib import Path
from validate_knowledge import load_yaml, local_path


def read_record(root, name):
    path, fragment = local_path('', name)
    if path is None or fragment:
        raise ValueError('expected a repository-relative file')
    file = (root / path).resolve()
    if not file.is_relative_to(root.resolve()) or path.startswith('archive/'):
        raise ValueError('context reads must remain in active knowledge')
    return file.read_text(encoding='utf-8')


def catalog(root):
    return load_yaml(read_record(root, 'INDEX.yaml'))


def search_topics(index, query):
    terms = set(re.findall(r'[\w-]+', query.casefold()))
    results = []
    for key, record in index['subsystems'].items():
        words = set(re.findall(r'[\w-]+', ' '.join(
            [key, record.get('title', ''), *record.get('keywords', [])]).casefold()))
        score = len(terms & words)
        if score:
            results.append((score, key, record))
    return [(key, record) for _, key, record in sorted(results, key=lambda x: (-x[0], x[1]))]


def headings(text):
    """Return navigable headings, ignoring fenced examples."""
    rows = []
    fence = None
    offset = 0
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
        elif fence is None:
            match = re.match(r"^(#{2,6}) +(.+?) *#*\s*$", line)
            if match:
                rows.append((offset, len(match.group(1)), match.group(2)))
        offset += len(line)
    return rows


def select_section(text, name):
    rows = headings(text)
    matches = [row for row in rows if row[2].casefold() == name.casefold()]
    if len(matches) != 1:
        raise ValueError('section must match one heading; use --list-sections')
    start, level, _ = matches[0]
    end = next((offset for offset, depth, _ in rows
                if offset > start and depth <= level), len(text))
    # Keep the title/intro so an excerpt retains scope and evidence qualifications.
    return text[:rows[0][0]] + text[start:end]


def bundle(root, topic, startup=False, sources=False, section=None, max_bytes=None):
    index = catalog(root)
    if topic not in index['subsystems']:
        raise ValueError(f'unknown topic: {topic}; use --list or --search')
    record = index['subsystems'][topic]
    paths = (index['read_order']['normal'] if startup else []) + [record['memory']]
    files = [{'path': p, 'text': read_record(root, p)} for p in dict.fromkeys(paths)]
    if section is not None:
        files[-1]['text'] = select_section(files[-1]['text'], section)
        files[-1]['section'] = section
    if sources:
        data = load_yaml(read_record(root, index['entrypoints']['source_heads']))
        wanted = set(record.get('source_paths', []))
        selected = [r for r in data['repositories'] if wanted.intersection(r['source_tree_paths'])]
        files.append({'path': index['entrypoints']['source_heads'] + ' (selected)',
                      'text': json.dumps({'observed': data['observed'], 'scope': data['scope'],
                                          'repositories': selected}, indent=2) + '\n'})
    size = sum(len(x['text'].encode('utf-8')) for x in files)
    if max_bytes is not None and (max_bytes <= 0 or size > max_bytes):
        raise ValueError(f'context is {size} bytes; limit is {max_bytes}. '
                         'Choose a narrower --section or raise the limit; no content was emitted.')
    return {'topic': topic, 'bytes': size, 'files': files}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('topic', nargs='?')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    action = parser.add_mutually_exclusive_group()
    action.add_argument('--list', action='store_true')
    action.add_argument('--search')
    parser.add_argument('--startup', action='store_true', help='include the two startup files')
    parser.add_argument('--sources', action='store_true', help='include only this topic source owners')
    parser.add_argument('--json', action='store_true', help='one JSON object; no wrapper text')
    parser.add_argument('--section', help='retrieve one exact heading with its intro and nested sections')
    parser.add_argument('--list-sections', action='store_true', help='list topic headings without document text')
    parser.add_argument('--max-bytes', type=int, help='reject oversized content without silently truncating it')
    args = parser.parse_args()
    if args.topic and (args.list or args.search is not None):
        parser.error('select a topic or a discovery action, not both')
    if (args.section or args.list_sections or args.max_bytes is not None) and not args.topic:
        parser.error('section and size options require a topic')
    if args.list_sections and (args.section or args.startup or args.sources or args.max_bytes is not None):
        parser.error('--list-sections cannot be combined with bundle options')
    try:
        if args.topic and args.list_sections:
            result = bundle(args.root, args.topic)
            names = [row[2] for row in headings(result['files'][0]['text'])]
            print(json.dumps({'topic': args.topic, 'sections': names}, ensure_ascii=False)
                  if args.json else '\n'.join(names))
        elif args.topic:
            result = bundle(args.root, args.topic, args.startup, args.sources, args.section, args.max_bytes)
            if args.json:
                print(json.dumps(result, ensure_ascii=False))
            else:
                for item in result['files']:
                    print('--- ' + item['path'] + ' ---\n' + item['text'])
        else:
            index = catalog(args.root)
            rows = search_topics(index, args.search) if args.search is not None else index['subsystems'].items()
            result = [{'topic': k, 'title': v.get('title', k), 'path': v['memory']} for k, v in rows]
            if args.json:
                print(json.dumps({'topics': result}, ensure_ascii=False))
            else:
                for item in result:
                    print(f"{item['topic']}: {item['title']} ({item['path']})")
        return 0
    except (OSError, UnicodeError, ValueError, KeyError, TypeError, yaml.YAMLError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
