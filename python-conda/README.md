# Python + micromamba

Nix provides `micromamba`; micromamba manages the project Python packages.

## Create the environment

```bash
nix develop
mamba create -p ./.conda -f environment.yml
```

In Positron, select:

```text
./.conda/bin/python
```

## Reproducibility

Commit `environment.yml` and the generated `flake.lock` to Git. `environment.yml` is a dependency specification, so recreating it later may resolve newer compatible package builds.

For stricter package locking, add a Conda lockfile workflow separately (for example with `conda-lock`) rather than assuming `conda-lock` is available as a top-level package in the pinned Nixpkgs release.
