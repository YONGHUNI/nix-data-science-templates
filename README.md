# Nix Data Science Templates

Reproducible development environment templates for Python and R on Nix/NixOS.

This repository provides two approaches for each language:

| Template | Environment strategy | Best for |
|---|---|---|
| `python-conda` | Nix + standalone micromamba | Conda-compatible classes, collaboration, scientific/ML stacks |
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

The Python + micromamba template expects a standalone micromamba binary at `~/.local/bin/micromamba`. See the generated project README for the one-time installation command and environment setup examples.

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
