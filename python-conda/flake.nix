{
  description = "Python data science environment with Nix-provided micromamba";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";

  outputs = { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};

      # nixpkgs currently wraps mamba-cpp, which makes micromamba's shell hook
      # see the executable as .mamba-wrapped. Build the same package without
      # that wrapper, then let the micromamba package copy the raw binary under
      # the correct micromamba name.
      mambaCppUnwrapped = pkgs.mamba-cpp.overrideAttrs (_: {
        postInstall = "";
      });

      micromambaFixed = pkgs.micromamba.override {
        mamba-cpp = mambaCppUnwrapped;
      };
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = [
          micromambaFixed
        ];

        shellHook = ''
          set -h
          export MAMBA_ROOT_PREFIX="$HOME/.mamba"
          export NIMBA_PROJECT_ROOT="$(pwd -P)"
          export NIMBA_PROJECT_PREFIX="$NIMBA_PROJECT_ROOT/.conda"

          eval "$(micromamba shell hook --shell bash)"
          alias mamba=micromamba

          nimba() {
            local subcommand=""

            if [ "$#" -gt 0 ]; then
              subcommand="$1"
              shift
            fi

            case "$subcommand" in
              ""|help|-h|--help)
                cat <<'EOF'
nimba - project-local micromamba helper

Usage:
  nimba create [ARGS...]       Create ./.conda; with no args, use environment.yml
  nimba activate               Activate ./.conda in the current shell
  nimba install PACKAGES...    Install packages into ./.conda
  nimba run COMMAND [ARGS...]  Run a command inside ./.conda without activating it
  nimba list [ARGS...]         List packages in ./.conda
  nimba status                 Show project environment status

The standard `mamba` command remains available for normal micromamba usage.
EOF
                ;;

              create)
                if [ -d "$NIMBA_PROJECT_PREFIX/conda-meta" ]; then
                  echo "nimba: project environment already exists: $NIMBA_PROJECT_PREFIX" >&2
                  return 1
                fi

                if [ "$#" -eq 0 ]; then
                  if [ ! -f "$NIMBA_PROJECT_ROOT/environment.yml" ]; then
                    echo "nimba: environment.yml not found in $NIMBA_PROJECT_ROOT" >&2
                    return 2
                  fi
                  micromamba create -p "$NIMBA_PROJECT_PREFIX" -f "$NIMBA_PROJECT_ROOT/environment.yml"
                else
                  micromamba create -p "$NIMBA_PROJECT_PREFIX" "$@"
                fi
                ;;

              activate)
                if [ "$#" -ne 0 ]; then
                  echo "Usage: nimba activate" >&2
                  return 2
                fi
                if [ ! -d "$NIMBA_PROJECT_PREFIX/conda-meta" ]; then
                  echo "nimba: project environment does not exist; run 'nimba create' first" >&2
                  return 1
                fi
                micromamba activate "$NIMBA_PROJECT_PREFIX"
                ;;

              install)
                if [ ! -d "$NIMBA_PROJECT_PREFIX/conda-meta" ]; then
                  echo "nimba: project environment does not exist; run 'nimba create' first" >&2
                  return 1
                fi
                if [ "$#" -eq 0 ]; then
                  echo "Usage: nimba install PACKAGES..." >&2
                  return 2
                fi
                micromamba install -p "$NIMBA_PROJECT_PREFIX" "$@"
                ;;

              run)
                if [ ! -d "$NIMBA_PROJECT_PREFIX/conda-meta" ]; then
                  echo "nimba: project environment does not exist; run 'nimba create' first" >&2
                  return 1
                fi
                if [ "$#" -eq 0 ]; then
                  echo "Usage: nimba run COMMAND [ARGS...]" >&2
                  return 2
                fi
                micromamba run -p "$NIMBA_PROJECT_PREFIX" "$@"
                ;;

              list)
                if [ ! -d "$NIMBA_PROJECT_PREFIX/conda-meta" ]; then
                  echo "nimba: project environment does not exist; run 'nimba create' first" >&2
                  return 1
                fi
                micromamba list -p "$NIMBA_PROJECT_PREFIX" "$@"
                ;;

              status)
                if [ "$#" -ne 0 ]; then
                  echo "Usage: nimba status" >&2
                  return 2
                fi

                echo "Project:      $NIMBA_PROJECT_ROOT"
                echo "Environment:  $NIMBA_PROJECT_PREFIX"

                if [ -d "$NIMBA_PROJECT_PREFIX/conda-meta" ]; then
                  echo "Exists:       yes"
                else
                  echo "Exists:       no"
                fi

                if [ "''${CONDA_PREFIX:-}" = "$NIMBA_PROJECT_PREFIX" ]; then
                  echo "Active:       yes"
                else
                  echo "Active:       no"
                fi

                if [ -x "$NIMBA_PROJECT_PREFIX/bin/python" ]; then
                  echo "Interpreter:  $NIMBA_PROJECT_PREFIX/bin/python"
                  printf "Python:       "
                  "$NIMBA_PROJECT_PREFIX/bin/python" --version 2>&1
                else
                  echo "Interpreter:  not available"
                  echo "Python:       not available"
                fi
                ;;

              *)
                echo "nimba: unknown command: $subcommand" >&2
                echo "Run 'nimba --help' for usage." >&2
                return 2
                ;;
            esac
          }
        '';
      };
    };
}
