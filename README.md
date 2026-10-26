# Nix Data Science & Research Templates

Reusable, reproducible **editor-independent** development environments for research projects. Nix provides a pinned toolchain; Pixi manages language-specific package environments where applicable. Use these templates from a terminal, VS Code, Positron, Neovim, remote SSH session, or CI.

## Available templates

| Template | Environment | Intended use |
|---|---|---|
| `python-pixi` | Nix + Pixi | Python, scientific computing, notebooks, ML |
| `python-pixi-sapelo2` | Nix + Pixi | Python on UGA Sapelo2 HPC (rootless Nix workflow) |
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
