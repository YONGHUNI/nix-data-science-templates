"""Offline structural regression tests for the monthly Pixi pin updater."""
import re
import sys
from pathlib import Path
import unittest
from unittest.mock import patch, call
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import monthly_pixi_update as updater  # noqa: E402
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


    def test_falls_back_to_next_newer_cached_version(self):
        original_sha = "a" * 40
        fallback_sha = "b" * 40
        newest_sha = "c" * 40
        with TemporaryDirectory() as directory:
            fake_root = Path(directory)
            for template in TEMPLATES:
                folder = fake_root / template
                folder.mkdir()
                (folder / "flake.nix").write_text(
                    f'inputs.nixpkgs-pixi.url = "github:NixOS/nixpkgs/{original_sha}";\n'
                )
            revisions = {
                "nixpkgs-unstable": newest_sha,
                "nixos-unstable": fallback_sha,
            }

            def fake_version(_work_dir, revision=None):
                return {
                    None: "0.82.1",
                    newest_sha: "0.84.0",
                    fallback_sha: "0.83.0",
                }[revision]

            def cache_available(_work_dir, revision):
                return revision == fallback_sha

            with (
                patch.object(updater, "ROOT", fake_root),
                patch.object(updater, "github_branch_sha", side_effect=revisions.get),
                patch.object(updater, "evaluate_pixi_version", side_effect=fake_version),
                patch.object(updater, "has_binary_substitute", side_effect=cache_available) as cache,
                patch.object(updater, "write_output") as output,
            ):
                updater.main()
            self.assertEqual(
                cache.call_args_list,
                [call(unittest.mock.ANY, newest_sha), call(unittest.mock.ANY, fallback_sha)],
            )
            output.assert_any_call(
                updated="true", pixi_version="0.83.0",
                nixpkgs_revision=fallback_sha, channel="nixos-unstable",
            )
            for template in TEMPLATES:
                self.assertEqual(
                    get_pin((fake_root / template / "flake.nix").read_text()),
                    fallback_sha,
                )

    def test_no_cached_upgrade_leaves_all_templates_untouched(self):
        original_sha = "a" * 40
        with TemporaryDirectory() as directory:
            fake_root = Path(directory)
            for template in TEMPLATES:
                folder = fake_root / template
                folder.mkdir()
                (folder / "flake.nix").write_text(
                    f'inputs.nixpkgs-pixi.url = "github:NixOS/nixpkgs/{original_sha}";\n'
                )

            with (
                patch.object(updater, "ROOT", fake_root),
                patch.object(updater, "github_branch_sha", side_effect=["b" * 40, "c" * 40]),
                patch.object(updater, "evaluate_pixi_version", side_effect=lambda _d, r=None: "0.82.1" if r is None else "0.83.0"),
                patch.object(updater, "has_binary_substitute", return_value=False),
                patch.object(updater, "write_output") as output,
            ):
                updater.main()
            output.assert_called_once_with(updated="false")
            for template in TEMPLATES:
                self.assertEqual(
                    get_pin((fake_root / template / "flake.nix").read_text()),
                    original_sha,
                )


    def test_workflows_pin_actions_and_have_no_unresolved_placeholders(self):
        for name in ("pixi-monthly-update.yml", "pixi-templates-ci.yml"):
            workflow = (ROOT / ".github" / "workflows" / name).read_text()
            self.assertNotRegex(workflow, r"__[A-Z_]+__")
            actions = re.findall(
                r"^\s*uses:\s*([\w./-]+)@([0-9a-f]{40})\b",
                workflow, flags=re.MULTILINE,
            )
            self.assertGreaterEqual(len(actions), 2, name)
            self.assertEqual(workflow.count("uses:"), len(actions), name)

        monthly = (
            ROOT / ".github" / "workflows" / "pixi-monthly-update.yml"
        ).read_text()
        self.assertIn("schedule:", monthly)
        self.assertIn("workflow_dispatch:", monthly)
        self.assertIn("steps.candidate.outputs.pixi_version", monthly)
        self.assertIn("peter-evans/create-pull-request@", monthly)

if __name__ == "__main__":
    unittest.main()
