# R + renv

Nix provides R and build tools; `renv` manages project R packages.

```bash
nix develop
R -q -e 'renv::init()'
```

Use R normally, then record the project package state with:

```r
renv::snapshot()
```

Commit `renv.lock` and the generated `renv/activate.R` metadata, but not `renv/library/`.

This template favors compatibility with standard R workflows while keeping the system/toolchain layer in Nix.
