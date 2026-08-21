# Nix Data Science Templates

Reproducible development environment templates for Python and R on Nix/NixOS.

This repository provides two approaches for each language:

| Template | Environment strategy | Best for |
|---|---|---|
| `python-conda` | Nix + micromamba + conda-lock | Conda-compatible classes, collaboration, scientific/ML stacks |
| `python-nix` | Pure Nix Python environment | Maximum Nix reproducibility |
| `r-renv` | Nix + R + renv | Standard R project workflows and collaboration |
| `r-nix` | Pure Nix R environment | Maximum Nix reproducibility |

All templates pin `nixpkgs` through `flake.lock` after the first `nix develop`.

## Quick start

Copy the template you want into a new project directory, then run:

```bash
nix develop
```

See the README inside each template for the remaining steps.
