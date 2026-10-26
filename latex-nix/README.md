# XeLaTeX + Nix

Editor-independent LaTeX project with a pinned Nix development environment, XeLaTeX/latexmk, `tex-fmt`, and SyncTeX. Optional `.vscode/` integration provides LaTeX Workshop recipes and build/clean tasks. No Python/Pixi required.

## Initialize

```bash
mkdir my-latex-project && cd my-latex-project
nix flake init -t github:YONGHUNI/nix-data-science-templates#latex-nix
nix develop --command latexmk -synctex=1 -xelatex -pdfxe main.tex
```

Commit the generated `flake.lock`; it pins the same Nixpkgs revision as the template's initial `flake.lock`. Launch your editor from a normal shell rather than an unrelated project's Nix shell if you want to avoid inheriting another project's environment.

## Optional VS Code-compatible editor integration

The included `.vscode/` settings are an **optional convenience**, not a requirement for using the template. In editors supporting VS Code extensions/tasks (including VS Code and Positron), install LaTeX Workshop, open `main.tex`, and use its Build command to invoke `nix develop --command latexmk`, or use `Ctrl+Shift+B` to run the default build task. In the internal PDF viewer, double-click inverse SyncTeX is configured; source-to-PDF synchronization uses the generated `.synctex.gz`. In other editors, use the CLI build commands below and configure SyncTeX with the editor's own PDF viewer if desired.

Manual formatting (typically `Shift+Alt+F` in compatible editors) uses `tex-fmt` through Nix. Format-on-save is disabled to avoid unexpected whole-document edits. For terminal use, invoke `nix develop --command tex-fmt` with options appropriate for your project.

## CLI

```bash
nix develop --command latexmk -synctex=1 -xelatex -pdfxe main.tex
nix develop --command latexmk -c main.tex
```

If renaming `main.tex`, update the filename in `.vscode/tasks.json`. The LaTeX Workshop recipe uses `%DOC%` and follows the active root document. Do not add a `% !TEX TS-program` magic comment, which can override the configured recipe.

Intermediate build files, including `.synctex.gz`, are ignored by Git but remain available locally for editor navigation. The template does not include GitHub Pages deployment; project-specific publishing can be added separately.

This preset is adapted from the validated `YONGHUNI/curriculum-vitae` XeLaTeX workflow; the reusable `main.tex` is a minimal generic example.
