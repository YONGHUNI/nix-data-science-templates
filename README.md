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

The Python template provides micromamba through Nix and initializes it automatically. The recommended workflow is to keep the Python environment inside the project as `./.conda`.

Create one with:

```bash
mamba-project python=3.12 ipykernel
mamba activate ./.conda
```

`mamba-project` is a convenience helper equivalent to:

```bash
mamba create -p ./.conda python=3.12 ipykernel
```

Normal micromamba commands are unchanged, so named environments remain available with `mamba create -n ...` when intentionally needed.

The project-local design keeps Python and Python-coupled native scientific libraries such as GDAL, PROJ, GEOS, Rasterio, and PyTorch runtime dependencies together in one environment. This also gives Positron and VS Code a stable project-specific interpreter at `./.conda/bin/python`.

The micromamba package cache under `~/.mamba/pkgs` is shared across projects, while each project's actual environment remains under its own `.conda/` directory.

See the generated `python-conda/README.md` for the environment boundary, IDE behavior, geospatial examples, and reproducibility guidance.

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
