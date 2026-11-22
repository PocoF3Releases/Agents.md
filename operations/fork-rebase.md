# Rebase a fork onto its upstream base

[`scripts/rebase_fork.py`](../scripts/rebase_fork.py) moves a linear fork branch
onto the newest upstream commit and proves the result. It works for any fork in the
[source ledger](../state/repositories.yaml) whose history above the upstream base
has no merges (kernel, device and vendor trees).

## Kernel example

Run from `~/evo` so the defconfig check finds the Android Clang prebuilts:

```bash
python3 ~/evo/.workhub/scripts/rebase_fork.py --repo ~/evo/kernel/xiaomi/sm8250 --upstream https://github.com/LineageOS/android_kernel_qcom_sm8250 --upstream-branch lineage-20 --fork-remote poco-device --fork-branch aosp-17 --check-cmd 'scripts/update_defconfig --check'
```

- No new upstream commits: it prints `nothing to rebase` and changes nothing.
- Otherwise it rebases onto a local `rebase/aosp-17` branch and verifies the result.
  Nothing is pushed until you add `--push`.
- On a conflict it stops (exit 2). Resolve the files, keeping both the upstream
  change and our intent, then `git add` them. Run `git rebase --continue` until it
  finishes, then rerun the same command with `--resume`.
- Review the "changed by both sides" files and any "patch adjusted" commits.
  Then rerun with `--resume --push`. The old tip is pushed to
  `aosp-17-pre-rebase-YYYYMMDD` before a leased force-push.

If upstream rewrote its branch (Evolution X force-pushes `cnb`), the merge-base
is too old and would replay rewritten upstream commits. Pass `--old-base` with
the last upstream commit directly under our commits.
`scripts/check_fork_bases.py` shows this as large `behind` and `ours` counts.
`git cherry <upstream> <fork>` then marks only our commits with `+`.

## What the verification guarantees

- Every kept commit keeps its author, date and message.
- Patches git found already upstream are dropped and counted.
- Files changed only by us equal our old tip.
- Files changed only upstream equal the new base.
- Files changed by both sides are listed for review.

`--check-cmd` adds a repository check. For the kernel, `scripts/update_defconfig
--check` regenerates the tracked `alioth_defconfig` and must match it. If upstream
changes a Kconfig fragment, run `scripts/update_defconfig` without `--check` and
add the regenerated defconfig before pushing. When the kernel is not under an
Android tree, pass `--android-root ~/evo` to the defconfig script.

## 2026-11-22 dry run

`lineage-20` had no commits newer than `abd144b`, so the real fork was already
current. A stale copy of the 350-commit kernel fork, placed four upstream commits
back, rebased in 42 seconds. Its tree was byte-identical to the published tip and
the defconfig check passed. A simulated upstream edit to `kernel/sched/tune.c`
exercised the stop, resolve and `--resume` path. The push path was exercised
against a local test remote only.
