{
  description = "Reproducible XeLaTeX and tex-fmt environment for Positron";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";

  outputs = { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      tex = pkgs.texlive.combine {
        inherit (pkgs.texlive)
          scheme-medium
          latexmk
          fontspec
          xunicode
          xltxtra
          hyphenat
          datetime2
          tracklang
          etoolbox
          xkeyval;
      };
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = [ tex pkgs.tex-fmt ];
      };
    };
}
