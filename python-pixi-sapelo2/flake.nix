{
  description = "Sapelo2 Python + Pixi using high-speed /lscratch storage";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";
  # Keep the base toolchain stable while selecting an up-to-date Pixi.
  # Updated by the monthly cache-verified Pixi workflow. No flake.lock ships with the template.
  inputs.nixpkgs-pixi.url = "github:NixOS/nixpkgs/4fe25e12eb9f4c744966dd3de5a05246cf098601";

  outputs = { nixpkgs, nixpkgs-pixi, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      pixiPackage = nixpkgs-pixi.legacyPackages.${system}.pixi;
    in
    {
      packages.${system}.pixi = pixiPackage;

      apps.${system}.pixi = {
        type = "app";
        program = "${pixiPackage}/bin/pixi";
      };

      devShells.${system}.default = pkgs.mkShell {
        packages = [
          pkgs.bashInteractive
          pixiPackage
        ];

        shellHook = ''
          # Nixpkgs 26.05 wraps Pixi 0.68.1 with TLS=system, which that
          # Pixi release does not recognize. Preserve explicit webpki/all.
          if ${if pkgs.lib.versionOlder pixiPackage.version "0.69.0" then "true" else "false"}; then
            case "''${PIXI_TLS_ROOT_CERTS:-}" in
              ""|system) export PIXI_TLS_ROOT_CERTS=native ;;
            esac
          elif [ "''${PIXI_TLS_ROOT_CERTS:-}" = native ]; then
            export PIXI_TLS_ROOT_CERTS=system
          fi

          export PIXI_CACHE_DIR="/lscratch/$USER/pixi-cache"

          mkdir -p \
            "$PIXI_CACHE_DIR" \
            "/lscratch/$USER/pixi-envs" \
            ".pixi"

          printf 'detached-environments = "/lscratch/%s/pixi-envs"\n' "$USER" \
            > .pixi/config.toml

          if [ -f /etc/NIXOS ] && [ ! -e /lib64/ld-linux-x86-64.so.2 ]; then
            echo "python-pixi: NixOS needs programs.nix-ld.enable = true for Conda binaries." >&2
          fi
        '';

      };
    };
}
