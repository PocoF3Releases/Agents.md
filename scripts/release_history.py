#!/usr/bin/env python3
"""Read-only source-history collection; never writes release prose or invokes builds."""
import argparse
import concurrent.futures
import hashlib
import json
import os
import tempfile
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET


def git(root, path, *args):
    return subprocess.check_output(["git", *args], cwd=root / path,
                                   text=True, stderr=subprocess.PIPE).strip()


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise ValueError(f"Refusing to overwrite {path}")
    path.write_text(json.dumps(data, indent=2) + "\n")


def snapshot(root, manifest, live=False, keep_ref=None):
    projects = ET.parse(manifest).getroot().findall("project")
    paths = [p.get("path", p.get("name")) for p in projects]
    if len(paths) != len(set(paths)):
        raise ValueError("Duplicate project paths")
    def read(p):
        path = p.get("path", p.get("name"))
        resolved = (root / path).resolve()
        if not resolved.is_relative_to(root.resolve()):
            raise ValueError(f"Project escapes checkout: {path}")
        revision = "HEAD" if live else p.get("revision", "")
        if not live and (len(revision) != 40 or any(c not in "0123456789abcdef" for c in revision)):
            raise ValueError(f"Manifest must be pinned: {path}")
        head = git(root, path, "rev-parse", revision + "^{commit}")
        tree = git(root, path, "rev-parse", head + "^{tree}")
        dirty = bool(git(root, path, "status", "--porcelain", "--untracked-files=normal")) if live else None
        if keep_ref:
            existing = subprocess.run(["git", "show-ref", "--verify", "--hash", keep_ref],
                                      cwd=root / path, text=True, capture_output=True)
            if existing.returncode == 0:
                if existing.stdout.strip() != head:
                    raise ValueError(f"Retention ref already names a different revision: {path}")
            else:
                git(root, path, "update-ref", keep_ref, head, "0" * 40)
        return dict(path=path, revision=head, tree=tree, dirty_worktree=dirty)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(read, projects))
    return dict(schema=1, kind="live-source-checkpoint" if live else "pinned-source-baseline",
                manifest_sha256=hashlib.sha256(manifest.read_bytes()).hexdigest(),
                artifact_inclusion="not-established", projects=records)


def compare(root, baseline, current):
    old = {p["path"]: p for p in baseline["projects"]}
    new = {p["path"]: p for p in current["projects"]}
    unchanged, identical, changed = [], [], []
    for path in sorted(old.keys() & new.keys()):
        before, after = old[path], new[path]
        if after.get("dirty_worktree") or after.get("tracked_edits"):
            raise ValueError(f"Uncommitted source input: {path}")
        if before["revision"] == after["revision"]:
            unchanged.append(path)
            continue
        if before["tree"] == after["tree"]:
            identical.append(path)
            continue
        a, b = before["revision"], after["revision"]
        net_paths = set(git(root, path, "diff", "--name-only", a, b).splitlines())
        if net_paths <= {".lfsconfig", ".gitattributes"}:
            changed.append(dict(path=path, before=a, after=b, candidates=[],
                                baseline_contains_patch=[], net_neutral_commits=[],
                                classification="repository-storage-metadata-only",
                                net_stat=git(root, path, "diff", "--stat", a, b)))
            continue
        # Symmetric cherry comparison removes equal stable patch IDs even after rebase.
        raw = git(root, path, "log", "--cherry-pick", "--right-only", "--no-merges",
                  "--format=%H", a + "..." + b)
        candidates = []
        net_neutral = []
        already_present = []
        with tempfile.TemporaryDirectory(prefix="release-history-index-") as temp:
            env = dict(os.environ, GIT_INDEX_FILE=str(Path(temp) / "index"))
            subprocess.run(["git", "read-tree", a], cwd=root / path, env=env,
                           check=True, capture_output=True)
            for commit in raw.splitlines():
                patch = subprocess.check_output(
                    ["git", "show", "--format=", "--binary", "--no-ext-diff", commit],
                    cwd=root / path)
                present = subprocess.run(
                    ["git", "apply", "--cached", "--reverse", "--check"],
                    input=patch, cwd=root / path, env=env, capture_output=True)
                if patch and present.returncode == 0:
                    already_present.append(commit)
        for commit in raw.splitlines():
            if commit in already_present:
                continue
            # Metadata-only/empty commits do not add source behavior.
            touched = set(git(root, path, "diff-tree", "--no-commit-id", "--name-only", "-r", commit).splitlines())
            if not touched or not (touched & net_paths):
                net_neutral.append(commit)
                continue
            candidates.append(dict(commit=commit,
                                   subject=git(root, path, "show", "-s", "--format=%s", commit)))
        changed.append(dict(path=path, before=a, after=b,
                            net_stat=git(root, path, "diff", "--stat", a, b),
                            candidates=candidates, baseline_contains_patch=already_present,
                            net_neutral_commits=net_neutral,
                            review="Review final net diff, reversions, adapted/squashed equivalents and announced topics; not release-ready prose"))
    return dict(schema=1, status="history-evidence-only", artifact_inclusion="not-established",
                identical_commit_count=len(unchanged), identical_tree_paths=identical,
                added_paths=sorted(new.keys() - old.keys()),
                removed_paths=sorted(old.keys() - new.keys()), changed=changed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    snap = sub.add_parser("snapshot")
    snap.add_argument("--manifest", type=Path, required=True)
    snap.add_argument("--live", action="store_true")
    snap.add_argument("--keep-ref", help="Optional local retention ref; never a branch or tag")
    diff = sub.add_parser("compare")
    diff.add_argument("--baseline", type=Path, required=True)
    diff.add_argument("--current", type=Path, required=True)
    for cmd in (snap, diff):
        cmd.add_argument("--root", type=Path, required=True)
        cmd.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Output already exists; use a new checkpoint filename")
    if args.command == "snapshot":
        if args.keep_ref and not args.keep_ref.startswith("refs/changelog/"):
            parser.error("Retention refs must be under refs/changelog/")
        result = snapshot(args.root, args.manifest, args.live, args.keep_ref)
    else:
        result = compare(args.root, json.loads(args.baseline.read_text()),
                         json.loads(args.current.read_text()))
    save(args.output, result)
    print("Saved history evidence; no changelog generated.")


if __name__ == "__main__":
    main()
