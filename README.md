# Nix Data Science Templates

Reproducible development environment templates for Python and R on Nix/NixOS.

This repository provides two approaches for each language:

| Template | Environment strategy | Best for |
|---|---|---|
| `python-conda` | Nix-provided micromamba + project-local `.conda` | Conda-compatible classes, collaboration, scientific/ML stacks |
| `python-nix` | Pure Nix Python environment | Maximum Nix reproducibility |
| `r-renv` | Nix + R + renv | Standard R project workflows and collaboration |
| `r-nix` | Pure Nix R environment | Maximum Nix reproducibility |

All templates pin `nixpkgs` through `flake.lock` after the first `nix develop`.

## Create a project from a template

You do not need to clone the whole repository. Create an empty project directory and initialize only the template you want.

### Python + micromamba

```bash
mkdir my-project
cd my-project
nix flake init -t github:YONGHUNI/nix-data-science-templates#python-conda
nix develop
```

The Python template uses an intentional Nix + Conda split:

- Nix provides micromamba and the outer development shell.
- The project keeps its Python runtime and Python-coupled native libraries in `./.conda`.
- `environment.yml` describes Conda-side dependencies.
- `~/.mamba/pkgs` is shared as a package cache across projects.
- `.conda/` is disposable and excluded from Git.

The template provides `nimba`, a small project-local helper. The default workflow is:

```bash
nimba create
nimba activate
```

With no arguments, `nimba create` recreates the environment from `environment.yml`. Useful project-scoped commands include:

```bash
nimba install xarray dask
nimba run python analysis.py
nimba list
nimba status
```

`nimba` always targets the current project's `.conda`. It does not replace the standard micromamba interface: `mamba` remains available for named or global environment operations.

This layout gives Positron and VS Code a predictable project-specific interpreter at:

```text
./.conda/bin/python
```

The approach is not pure Nix. It intentionally keeps Python and ABI-coupled scientific libraries such as GDAL/PROJ/GEOS, Rasterio, or PyTorch user-space dependencies inside one Conda prefix, while Nix manages the development-shell and host-side boundary.

See the generated `python-conda/README.md` for detailed `nimba` usage, IDE behavior, native-library guidance, and reproducibility notes.

### Pure Nix Python

```bash
mkdir my-project
cd my-project
nix flake init -t github:YONGHUNI/nix-data-science-templates#python-nix
nix develop
```

### R + renv

```bash
mkdir my-project
cd my-project
nix flake init -t github:YONGHUNI/nix-data-science-templates#r-renv
nix develop
```

### Pure Nix R

```bash
mkdir my-project
cd my-project
nix flake init -t github:YONGHUNI/nix-data-science-templates#r-nix
nix develop
```

The default template is `python-conda`, so this is equivalent to selecting it explicitly:

```bash
nix flake init -t github:YONGHUNI/nix-data-science-templates
```

## Inspect available templates

```bash
nix flake show github:YONGHUNI/nix-data-science-templates
```

See the README inside each generated project for the remaining environment-specific steps.
