{
  description = "Pure Nix Python data science environment";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";

  outputs = { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      python = pkgs.python312.withPackages (ps: with ps; [
        ipykernel
        numpy
        pandas
        scipy
        matplotlib
      ]);
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = [ python ];
      };
    };
}
