# Python + micromamba

Nix provides `micromamba`; micromamba manages the project Python packages.

## Enter the development shell

```bash
nix develop
```

The shell initializes micromamba automatically and uses:

```text
~/.mamba
```

as the micromamba root prefix. Named environments are therefore stored under:

```text
~/.mamba/envs/<name>
```

At this point, `micromamba` is available, but Python is not installed yet. You can create a Python environment in either of two ways.

## Option 1: Create from `environment.yml`

Use this when you already have an environment specification and want to reproduce it.

Project-local environment:

```bash
mamba create -p ./.conda -f environment.yml
```

Named environment:

```bash
mamba create -n myenv -f environment.yml
mamba activate myenv
```

The project-local form creates the interpreter at:

```text
./.conda/bin/python
```

This is convenient for Positron because the environment stays attached to the project directory.

## Option 2: Create a new environment interactively

Use this when starting a new project and deciding packages as you go.

```bash
mamba create -n myenv python=3.12
mamba activate myenv
mamba install numpy pandas scipy matplotlib ipykernel
```

You can also create the environment inside the project instead of giving it a global name:

```bash
mamba create -p ./.conda python=3.12
mamba activate ./.conda
mamba install numpy pandas scipy matplotlib ipykernel
```

Conceptually:

```text
environment.yml
→ reproduce an already specified environment

new mamba environment
→ build an environment interactively
```

These workflows can be combined. A common pattern is to create an environment interactively first, stabilize the package set, and then record a reusable environment specification for the project.

## Positron / VS Code

For a project-local environment, select:

```text
./.conda/bin/python
```

as the Python interpreter/kernel.

For a named environment, select the interpreter under:

```text
~/.mamba/envs/<name>/bin/python
```

Install `ipykernel` in the environment if you want to use it as a Jupyter kernel.

## Reproducibility

Commit `environment.yml` and the generated `flake.lock` to Git. `environment.yml` is a dependency specification, so recreating it later may resolve newer compatible package builds.

For stricter package locking, add a Conda lockfile workflow separately (for example with `conda-lock`) rather than assuming `conda-lock` is available as a top-level package in the pinned Nixpkgs release.
