{
  description = "Python data science environment with micromamba";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";

  outputs = { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [
          micromamba
        ];

        shellHook = ''
          export MAMBA_ROOT_PREFIX="$HOME/.mamba"
          eval "$(micromamba shell hook --shell bash)"
          alias mamba=micromamba
        '';
      };
    };
}
