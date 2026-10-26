# XeLaTeX + Nix + Positron

Reusable LaTeX project with a pinned Nix development environment, XeLaTeX/latexmk, `tex-fmt`, LaTeX Workshop settings, SyncTeX, and build/clean tasks. No Python/Pixi required.

## Initialize

```bash
mkdir my-latex-project && cd my-latex-project
nix flake init -t github:YONGHUNI/nix-data-science-templates#latex-nix
nix develop --command latexmk -synctex=1 -xelatex -pdfxe main.tex
```

Commit the generated `flake.lock`; it pins the same Nixpkgs revision as the template's initial `flake.lock`. On NixOS, open the project in Positron from a normal terminal rather than an unrelated project's Nix shell.

## Positron

Install LaTeX Workshop. Open `main.tex` and use its Build command to invoke `nix develop --command latexmk`, or use `Ctrl+Shift+B` to run the default build task. The internal PDF viewer supports double-click inverse SyncTeX; source-to-PDF synchronization works with the generated `.synctex.gz`.

Manual formatting (typically `Shift+Alt+F`) uses `tex-fmt` through Nix. Format-on-save is disabled to avoid unexpected whole-document edits.

## CLI

```bash
nix develop --command latexmk -synctex=1 -xelatex -pdfxe main.tex
nix develop --command latexmk -c main.tex
```

If renaming `main.tex`, update the filename in `.vscode/tasks.json`. The LaTeX Workshop recipe uses `%DOC%` and follows the active root document. Do not add a `% !TEX TS-program` magic comment, which can override the configured recipe.

Intermediate build files, including `.synctex.gz`, are ignored by Git but remain available locally for editor navigation. The template does not include GitHub Pages deployment; project-specific publishing can be added separately.

This preset is adapted from the validated `YONGHUNI/curriculum-vitae` XeLaTeX workflow; the reusable `main.tex` is a minimal generic example.
