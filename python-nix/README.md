# Pure Nix Python

Python and project packages are provided directly by Nix.

```bash
nix develop
python --version
```

Add Python packages in `flake.nix` under `python312.withPackages`, then run `nix develop` again. Commit both `flake.nix` and the generated `flake.lock`.

This template favors Nix-level reproducibility over Conda ecosystem compatibility.
