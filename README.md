# Nix Data Science Templates for Positron

Reproducible Python and R project templates for Positron on Nix/NixOS.

This repository now focuses on the two workflows that were validated with Positron locally and over Remote SSH:

| Template | Runtime manager | Intended use |
|---|---|---|
| `python-pixi` | Pixi | Python data science, notebooks, scientific/ML projects |
| `r-pixi` | Pixi | R data science, IRkernel, native/source package builds |

The previous Conda, pure-Nix, and renv templates are preserved on the archive branch `archive/pre-positron-cleanup-2026-08-28`.

## Host prerequisites on NixOS

The project templates intentionally do not modify the host. For Pixi/conda-forge compatibility, the NixOS host should provide:

```nix
{
  programs.nix-ld.enable = true;

  systemd.tmpfiles.rules = [
    "d /usr/bin 0755 root root -"
    "L+ /usr/bin/which - - - - ${pkgs.which}/bin/which"
  ];
}
```

`nix-ld` allows generic dynamically linked binaries from Pixi/conda-forge to run on NixOS. The `/usr/bin/which` compatibility link is needed by the current conda-forge R startup path on NixOS.

## Positron and Pixi discovery

Each project pins the Pixi executable through its Nix flake and keeps its runtime under the project directory. No global Pixi installation is required for normal shell use.

Positron's Python support can discover project-local Pixi Python environments. For R, enable:

```text
positron.r.interpreters.pixiDiscovery
```

Current Positron R discovery searches for `pixi` on the extension-host `PATH` and then at `~/.pixi/bin/pixi`. If Positron itself is not launched from `nix develop`, a small user-level dispatcher at that fallback path can delegate calls back into the current project's flake. This workaround belongs in the user's host/Home Manager configuration rather than in each project template.

The project remains reproducible because the dispatcher does not provide its own Pixi package; it invokes the project-pinned Pixi from `nix develop`.

## Create a Python project

```bash
mkdir my-python-project
cd my-python-project
nix flake init -t github:YONGHUNI/nix-data-science-templates#python-pixi
nix develop
pixi install
```

The generated project uses:

```text
flake.nix
flake.lock
pixi.toml
pixi.lock      # commit this
.pixi/         # generated; do not commit
```

Typical commands:

```bash
pixi add xarray dask
pixi run python analysis.py
pixi shell
```

`ipykernel` is included so the environment can be used directly from Positron notebooks.

## Create an R project

```bash
mkdir my-r-project
cd my-r-project
nix flake init -t github:YONGHUNI/nix-data-science-templates#r-pixi
nix develop
pixi install
```

The starter environment contains R, IRkernel, common data-science packages, and a C/C++/Fortran source-build toolchain.

Typical commands:

```bash
pixi run R
pixi run Rscript analysis.R
pixi add r-sf r-terra
```

Prefer `pixi add` for dependencies that should be represented by `pixi.toml` and `pixi.lock`. Direct `install.packages()` remains useful for exceptional source installs but is not captured by the Pixi lockfile.

## Local and Remote SSH workflow

The same project layout is used on a workstation and a headless NixOS server:

```text
Positron
  -> local or Remote SSH extension host
  -> project flake
  -> project-pinned Pixi
  -> project-local .pixi runtime
```

For remote work, run `pixi install` on the remote machine so `.pixi/` is created for that host. Commit `flake.lock` and `pixi.lock`; never commit `.pixi/`.

If the project path contains symlinked directory components, tooling that passes the project to `nix develop path:...` should canonicalize the path first (`pwd -P` / `realpath`). Nix rejects `path:` inputs whose intermediate path components are symlinks.

## Inspect available templates

```bash
nix flake show github:YONGHUNI/nix-data-science-templates
```

The default template is `python-pixi`:

```bash
nix flake init -t github:YONGHUNI/nix-data-science-templates
```

See each template's README for language-specific details.
