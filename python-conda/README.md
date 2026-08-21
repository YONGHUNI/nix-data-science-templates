# Python + micromamba

Nix provides `micromamba` inside the development shell; micromamba manages the Python environments and packages.

## Enter the development shell

```bash
nix develop
```

The shell automatically:

- provides `micromamba` from Nix
- sets `MAMBA_ROOT_PREFIX=~/.mamba`
- sets `MAMBA_PROJECT_PREFIX=$PWD/.conda`
- initializes the micromamba Bash shell hook
- provides `mamba` as an alias for `micromamba`
- provides a `mamba-project` helper for project-local environments

No separate micromamba installation under `~/.local/bin` is required.

## Recommended workflow: project-local `.conda`

For research projects, the recommended default is to keep the Python environment inside the project directory:

```text
my-project/
├── flake.nix
├── flake.lock
├── environment.yml
└── .conda/
```

Create a new project-local environment with:

```bash
mamba-project python=3.12 ipykernel
```

This is equivalent to:

```bash
mamba create -p ./.conda python=3.12 ipykernel
```

Then activate it with:

```bash
mamba activate ./.conda
```

The interpreter is located at:

```text
./.conda/bin/python
```

The helper does not change normal `mamba` behavior. Commands such as `mamba create -n myenv ...` still work normally when a named environment is desired.

## Create from `environment.yml`

To reproduce the environment specification shipped with the project:

```bash
mamba-project -f environment.yml
mamba activate ./.conda
```

Equivalent explicit command:

```bash
mamba create -p ./.conda -f environment.yml
```

## Why project-local environments?

A project-local `.conda` keeps the Python interpreter, Python packages, and Conda-managed native libraries together under the project directory. This is useful for scientific and geospatial stacks where packages such as GDAL, PROJ, GEOS, Rasterio, PyProj, GeoPandas, or PyTorch may depend on native libraries.

For example:

```bash
mamba-project \
  python=3.12 \
  ipykernel \
  numpy pandas scipy matplotlib \
  gdal rasterio geopandas pyproj shapely
```

The resulting environment contains its own Python and native runtime libraries under `.conda/`, reducing dependence on IDE processes inheriting the Nix development shell environment.

`~/.mamba/pkgs` remains a shared micromamba package cache. Sharing the cache does not make the environments themselves shared: each project's resolved environment still lives in that project's `.conda/` directory.

Project-local environments are not filesystem sandboxes. Another project could deliberately execute an interpreter by absolute path, but normal project workflows and IDE interpreter selection can remain project-specific.

## Named environments

Named environments remain available when they are useful:

```bash
mamba create -n myenv python=3.12 ipykernel
mamba activate myenv
```

They are stored under:

```text
~/.mamba/envs/<name>
```

Use named environments for intentionally shared or general-purpose environments. Prefer `.conda` for project-specific research environments.

## Positron / VS Code

For the recommended project-local environment, select:

```text
./.conda/bin/python
```

as the Python interpreter and Jupyter kernel.

Because the interpreter and its Conda-managed native libraries are both inside `.conda`, Positron or VS Code can launch that interpreter directly without relying on the IDE process to inherit every environment variable from `nix develop`.

Install `ipykernel` in the environment when Jupyter notebook support is needed.

## Responsibility boundary

The intended division is:

```text
Nix / flake.nix
├── micromamba
├── development-shell tooling
└── host/system-level dependencies when appropriate

project/.conda
├── Python
├── ipykernel
├── Python packages
└── Python-coupled native scientific libraries
```

For example, keep GDAL/PROJ/GEOS and their Python bindings in the same Conda environment rather than mixing a Conda Python package with unrelated Nix-provided runtime libraries.

Host-level facilities such as the NVIDIA kernel driver remain managed by NixOS, while Python frameworks and their user-space runtime dependencies can live in `.conda`.

## Reproducibility

Do not commit `.conda/` itself. It is excluded by `.gitignore`.

Commit:

- `flake.nix`
- `flake.lock`
- `environment.yml`

`flake.lock` pins the Nix side, including the micromamba build. `environment.yml` records the Conda dependency specification, although recreating it later may still resolve newer compatible package builds.

For stricter Conda package locking, add a separate lockfile workflow.
