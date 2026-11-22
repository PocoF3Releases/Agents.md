#!/usr/bin/env python3
"""Rebase a linear PocoF3Releases fork branch onto its updated upstream base.

Typical kernel use (from anywhere):
  scripts/rebase_fork.py --repo ~/evo/kernel/xiaomi/sm8250 \
      --upstream https://github.com/LineageOS/android_kernel_qcom_sm8250 \
      --upstream-branch lineage-20 --fork-remote poco-device --fork-branch aosp-17 \
      --check-cmd 'scripts/update_defconfig --check'

Stages (each is safe to rerun):
  1. fetch upstream and fork, find the old base and refuse non-linear forks;
  2. report the upstream delta, overlapping files and our patches upstream
     already contains (git drops those during the rebase);
  3. rebase onto the new base on a local work branch; on a conflict it stops so
     you can resolve, `git add`, `git rebase --continue`, then rerun with
     --resume;
  4. verify every kept commit keeps author, date and message, report changed
     patches, and prove the tree equals "new upstream + our old delta"
     file by file (files touched by both sides are listed for review);
  5. optional --check-cmd, then --push: back up the old tip as
     <branch>-pre-rebase-YYYYMMDD and force-push with a lease.
Nothing is pushed without --push.
"""
import argparse
import datetime
import os
import subprocess
import sys


def run(*args, check=True, cwd=None, inp=None):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True, input=inp)
    if check and r.returncode:
        sys.stderr.write(r.stdout + r.stderr)
        raise SystemExit(f"failed: {' '.join(args)}")
    return r


def git(*args, check=True):
    return run("git", *args, check=check).stdout.strip()


def patch_id(sha):
    out = subprocess.run(f"git show {sha} | git patch-id --stable", shell=True,
                         capture_output=True).stdout.split()
    return out[0].decode() if out else "EMPTY"


def meta(sha):
    return git("log", "-1", "--format=%an%x00%ae%x00%ad%x00%B", sha)


def changed(a, b):
    return set(git("diff", "--name-only", "--no-renames", a, b).split())


def verify(old_base, old_tip, new_base, new_tip):
    old = git("rev-list", "--reverse", f"{old_base}..{old_tip}").split()
    new = git("rev-list", "--reverse", f"{new_base}..{new_tip}").split()
    if git("rev-list", "--merges", f"{new_base}..{new_tip}"):
        raise SystemExit("new history contains merges")
    upstream_has = {l[2:] for l in git("cherry", new_base, old_tip, old_base).splitlines()
                    if l.startswith("- ")}
    kept = [c for c in old if c not in upstream_has]
    print(f"commits: old {len(old)}, already upstream {len(upstream_has)}, "
          f"expected {len(kept)}, new {len(new)}")
    problems = 0
    if len(kept) != len(new):
        print("COUNT MISMATCH: a commit became empty or was skipped; inspect the rebase log")
        problems += 1
    changed_patches = []
    for o, n in zip(kept, new):
        if meta(o) != meta(n):
            print(f"METADATA {o[:12]} -> {n[:12]}"); problems += 1
        elif patch_id(o) != patch_id(n):
            changed_patches.append((o, n))
    for o, n in changed_patches:
        print(f"patch adjusted while rebasing: {o[:12]} -> {n[:12]} "
              f"{git('log', '-1', '--format=%s', n)}")
    ours = changed(old_base, old_tip)
    theirs = changed(old_base, new_base)
    # Files only we touched (or nobody touched) must equal our old tip; files
    # only upstream touched must equal the new base.
    for f in sorted(changed(old_tip, new_tip) - theirs):
        print(f"TREE {f}: differs from our old tip although upstream did not touch it")
        problems += 1
    for f in sorted(changed(new_base, new_tip) - ours):
        print(f"TREE {f}: differs from the new base although we never touched it")
        problems += 1
    both = sorted(ours & theirs)
    if both:
        print(f"{len(both)} files changed by both sides (review these diffs):")
        for f in both:
            print("  " + f)
    print("VERIFY", "OK" if not problems else f"FAILED ({problems})")
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--upstream", required=True, help="upstream URL or remote name")
    ap.add_argument("--upstream-branch", required=True)
    ap.add_argument("--fork-remote", required=True)
    ap.add_argument("--fork-branch", default="aosp-17")
    ap.add_argument("--onto", help="rebase onto this commit instead of the upstream tip")
    ap.add_argument("--resume", action="store_true", help="verify after a finished manual rebase")
    ap.add_argument("--check-cmd", help="extra command to run in the repo after verification")
    ap.add_argument("--push", action="store_true")
    a = ap.parse_args()
    os.chdir(os.path.expanduser(a.repo))
    up_ref = f"refs/remotes/rebase-upstream/{a.upstream_branch}"
    fork_ref = f"refs/remotes/{a.fork_remote}/{a.fork_branch}"
    work = f"rebase/{a.fork_branch}"
    state = os.path.join(git("rev-parse", "--git-dir"), "rebase-fork-state")
    if a.resume:
        if os.path.isdir(os.path.join(git("rev-parse", "--git-dir"), "rebase-merge")):
            raise SystemExit("a rebase is still in progress; finish it with git rebase --continue")
        old_base, old_tip, new_base = open(state).read().split()
    else:
        if git("status", "--porcelain", "--untracked-files=no"):
            raise SystemExit("worktree has uncommitted changes")
        git("fetch", "-q", a.upstream, f"+refs/heads/{a.upstream_branch}:{up_ref}")
        git("fetch", "-q", a.fork_remote, f"+refs/heads/{a.fork_branch}:{fork_ref}")
        old_tip = git("rev-parse", fork_ref)
        new_base = git("rev-parse", (a.onto or up_ref) + "^{commit}")
        old_base = git("merge-base", old_tip, up_ref)
        if git("rev-list", "--merges", f"{old_base}..{old_tip}"):
            raise SystemExit("fork history above the upstream base is not linear")
        print(f"old base {old_base[:12]}  fork tip {old_tip[:12]}  new base {new_base[:12]}")
        print(f"fork commits: {git('rev-list', '--count', f'{old_base}..{old_tip}')}, "
              f"new upstream commits: {git('rev-list', '--count', f'{old_base}..{new_base}')}")
        if old_base == new_base:
            print("fork already sits on the requested upstream commit; nothing to rebase")
            return 0
        if run("git", "merge-base", "--is-ancestor", old_base, new_base,
               check=False).returncode:
            print("note: the new base does not contain the old base (upstream was rewritten)")
        both = changed(old_base, old_tip) & changed(old_base, new_base)
        print(f"files changed by both sides: {len(both)}")
        open(state, "w").write(f"{old_base} {old_tip} {new_base}\n")
        git("checkout", "-q", "-B", work, old_tip)
        r = run("git", "rebase", "-q", "--onto", new_base, old_base, work, check=False)
        if r.returncode:
            sys.stderr.write(r.stdout + r.stderr)
            print("\nCONFLICT. Resolve the listed files keeping both the upstream change and "
                  "our intent, `git add` them, run `git rebase --continue` until it finishes, "
                  "then rerun this command with --resume.")
            return 2
    new_tip = git("rev-parse", work)
    print(f"new tip {new_tip[:12]}")
    if verify(old_base, old_tip, new_base, new_tip):
        return 1
    if a.check_cmd:
        r = subprocess.run(a.check_cmd, shell=True)
        if r.returncode:
            raise SystemExit(f"check command failed: {a.check_cmd}")
    if not a.push:
        print(f"Not pushed. Review `{work}`, then rerun with --resume --push.")
        return 0
    backup = f"{a.fork_branch}-pre-rebase-{datetime.date.today():%Y%m%d}"
    git("push", a.fork_remote, f"{old_tip}:refs/heads/{backup}")
    git("push", a.fork_remote, f"--force-with-lease={a.fork_branch}:{old_tip}",
        f"{new_tip}:refs/heads/{a.fork_branch}")
    print(f"pushed {new_tip[:12]} to {a.fork_branch}; old tip kept as {backup}")
    os.remove(state)
    return 0


if __name__ == "__main__":
    sys.exit(main())
