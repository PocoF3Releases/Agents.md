#!/usr/bin/env python3
"""Report how far each maintained fork is behind its upstream base.

Reads the source ledger (state/repositories.yaml) and the unmodified Evolution X
manifest in ANDROID_ROOT/.repo/manifests (local_manifests are ignored, so each
path resolves to the project our fork replaces). Paths outside that manifest use
STANDALONE below. For each fork it fetches the upstream branch into the
checkout as refs/remotes/upstream-check/<branch> (no working-tree change) and
prints: commits upstream has that the fork lacks, the fork's own commits, and
the upstream branch that currently contains the fork base.

  scripts/check_fork_bases.py [--android-root ~/evo] [--only PATH ...]
Exit status 1 when any fork is behind. Rebase with scripts/rebase_fork.py.
"""
import argparse
import os
import subprocess
import sys
import xml.etree.ElementTree as ET

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
GH = "https://github.com/"
# Upstreams for forks that the Evolution X manifest does not carry.
# Older branches are listed only to identify where an un-rebased fork sits.
STANDALONE = {
    "kernel/xiaomi/sm8250": (GH + "LineageOS/android_kernel_qcom_sm8250", ["lineage-20"]),
    "device/xiaomi/alioth": (GH + "LineageOS/android_device_xiaomi_alioth", ["lineage-24.0", "lineage-23.2"]),
    "device/xiaomi/sm8250-common": (GH + "LineageOS/android_device_xiaomi_sm8250-common", ["lineage-24.0", "lineage-23.2"]),
    "hardware/xiaomi": (GH + "LineageOS/android_hardware_xiaomi", ["lineage-24.0", "lineage-23.2"]),
    "vendor/xiaomi/alioth": (GH + "TheMuppets/proprietary_vendor_xiaomi_alioth", ["lineage-24.0", "lineage-23.2"]),
    "vendor/xiaomi/sm8250-common": (GH + "TheMuppets/proprietary_vendor_xiaomi_sm8250-common", ["lineage-24.0", "lineage-23.2"]),
}
NO_UPSTREAM = {"device/xiaomi/camera", "vendor/xiaomi/camera", ".repo/local_manifests"}


def git(repo, *args, check=True):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    if check and r.returncode:
        raise RuntimeError(r.stderr.strip() or f"git {' '.join(args)} failed")
    return r.stdout.strip()


def manifest_projects(root):
    mdir = os.path.join(root, ".repo", "manifests")
    base = git(mdir, "remote", "get-url", "origin").rsplit("/", 1)[0] + "/"
    remotes, default, projects = {}, {}, {}

    def load(name):
        for el in ET.parse(os.path.join(mdir, name)).getroot():
            if el.tag == "include":
                load(el.get("name"))
            elif el.tag == "remote":
                fetch = el.get("fetch")
                if fetch.startswith(".."):
                    fetch = base.rsplit("/", 2)[0] + "/" + fetch[2:].lstrip("/")
                remotes[el.get("name")] = (fetch.rstrip("/"), el.get("revision"))
            elif el.tag == "default":
                default.update(el.attrib)
            elif el.tag == "project":
                projects[el.get("path") or el.get("name")] = el.attrib
    load("default.xml")
    out = {}
    for path, p in projects.items():
        fetch, rrev = remotes[p.get("remote", default.get("remote"))]
        rev = p.get("revision") or rrev or default.get("revision")
        rev = rev[len("refs/heads/"):] if rev.startswith("refs/heads/") else rev
        out[path] = (f"{fetch}/{p['name']}", [rev])
    return out


def check(root, path, url, branches, fork_tip):
    repo = os.path.join(root, path)
    res = {}
    for b in branches:
        src = b if b.startswith("refs/") else f"refs/heads/{b}"
        ref = "refs/remotes/upstream-check/" + src.split("/", 2)[2]
        try:
            git(repo, "fetch", "-q", "--no-tags", url, f"+{src}:{ref}")
        except RuntimeError as e:
            res[b] = f"fetch failed: {e}".splitlines()[0]
            continue
        mb = git(repo, "merge-base", fork_tip, ref, check=False)
        if not mb:
            res[b] = "no shared history"
            continue
        res[b] = (int(git(repo, "rev-list", "--count", f"{fork_tip}..{ref}")),
                  int(git(repo, "rev-list", "--count", f"{ref}..{fork_tip}")), mb[:12])
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--android-root", default=os.path.expanduser("~/evo"))
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    ledger = yaml.safe_load(open(os.path.join(HERE, "..", "state", "repositories.yaml")))
    mani = manifest_projects(a.android_root)
    behind = 0
    for r in ledger["repositories"]:
        if r.get("role") not in ("build_source", "required_camera_prebuilts"):
            continue
        for path in r.get("source_tree_paths") or []:
            if a.only and path not in a.only:
                continue
            tip = r["refs"][r["selected_ref"]]
            if path in NO_UPSTREAM:
                print(f"{path}: standalone (no upstream base)")
                continue
            url, branches = STANDALONE.get(path) or mani.get(path, (None, None))
            if not url:
                print(f"{path}: no upstream mapping")
                continue
            for b, v in check(a.android_root, path, url, branches, tip).items():
                if isinstance(v, str):
                    print(f"{path}: {url.replace(GH, '')} {b}: {v}")
                    continue
                n_behind, n_ahead, mb = v
                tag = "BEHIND" if n_behind else "current"
                print(f"{path}: {url.replace(GH, '')} {b}: {tag} behind={n_behind} "
                      f"ours={n_ahead} base={mb}")
                if b == branches[0] and n_behind:
                    behind += 1
    print(f"\n{behind} fork(s) behind their primary upstream branch")
    return 1 if behind else 0


if __name__ == "__main__":
    sys.exit(main())
