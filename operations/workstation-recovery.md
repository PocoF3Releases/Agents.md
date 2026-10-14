# Restore after a Windows reinstall

Status: source and tool inventory checked 2026-09-30; recovery procedure documented, not executed. These are portable instructions, not permission to erase, install, sync or rebuild. For analysis tools use [Android tooling](android-tooling.md); for code versions use the [source map](../state/repositories.yaml).

## Before erasing the old installation

The public knowledge repository is not a backup of the workstation. Keep an encrypted offline backup on storage that will survive reinstalling Windows. Verify that the backup can be read before erasing anything.

- Preserve the WSL distribution, including Git metadata, uncommitted/untracked work, local manifests, scripts, indexes, Ghidra projects and extracted reference dumps. Pushed commits alone do not preserve these.
- Separately preserve signing material, SSH/authentication configuration and any necessary private credentials offline. Never upload them here or paste them into chat. Reauthenticate GitHub/GitLab after recovery rather than publishing tokens.
- Save `repo manifest -r` and `repo status` privately from each Android tree. Review local changes per repository; a manifest records commits, not uncommitted files. Preserve `.repo/local_manifests` even if empty. Do not publish a raw global configuration or environment dump.
- Source `out/` directories are usually disposable build output, but this workspace also holds research scripts, disassembly and the knowledge checkout. Inspect and back up those artifacts separately before deleting any output tree.
- Save this repository URL outside the PC. Windows applications and Codex plugins are separate from the Ubuntu filesystem and may need reinstalling.

From PowerShell, identify the distribution, finish running tasks, then export to a chosen external location:

```powershell
wsl --list --verbose
wsl --status
# Stop the distro only after builds and other writes have finished.
wsl --terminate Ubuntu
wsl --export Ubuntu "E:\Backups\Ubuntu.tar"
Get-FileHash "E:\Backups\Ubuntu.tar" -Algorithm SHA256
```

The drive and distro name above are examples. Keep the digest with the private backup. Test an import under a different distro name/location if storage permits. Never use `wsl --unregister` as a backup step. [Microsoft WSL commands](https://learn.microsoft.com/en-us/windows/wsl/basic-commands).

## Restore WSL

Either import the saved distribution, or install a clean one; do not run both against the same destination:

```powershell
# Restore a previously exported distribution:
wsl --import Ubuntu-Restored "D:\WSL\Ubuntu-Restored" "E:\Backups\Ubuntu.tar" --version 2
wsl -d Ubuntu-Restored
# Alternative: clean installation, when no distribution backup is available:
wsl --list --online
# Then install the intended Ubuntu 26.04 distribution using its listed name.
```

An imported distro may start as root. Confirm the existing Linux user, then set `[user]` / `default=<existing-linux-user>` in `/etc/wsl.conf`; restart that distro when no tasks are running. Preserve its other configuration. Do not assume a Windows username is the Linux username. The latest inspected environment is Ubuntu 26.04.1 LTS. Use the checkout-provided JDK for builds; analysis tools may require their own JDK.

Keep Android source inside the Linux filesystem, such as `~/evo`, rather than `/mnt/c`. Access it from Windows with `\\wsl.localhost\<distro>\home\<linux-user>\evo`. After a Windows rename or distro import, update workspace shortcuts and tool paths instead of hardcoding the former account name. Run Linux tools through Bash:

```powershell
wsl -d Ubuntu -- bash -lc 'cd ~/evo && git -C hardware/xiaomi status --short --branch'
```

Use a Bash script or pipe a Python script to `wsl -d Ubuntu -- python3 -` for complex operations; avoid interpolating PowerShell variables into shell code.

## Restore knowledge first

```bash
git clone https://github.com/PocoF3Releases/Agents.md.git ~/project-knowledge
cd ~/project-knowledge
# In a venv, or use the distro python3-yaml package:
python3 -m venv .venv
.venv/bin/pip install 'PyYAML>=6,<7'
.venv/bin/python scripts/check.py
```

Read AGENTS.md, CURRENT_STATE.md, then only the task's topic. The optional [Android-root router](../templates/android-root-AGENTS.md) can replace a generated full-tree census after preserving it separately and setting the correct workhub path. Without PC access an agent can still use the repository, public source refs and recorded validation. It cannot recover unavailable binaries or claim fresh device tests. Copying these records does not synchronize account memory or reinstall tools.

## Restore Android source deliberately

Use the saved effective manifest when available. For a clean checkout, follow [AOSP setup](https://source.android.com/docs/setup/start/requirements) and [source download](https://source.android.com/docs/setup/download), plus the selected Evolution X branch's instructions. Install its required host dependencies, Git LFS and the official Repo launcher. Keep signing keys private. Reauthenticate Git remotes using your chosen credential manager.

Current observed Android 17 manifest identity is owned by [Sources](../state/repositories.yaml). The October 9 `.repo/local_manifests` inspection was empty: the source map is therefore essential, but it is not a complete effective manifest. An existing public fork does not mean the current build still needs it.

```bash
mkdir -p ~/evo
cd ~/evo
repo init -u https://github.com/Evolution-X/manifest -b cnb --git-lfs
# Review the effective project map and required overrides before syncing.
repo manifest -o /tmp/evo-manifest.xml
# Run repo sync only when authorized; choose jobs for available resources.
```

Reconcile each necessary override by its existing manifest project name/path using a local manifest; do not add a second project at the same path. Consult the source map for A16/A17 refs, then compare upstream for already merged fixes. Keep `hardware/xiaomi` standalone. Both camera repositories are mandatory device integration. Fetch LFS content for camera/vendor projects and verify real blobs rather than pointer files. Do not clone over a nonempty checkout or use force-sync/reset to hide divergence.

The active Android 17 checkout moved from `~/evo17` to `~/evo`; determine any Android 16 checkout separately. Do not infer the Android 16 upstream manifest branch from the A17 `cnb` name: restore its saved manifest or verify the current upstream branch. User builds only; no full ROM build is started by this recovery procedure.

## Completion checkpoint

Knowledge checks pass; intended distro/user and source root resolve; Git statuses are preserved; required branches and LFS files match the chosen manifest; analysis tools report their expected versions; exactly one ADB installation owns the connection. Then report remaining missing private artifacts or credentials. A recovered environment is not a tested ROM.
