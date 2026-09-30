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


def bundle(root, topic, startup=False, sources=False):
    index = catalog(root)
    if topic not in index['subsystems']:
        raise ValueError(f'unknown topic: {topic}; use --list or --search')
    record = index['subsystems'][topic]
    paths = (index['read_order']['normal'] if startup else []) + [record['memory']]
    files = [{'path': p, 'text': read_record(root, p)} for p in dict.fromkeys(paths)]
    if sources:
        data = load_yaml(read_record(root, index['entrypoints']['source_heads']))
        wanted = set(record.get('source_paths', []))
        selected = [r for r in data['repositories'] if wanted.intersection(r['source_tree_paths'])]
        files.append({'path': index['entrypoints']['source_heads'] + ' (selected)',
                      'text': json.dumps({'observed': data['observed'], 'scope': data['scope'],
                                          'repositories': selected}, indent=2) + '\n'})
    return {'topic': topic, 'bytes': sum(len(x['text'].encode('utf-8')) for x in files),
            'files': files}


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
    args = parser.parse_args()
    if args.topic and (args.list or args.search is not None):
        parser.error('select a topic or a discovery action, not both')
    try:
        if args.topic:
            result = bundle(args.root, args.topic, args.startup, args.sources)
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
