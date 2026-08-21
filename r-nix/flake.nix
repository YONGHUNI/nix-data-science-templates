{
  description = "Pure Nix R data science environment";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";

  outputs = { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [
          R
          rPackages.data_table
          rPackages.ggplot2
          rPackages.dplyr
          rPackages.tidyr
          rPackages.sf
          rPackages.terra
        ];
      };
    };
}
