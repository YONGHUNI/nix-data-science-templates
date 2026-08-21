# Pure Nix R

R and project R packages are provided directly by Nix.

```bash
nix develop
R
```

Add R packages in `flake.nix` using `rPackages.<package>`, then run `nix develop` again. Commit both `flake.nix` and the generated `flake.lock`.

This template favors Nix-level reproducibility over standard `renv` portability.
