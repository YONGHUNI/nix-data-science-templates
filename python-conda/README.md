# Python + micromamba

Nix provides the environment tooling; micromamba manages the project Python packages.

## Create the environment

```bash
nix develop
mamba create -p ./.conda -f environment.yml
```

In Positron, select:

```text
./.conda/bin/python
```

## Reproducible lockfile

Generate a conda lockfile and commit it to Git:

```bash
conda-lock -f environment.yml
```

The generated lockfile captures the resolved Conda package set more strictly than `environment.yml` alone.
