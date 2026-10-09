# Windows and WSL host tools

For LLVM, Ghidra and ADB use [Android tooling](android-tooling.md).
Inventory commands/PATH first; install only missing tools needed for authorized
work. No blanket OS upgrade or project-rule changes. Windows 11/Ubuntu 26.04.1
were host-tested **2026-10-06**; recheck versions when needed.

## Current host checkpoint

October 9: the documented Ubuntu apt package set was already installed and
`dpkg --audit` was clean. User tools resolve in a fresh login shell: uv 0.12.21,
Ruff 0.16.10, pytest 9.1.1, fd/fdfind 10.3.0; PyYAML 6.0.3. Added the missing
fd user symlink and repaired shell discovery. Windows gh/rg/fd/jq/uv/Ruff/pytest
were present. Windows Python resolved into an application venv; do not use it
for global package changes. Windows ADB was not on PATH; Linux ADB was present.
WSL gh is installed but unauthenticated; public API reads still work.

## Host utility setup

Ubuntu's exercised host/build package set (select what the task needs):

```bash
sudo apt-get update
sudo apt-get install --no-install-recommends   build-essential git git-lfs ccache python3-venv python3-pip python3-yaml pipx   ripgrep fd-find jq curl wget rsync file binutils patchelf   clang-format shellcheck device-tree-compiler dwarves   libssl-dev libelf-dev libncurses-dev bc bison flex   unzip zip 7zip xz-utils lz4 zstd cpio libxml2-utils xmlstarlet   sqlite3 strace lsof time bash-completion
```

Verify `dpkg --audit`. Ubuntu names `fd` as `fdfind`; use it directly or create
an `fd` symlink in `~/.local/bin` only when absent. Host clang-format does not
select the Android compiler.

Windows may already have PowerShell, Git, Python and Platform Tools. Missing
helpers can be installed through WinGet:

```powershell
winget install --id GitHub.cli --exact --source winget
winget install --id jqlang.jq --exact --source winget
winget install --id sharkdp.fd --exact --source winget
winget install --id BurntSushi.ripgrep.MSVC --exact --source winget
winget install --id astral-sh.uv --exact --source winget
uv tool install ruff
uv tool install pytest
uv tool update-shell
```

On Ubuntu install missing `uv` using [official instructions](https://docs.astral.sh/uv/getting-started/installation/), then:

```bash
uv tool install ruff --python /usr/bin/python3
uv tool install pytest --python /usr/bin/python3
uv tool update-shell
```

Use isolated uv tools/venvs/pipx, existing suitable Python and PyYAML 6.x for hub
validators. Managed Python is optional. Do not alter system Python or an app's
Torch/ROCm environment for host convenience.

## Verify and use

A missing command may mean stale PATH. Open a fresh shell; verify discovery and
versions of `gh`, `rg`, `fd`/`fdfind`, `jq`, `uv`, `ruff`, `pytest` and ShellCheck
where installed. From PowerShell use `wsl -d Ubuntu -- bash -lc` for Linux user
tools. Cloning this repo installs none of them. Keep authentication data private;
see [optional skill setup](first-chat.md).

Use `rg --files`/`fd` for discovery, scoped `rg -n` for code, `jq` for selected
JSON fields and focused Ruff/pytest checks. Bound output and retain real command
diagnostics rather than whole-file dumps or generic subprocess tracebacks.
No measured token reduction is claimed.
