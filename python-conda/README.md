# Python + micromamba

Nix provides the project development shell and basic tooling. Python packages are managed with a standalone micromamba installation.

## One-time micromamba installation

Install micromamba once per machine:

```bash
mkdir -p ~/.local/bin
curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest \
  | tar -xvj -C ~/.local/bin --strip-components=1 bin/micromamba
```

Verify the installation:

```bash
~/.local/bin/micromamba --version
```

The template expects micromamba at:

```text
~/.local/bin/micromamba
```

## Enter the development shell

```bash
nix develop
```

The shell automatically:

- adds `~/.local/bin` to `PATH`
- sets `MAMBA_ROOT_PREFIX=~/.mamba`
- initializes the micromamba Bash shell hook
- provides `mamba` as an alias for `micromamba`

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

Commit `environment.yml` and the generated `flake.lock` to Git. `environment.yml` is a dependency specification, so recreating it later may resolve newer compatible package builds.

For stricter package locking, add a Conda lockfile workflow separately rather than assuming a lock tool is available in the pinned Nixpkgs release.
