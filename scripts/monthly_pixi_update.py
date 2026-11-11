#!/usr/bin/env python3
"""Propose only newer Pixi versions available from Nix binary substitutes.

This script is designed for a monthly GitHub Actions run on x86_64-linux.
It deliberately does not update any generated project's flake.lock or pixi.lock.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ("python-pixi", "python-pixi-sapelo2", "r-pixi")
CHANNELS = ("nixpkgs-unstable", "nixos-unstable")
PIN_RE = re.compile(r'inputs\.nixpkgs-pixi\.url\s*=\s*"github:NixOS/nixpkgs/([^"]+)";')
SHA_RE = re.compile(r"[0-9a-f]{40}\Z")


def get_pin(source: str) -> str:
    matches = list(PIN_RE.finditer(source))
    if len(matches) != 1:
        raise ValueError("Expected exactly one nixpkgs-pixi input in the flake")
    return matches[0].group(1)


def replace_pin(source: str, new_sha: str) -> str:
    if not SHA_RE.fullmatch(new_sha):
        raise ValueError("The replacement must be a full 40-character commit SHA")
    matches = list(PIN_RE.finditer(source))
    if len(matches) != 1:
        raise ValueError("Expected exactly one nixpkgs-pixi input in the flake")
    match = matches[0]
    return source[: match.start(1)] + new_sha + source[match.end(1) :]


def version_key(version: str) -> tuple[int, ...]:
    if not re.fullmatch(r"\d+(?:\.\d+){2,3}", version):
        raise ValueError(f"Unexpected Pixi version: {version!r}")
    return tuple(int(part) for part in version.split("."))


def current_pin() -> str:
    pins = {
        get_pin((ROOT / template / "flake.nix").read_text())
        for template in TEMPLATES
    }
    if len(pins) != 1:
        raise ValueError(f"Pixi templates are pinned inconsistently: {pins}")
    (pin,) = pins
    if not SHA_RE.fullmatch(pin):
        raise ValueError("Templates must use a verified full commit SHA, not a moving branch")
    return pin


def github_branch_sha(branch: str) -> str:
    url = f"https://api.github.com/repos/NixOS/nixpkgs/branches/{branch}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "nix-data-science-templates-pixi-update",
    }
    token = os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(url, headers=headers), timeout=45) as response:
        sha = json.load(response)["commit"]["sha"]
    if not SHA_RE.fullmatch(sha):
        raise ValueError(f"Unexpected GitHub revision for {branch}: {sha}")
    return sha


def nix_command(work_dir: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["nix", *args], cwd=work_dir, check=True,
        capture_output=True, text=True, timeout=900
    )


def override_args(revision: str | None) -> list[str]:
    if revision is None:
        return []
    return ["--override-input", "nixpkgs-pixi", f"github:NixOS/nixpkgs/{revision}"]


def evaluate_pixi_version(work_dir: Path, revision: str | None = None) -> str:
    return nix_command(
        work_dir,
        ["eval", "--raw", ".#packages.x86_64-linux.pixi.version", *override_args(revision)],
    ).stdout.strip()


def has_binary_substitute(work_dir: Path, revision: str) -> bool:
    # No compilation on the GitHub runner. Using a fresh hosted runner with
    # cache.nixos.org makes this a practical binary-substitute availability check.
    try:
        nix_command(
            work_dir,
            ["build", "--no-link", "--option", "max-jobs", "0",
             ".#pixi", *override_args(revision)],
        )
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        print(f"Cache-only build failed for {revision[:12]}: {exc}", flush=True)
        if isinstance(exc, subprocess.CalledProcessError):
            print((exc.stderr or "")[-2500:], flush=True)
        return False


def write_output(**values: str) -> None:
    output_file = os.environ.get("GITHUB_OUTPUT")
    if output_file:
        with open(output_file, "a", encoding="utf-8") as fh:
            for key, value in values.items():
                fh.write(f"{key}={value}\n")


def main() -> None:
    write_output(updated="false")
    old_sha = current_pin()
    with tempfile.TemporaryDirectory(prefix="monthly-pixi-") as directory:
        work_dir = Path(directory) / "python-pixi"
        shutil.copytree(ROOT / "python-pixi", work_dir)
        old_version = evaluate_pixi_version(work_dir)
        print(f"Current Pixi: {old_version} at {old_sha}", flush=True)

        candidates: list[tuple[tuple[int, ...], str, str, str]] = []
        for channel in CHANNELS:
            sha = github_branch_sha(channel)
            if sha == old_sha:
                continue
            version = evaluate_pixi_version(work_dir, sha)
            print(f"Candidate {channel}: Pixi {version}, {sha}", flush=True)
            if version_key(version) > version_key(old_version):
                candidates.append((version_key(version), channel, sha, version))

        # Newest Pixi first; prefer the general Linux channel for ties.
        candidates.sort(
            key=lambda candidate: (
                candidate[0], candidate[1] == "nixpkgs-unstable"
            ), reverse=True
        )
        for _, channel, sha, version in candidates:
            if not has_binary_substitute(work_dir, sha):
                continue

            # Never change one template without changing all three.
            updates = {}
            for template in TEMPLATES:
                path = ROOT / template / "flake.nix"
                updates[path] = replace_pin(path.read_text(), sha)
            for path, contents in updates.items():
                path.write_text(contents)

            print(f"Selected {channel}: Pixi {version} ({sha})", flush=True)
            write_output(
                updated="true", pixi_version=version,
                nixpkgs_revision=sha, channel=channel
            )
            return

    print("No newer Pixi with a verified binary substitute. Keeping existing pin.")


if __name__ == "__main__":
    main()
