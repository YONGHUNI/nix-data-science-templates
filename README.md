# Nix Data Science & Research Templates

Reusable, reproducible **editor-independent** development environments for research projects. Nix provides a pinned toolchain; Pixi manages language-specific package environments where applicable. Use these templates from a terminal, VS Code, Positron, Neovim, remote SSH session, or CI.

## Available templates

| Template | Environment | Intended use |
|---|---|---|
| `python-pixi` | Nix + Pixi | Python, scientific computing, notebooks, ML |
| `python-pixi-sapelo2` | Nix + Pixi | Sapelo2 Python environment with Pixi cache and environments on fast `/lscratch` storage |
| `r-pixi` | Nix + Pixi | R, IRkernel, native/source package builds |
| `latex-nix` | Nix | XeLaTeX, latexmk, tex-fmt, SyncTeX-enabled PDF builds |

Earlier Conda, pure-Nix, and renv experiments remain on the `archive/pre-positron-cleanup-2026-08-28` branch. The archived branch name is historical and does not determine the focus of current templates.

## Create a project

Choose a preset, create an empty directory, and initialize it:

```bash
mkdir my-python-project && cd my-python-project
nix flake init -t github:YONGHUNI/nix-data-science-templates#python-pixi
nix develop
pixi install
```

For other presets, replace `#python-pixi` with `#r-pixi`, `#python-pixi-sapelo2`, or `#latex-nix` as appropriate. Each template has its own README and dependencies.

### Python and R

```bash
# In a Python or R Pixi-based project:
nix develop
pixi install
pixi run python --version   # python-pixi
# or: pixi run R --version  # r-pixi

# Add dependencies to the project manifest and lockfile:
pixi add xarray dask        # example for Python
```

Commit `flake.lock` and `pixi.lock`. Do not commit the generated `.pixi/` environment. `ipykernel` and `IRkernel` support standard Jupyter clients and compatible editors; they do not require any particular IDE.

### Sapelo2 storage optimization

Unlike the general `python-pixi` preset, `python-pixi-sapelo2` is designed to reduce storage I/O bottlenecks on Sapelo2. Its shell hook sets `PIXI_CACHE_DIR=/lscratch/$USER/pixi-cache` and configures detached Pixi environments in `/lscratch/$USER/pixi-envs` through `.pixi/config.toml`. Rootless Nix may be needed on the cluster, but it is not the defining difference of this preset. Check scratch retention policies before storing anything important there.

### LaTeX

```bash
mkdir my-latex-project && cd my-latex-project
nix flake init -t github:YONGHUNI/nix-data-science-templates#latex-nix
nix develop --command latexmk -synctex=1 -xelatex -pdfxe main.tex
```

The LaTeX preset provides a CLI-first compilation and formatting environment. Its `.vscode/` configuration adds **optional** LaTeX Workshop integration for VS Code-compatible editors, including Positron. The Nix build and formatter work without that configuration or extension.

## NixOS host prerequisites for Pixi-based presets

The templates do not alter host configuration. For conda-forge binaries running on NixOS, enable `nix-ld` on the host:

```nix
programs.nix-ld.enable = true;
```

Some R startup environments also need `/usr/bin/which`; where necessary, configure that compatibility path in the NixOS host instead of the project template. These host-specific notes do not apply to the `latex-nix` preset.

## Local, remote, and CI use

The same project manifests can be used on a supported local Linux machine, a remote compute node, or an automated workflow. Install each project's Pixi environment on the target machine. The templates are not tied to Positron, another editor, or a graphical desktop.

If a project path contains symlinked components, use its canonical path (`pwd -P` / `realpath`) when tooling passes it to `nix develop path:...`.

## Inspect the template catalog

```bash
nix flake show github:YONGHUNI/nix-data-science-templates
```

The default preset remains `python-pixi`:

```bash
nix flake init -t github:YONGHUNI/nix-data-science-templates
```

For full details, see [Python + Pixi](python-pixi/README.md), [Sapelo2 Python + Pixi](python-pixi-sapelo2/README.md), [R + Pixi](r-pixi/README.md), and [LaTeX + Nix](latex-nix/README.md).

## Pixi version policy (Nov 2026)

**Template creation and project reproducibility are different concerns.** The three Pixi templates intentionally have **no template-side flake.lock**. After using `nix flake init`, the new project runs `nix flake lock` (automatically on first applicable Nix command) and commits its own `flake.lock` and `pixi.lock`.

For predictable installation on Slurm nodes with local Nix stores, the template's `nixpkgs-pixi` input is pinned to a **full, binary-cache-verified Nixpkgs commit** instead of a moving unstable branch. The starting point is Pixi 0.82.1 (`b57afef75289b29747cd49e60cb86c1062542072`), verified on Sapelo2 x86_64-linux without compiling Pixi. The remaining toolchain continues tracking `nixos-26.05` per project lockfile.

### Monthly update policy

The [monthly Pixi updater](.github/workflows/pixi-monthly-update.yml) runs once a month (or manually via **Actions → Monthly verified Pixi update → Run workflow**):

1. Inspect both `nixpkgs-unstable` and `nixos-unstable` at their current commit SHAs.
2. Evaluate their packaged Pixi versions. Skip candidates with versions not newer than the current pin.
3. Try the newest candidates in version order with **`nix build --no-link --option max-jobs 0`**. A candidate requiring local source compilation is rejected.
4. If an eligible candidate exists, update all three Pixi templates and verify their flake/devShell evaluations, the shared Pixi binary and general Python/R devShell execution.
5. Open a **reviewable pull request**. The workflow never auto-merges and never changes existing projects.

The check runs on a fresh GitHub-hosted `x86_64-linux` environment using the normal Nix binary cache. It verifies *cache availability at check time*, not permanent cache retention, future network access, or real Sapelo2/rootless behavior. Before merging a major change, optionally repeat the Pixi and Positron smoke tests on Sapelo2.

To let scheduled workflows open PRs, enable **Settings → Actions → General → Workflow permissions → Allow GitHub Actions to create and approve pull requests**. The workflow requests only repository contents and PR write permissions. GitHub may disable scheduled workflows on public repositories after 60 days of inactivity; manual runs remain available once re-enabled.

The [Pixi template CI](.github/workflows/pixi-templates-ci.yml) validates manual changes as well. No `flake.lock` is added to these three template directories; CI generates temporary lock files outside the repository while evaluating candidates. The shell hook keeps the version-sensitive `PIXI_TLS_ROOT_CERTS` compatibility handling, without overriding explicit `webpki`/`all` choices.
