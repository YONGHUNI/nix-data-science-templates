{
  description = "Python data science environment with standalone micromamba";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";

  outputs = { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [
          curl
          gnutar
          bzip2
        ];

        shellHook = ''
          export MAMBA_ROOT_PREFIX="$HOME/.mamba"
          export PATH="$HOME/.local/bin:$PATH"

          if [ -x "$HOME/.local/bin/micromamba" ]; then
            eval "$("$HOME/.local/bin/micromamba" shell hook --shell bash)"
            alias mamba=micromamba
          else
            echo "micromamba not found at $HOME/.local/bin/micromamba"
            echo "See README.md for the one-time installation step."
          fi
        '';
      };
    };
}
