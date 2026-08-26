# Nix Data Science Templates

Reproducible development environment templates for Python and R on Nix/NixOS.

This repository provides several approaches depending on how much of the language ecosystem you want Nix to manage directly.

| Template | Environment strategy | Best for |
|---|---|---|
| `python-conda` | Nix-provided micromamba + one project-local `.conda` | Conda-compatible classes, collaboration, ordinary scientific/ML projects |
| `python-pixi` | Nix-provided Pixi + project-local `.pixi` + `pixi.lock` | Project-oriented Python workflows, stronger locking, tasks, multiple related environments |
| `python-nix` | Pure Nix Python environment | Maximum Nix reproducibility |
| `r-pixi` | Nix-provided Pixi + project-local R + `.pixi` + `pixi.lock` | Unified Pixi workflow for R, fixed R/runtime dependencies, local + server research |
| `r-renv` | Nix + R + renv | Standard CRAN/renv workflows and collaboration |
| `r-nix` | Pure Nix R environment | Maximum Nix reproducibility |

All templates pin `nixpkgs` through `flake.lock` after the first `nix develop`.

## Create a project from a template

You do not need to clone the whole repository. Create an empty project directory and initialize only the template you want.

### Python + micromamba (`python-conda`)

```bash
mkdir my-project
cd my-project
nix flake init -t github:YONGHUNI/nix-data-science-templates#python-conda
nix develop
```

The template intentionally uses one canonical project-local Conda environment:

```text
./.conda
```

Nix provides micromamba and the outer development shell; Conda manages Python and Python-coupled native libraries. The `nimba` helper keeps common project-local operations short:

```bash
nimba create
nimba activate
nimba install xarray dask
nimba run python analysis.py
nimba list
nimba status
```

With no arguments, `nimba create` creates `./.conda` from `environment.yml`. `nimba` remains intentionally single-environment and does not replace the standard `mamba` interface.

This gives Positron and VS Code a predictable interpreter at:

```text
./.conda/bin/python
```

Use this template when a project needs one main Python environment and compatibility with conventional Conda `environment.yml` workflows matters.

### Python + Pixi (`python-pixi`)

```bash
mkdir my-project
cd my-project
nix flake init -t github:YONGHUNI/nix-data-science-templates#python-pixi
nix develop
pixi install
```

Here Nix provides the Pixi executable while Pixi manages the project Python environment and dependency lockfile.

The project uses:

```text
pixi.toml     # dependency/project manifest
pixi.lock     # generated resolved dependency lock; commit this
.pixi/        # generated runtime environment; do not commit
```

Typical commands are:

```bash
pixi add xarray dask
pixi shell
pixi run python analysis.py
```

Prefer this template when one repository needs richer project-level environment composition, tasks, or multiple related environments—for example comparing several weather/AI models whose Python, JAX, PyTorch, or CUDA user-space requirements may differ.

The distinction is intentional: `python-conda` + `nimba` stays a thin, single-environment Conda workflow; `python-pixi` is the option for projects that need Pixi's broader project/environment model rather than extending `nimba` into another package manager.

### Pure Nix Python

```bash
mkdir my-project
cd my-project
nix flake init -t github:YONGHUNI/nix-data-science-templates#python-nix
nix develop
```

### R + Pixi (`r-pixi`)

```bash
mkdir my-project
cd my-project
nix flake init -t github:YONGHUNI/nix-data-science-templates#r-pixi
nix develop
pixi install
```

This mirrors the Python Pixi model: Nix supplies Pixi, while Pixi owns the project-local R runtime, R packages, native dependencies, and `pixi.lock`.

The starter manifest fixes R at `4.5.3` and includes IRkernel, data.table, dplyr, and ggplot2. Add additional packages through Pixi:

```bash
pixi add r-tidyr r-readr
pixi add r-sf r-terra
```

On NixOS, enable `programs.nix-ld.enable = true;` at the host level so conda-forge binaries can run.

For Positron, enable the experimental `positron.r.interpreters.pixiDiscovery` setting and select the Pixi-managed R installation for the current project.

This is the preferred R template when you want the same project-local environment model for Python and R, especially when the same repository should run on both an x86_64 Linux laptop/workstation and a headless x86_64 Linux server.

It can substantially reduce the need for Rocker in ordinary research workflows, but it does not replace Docker/OCI isolation when an actual container image is part of the requirement.

### R + renv

```bash
mkdir my-project
cd my-project
nix flake init -t github:YONGHUNI/nix-data-science-templates#r-renv
nix develop
```

Use this when compatibility with established CRAN/renv workflows is more important than using Pixi as the single project package manager.

### Pure Nix R

```bash
mkdir my-project
cd my-project
nix flake init -t github:YONGHUNI/nix-data-science-templates#r-nix
nix develop
```

The default template remains `python-conda`, so this is equivalent to selecting it explicitly:

```bash
nix flake init -t github:YONGHUNI/nix-data-science-templates
```

## Inspect available templates

```bash
nix flake show github:YONGHUNI/nix-data-science-templates
```

See the README inside each generated project for environment-specific details.
