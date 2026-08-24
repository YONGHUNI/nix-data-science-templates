# Python + micromamba

Nix provides `micromamba` inside the development shell; micromamba manages the Python environments and packages.

The recommended workflow is deliberately hybrid:

- Nix provides micromamba and the reproducible development shell.
- Each project keeps its Python/Conda runtime in `./.conda`.
- `environment.yml` describes the Conda-side dependencies.
- `flake.lock` pins the Nix side.
- `~/.mamba/pkgs` remains a shared package cache across projects.

The local `.conda` directory is a disposable build/runtime artifact and should not be committed to Git.

## Enter the development shell

```bash
nix develop
```

The shell automatically:

- provides `micromamba` from Nix
- sets `MAMBA_ROOT_PREFIX=~/.mamba`
- initializes the micromamba Bash shell hook
- provides `mamba` as an alias for standard `micromamba`
- provides `nimba`, a thin helper dedicated to the current project's `./.conda`

No separate micromamba installation under `~/.local/bin` is required.

## Recommended project layout

```text
my-project/
├── flake.nix
├── flake.lock
├── environment.yml
├── .gitignore
├── .conda/          # generated; do not commit
└── source files
```

The actual Python interpreter and Conda-managed native libraries live inside `.conda`, while downloaded package artifacts are cached globally under `~/.mamba/pkgs`.

This is not a pure-Nix Python environment. It is an intentional Nix + Conda boundary: Nix controls the outer development environment, and Conda controls Python and Python-coupled native dependencies.

## `nimba`: project-local helper

`nimba` always targets the `.conda` directory belonging to the project in which `nix develop` was entered. It does not replace normal micromamba behavior; use `mamba` whenever you want the standard CLI, including named environments.

### Create

With no extra arguments, `nimba create` builds the project environment from `environment.yml`:

```bash
nimba create
```

Equivalent explicit command:

```bash
mamba create -p ./.conda -f environment.yml
```

You can also pass normal create arguments:

```bash
nimba create python=3.12 ipykernel
```

or use another specification file:

```bash
nimba create -f environment-gpu.yml
```

`nimba create` refuses to overwrite an existing project environment. Treat `.conda` as disposable: if you intentionally want a clean rebuild, remove it and create it again.

### Activate

```bash
nimba activate
```

This activates the project's `.conda` in the current shell.

The interpreter is then:

```text
./.conda/bin/python
```

### Install

```bash
nimba install xarray dask netcdf4
```

This explicitly installs into the project's `.conda`, even if another environment is active. For reproducible work, record dependencies that become part of the project in `environment.yml` rather than relying only on interactive installs.

### Run without activation

```bash
nimba run python analysis.py
nimba run pytest
nimba run python -c 'import sys; print(sys.executable)'
```

This uses `micromamba run -p ./.conda ...` and is useful for scripts, batch jobs, and reproducible commands where shell activation is unnecessary.

### List packages

```bash
nimba list
```

Additional `micromamba list` arguments can be passed through normally.

### Status

```bash
nimba status
```

This reports the project root, environment path, whether the environment exists and is active, the Python interpreter/version, and whether `environment.yml` is present.

### Help

```bash
nimba --help
```

## Why project-local `.conda`?

A project-local environment keeps the Python interpreter, Python packages, and Conda-managed native libraries together under the project directory. This is especially useful for scientific, geospatial, and ML stacks where Python packages depend on ABI-compatible native libraries.

Examples include:

- GDAL / Rasterio
- PROJ / PyProj
- GEOS / Shapely
- GeoPandas
- PyTorch and Conda-managed user-space runtime dependencies

Keeping these in one Conda prefix avoids pairing a Conda Python binding with unrelated native runtime libraries from another package-management layer.

The project-local design also gives Positron and VS Code a stable interpreter path:

```text
./.conda/bin/python
```

This reduces accidental interpreter selection from unrelated projects and avoids requiring the IDE process to inherit every development-shell environment variable.

Project-local environments are not security sandboxes. Another process can deliberately execute another project's interpreter by path. The goal is project-level dependency isolation and predictable IDE selection, not filesystem isolation.

## Shared cache vs project environment

Micromamba's package cache remains shared:

```text
~/.mamba/pkgs/
```

Actual environments remain project-specific:

```text
project-a/.conda/
project-b/.conda/
```

This provides a practical balance: projects have independent runtime environments while micromamba can reuse cached package artifacts.

## Standard `mamba` remains available

`nimba` is intentionally small. It does not manage global or named environments.

Use standard micromamba commands when needed:

```bash
mamba create -n myenv python=3.12
mamba activate myenv
mamba env list
```

Named environments are stored under:

```text
~/.mamba/envs/<name>
```

Use them for intentionally shared or general-purpose environments. Prefer `.conda` for project-specific research environments.

## Positron / VS Code

For a project-local environment, select:

```text
./.conda/bin/python
```

as the Python interpreter and Jupyter kernel.

Install `ipykernel` in the environment when notebook/Jupyter support is needed.

## Responsibility boundary

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

Host-level facilities such as the NVIDIA kernel driver remain managed by NixOS, while Python frameworks and their user-space dependencies can live in `.conda`.

## Reproducibility

Do not commit `.conda/` itself. It is excluded by `.gitignore`.

Commit:

- `flake.nix`
- `flake.lock`
- `environment.yml`

`flake.lock` pins the Nix side, including the micromamba build. `environment.yml` records the Conda dependency specification, although recreating it later may still resolve newer compatible package builds.

For stricter Conda package reproducibility, add a dedicated Conda lockfile workflow later rather than turning `nimba` into a separate package manager.
