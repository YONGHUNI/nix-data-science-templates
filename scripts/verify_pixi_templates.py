#!/usr/bin/env python3
"""Check all Pixi templates without compiling Pixi from source."""
from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import tempfile

from monthly_pixi_update import ROOT, TEMPLATES, current_pin


def run(work_dir: Path, *args: str) -> str:
    result = subprocess.run(
        ["nix", *args], cwd=work_dir, text=True, capture_output=True,
        check=True, timeout=900,
    )
    return result.stdout.strip()


def main() -> None:
    pinned_sha = current_pin()
    print(f"All templates pin nixpkgs-pixi at {pinned_sha}", flush=True)

    versions: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="verify-pixi-templates-") as temp:
        for template in TEMPLATES:
            work_dir = Path(temp) / template
            shutil.copytree(ROOT / template, work_dir)

            version = run(work_dir, "eval", "--raw", ".#packages.x86_64-linux.pixi.version")
            run(work_dir, "eval", "--raw", ".#devShells.x86_64-linux.default.drvPath")
            versions[template] = version
            print(f"{template}: Pixi {version}; flake and devShell evaluate", flush=True)

            if template == "python-pixi":
                run(work_dir, "build", "--no-link", "--option", "max-jobs", "0", ".#pixi")

            # Sapelo2's shellHook requires /lscratch, unavailable on GitHub runners.
            # Its Nix evaluation is checked here; runtime testing requires Sapelo2.
            if template != "python-pixi-sapelo2":
                observed = run(
                    work_dir, "develop", "--option", "max-jobs", "0",
                    "--command", "pixi", "--version",
                )
                if observed != f"pixi {version}":
                    raise AssertionError(f"{template}: unexpected Pixi output {observed!r}")
                print(f"{template}: nix develop / pixi --version OK", flush=True)

    if len(set(versions.values())) != 1:
        raise AssertionError(f"Pixi versions differ across templates: {versions}")
    print("Verified: no Pixi source compilation and no repository lockfile edits.", flush=True)


if __name__ == "__main__":
    main()
