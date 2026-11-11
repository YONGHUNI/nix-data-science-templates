"""Offline structural regression tests for the monthly Pixi pin updater."""
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from monthly_pixi_update import (  # noqa: E402
    TEMPLATES, current_pin, get_pin, replace_pin, version_key,
)


class PixiUpdateTests(unittest.TestCase):
    def test_template_pins_are_identical_and_immutable(self):
        pin = current_pin()
        self.assertEqual(len(pin), 40)
        for template in TEMPLATES:
            self.assertEqual(
                get_pin((ROOT / template / "flake.nix").read_text()), pin
            )

    def test_template_lockfiles_are_not_committed(self):
        for template in TEMPLATES:
            self.assertFalse((ROOT / template / "flake.lock").exists())

    def test_replace_only_pixi_input(self):
        source = (
            '{\n'
            '  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";\n'
            '  inputs.nixpkgs-pixi.url = "github:NixOS/nixpkgs/' + "a" * 40 + '";\n'
            '}\n'
        )
        updated = replace_pin(source, "b" * 40)
        self.assertIn('nixos-26.05', updated)
        self.assertIn("b" * 40, updated)
        self.assertNotIn("a" * 40, updated)

    def test_multiple_inputs_or_moving_refs_rejected(self):
        entry = 'inputs.nixpkgs-pixi.url = "github:NixOS/nixpkgs/nixos-unstable";'
        with self.assertRaises(ValueError):
            get_pin(entry + "\n" + entry)
        with self.assertRaises(ValueError):
            replace_pin(entry, "not-a-commit-sha")

    def test_semantic_version_order(self):
        self.assertGreater(version_key("0.83.0"), version_key("0.82.1"))
        self.assertGreater(version_key("0.100.0"), version_key("0.99.0"))
        with self.assertRaises(ValueError):
            version_key("latest")


if __name__ == "__main__":
    unittest.main()
