# Python + micromamba

Nix provides `micromamba` inside the development shell; micromamba manages the Python environments and packages.

## Enter the development shell

```bash
nix develop
```

The shell automatically:

- provides `micromamba` from Nix
- sets `MAMBA_ROOT_PREFIX=~/.mamba`
- initializes the micromamba Bash shell hook
- provides `mamba` as an alias for `micromamba`

No separate micromamba installation under `~/.local/bin` is required.

Named environments are stored under:

```text
~/.mamba/envs/<name>
```

At this point, micromamba is ready, but Python is not installed until you create an environment.

## Option 1: Create from `environment.yml`

Use this when you already have an environment specification and want to reproduce it.

Project-local environment:

```bash
mamba create -p ./.conda -f environment.yml
mamba activate ./.conda
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
mamba create -n myenv python=3.12 ipykernel
mamba activate myenv
mamba install numpy pandas scipy matplotlib
```

You can also create the environment inside the project instead of giving it a global name:

```bash
mamba create -p ./.conda python=3.12 ipykernel
mamba activate ./.conda
mamba install numpy pandas scipy matplotlib
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

Commit `environment.yml` and the generated `flake.lock` to Git. `flake.lock` pins the Nix side, including the micromamba build. `environment.yml` is a dependency specification, so recreating it later may still resolve newer compatible Conda package builds.

For stricter Conda package locking, add a separate lockfile workflow.
