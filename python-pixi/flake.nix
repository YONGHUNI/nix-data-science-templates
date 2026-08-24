{
  description = "Python data science environment with Nix-provided Pixi";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";

  outputs = { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = [
          pkgs.pixi
        ];

        shellHook = ''
          if [ -f /etc/NIXOS ] && [ ! -e /lib64/ld-linux-x86-64.so.2 ]; then
            echo "python-pixi: NixOS needs programs.nix-ld.enable = true for Conda binaries." >&2
          fi
        '';
      };
    };
}
