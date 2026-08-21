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
          export MAMBA_PROJECT_PREFIX="$PWD/.conda"
          eval "$(micromamba shell hook --shell bash)"
          alias mamba=micromamba

          mamba-project() {
            micromamba create -p "$MAMBA_PROJECT_PREFIX" "$@"
          }
        '';
      };
    };
}
