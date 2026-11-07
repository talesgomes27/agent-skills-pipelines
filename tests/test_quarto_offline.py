"""Filesystem-only discovery must not execute binaries that may access the network."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
from unittest.mock import patch
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'quarto-expert/scripts/offline_probe.py'


class OfflineProbeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.prefix = self.root / 'install'
        (self.prefix / 'bin').mkdir(parents=True)
        (self.prefix / 'share').mkdir()
        self.marker = self.root / 'executed'
        self.quarto = self.prefix / 'bin' / ('quarto.exe' if os.name == 'nt' else 'quarto')
        self.quarto.write_text('#!' + sys.executable + '\nfrom pathlib import Path\nPath(' + repr(str(self.marker)) + ').write_text("executed")\n', encoding='utf-8')
        self.quarto.chmod(0o755)
        self.version = self.prefix / 'share/version'
        self.version.write_text('1.10.19', encoding='utf-8')

    def load(self):
        spec = importlib.util.spec_from_file_location('offline_probe', SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_discovery_reads_version_without_running_quarto(self):
        data = self.load().inventory(str(self.quarto))
        self.assertEqual(data['quarto']['version'], '1.10.19')
        self.assertEqual(data['mode'], 'filesystem-only')
        self.assertFalse(data['execution_verified'])
        self.assertFalse(self.marker.exists())

    def test_missing_explicit_binary_does_not_fall_back_to_host(self):
        data = self.load().inventory(str(self.root / 'missing'))
        self.assertIsNone(data['quarto']['path'])
        self.assertIsNone(data['quarto']['version'])

    def test_bad_version_is_unknown_not_a_runtime_success(self):
        self.version.write_text('not version metadata', encoding='utf-8')
        self.assertIsNone(self.load().inventory(str(self.quarto))['quarto']['version'])

    def test_version_symlink_outside_prefix_is_not_read(self):
        outside = self.root / 'outside-version'
        outside.write_text('9.9.9', encoding='utf-8')
        self.version.unlink()
        self.version.symlink_to(outside)
        self.assertIsNone(self.load().inventory(str(self.quarto))['quarto']['version'])

    def test_cli_reports_missing_binary_as_unperformed(self):
        result = subprocess.run([sys.executable, '-B', str(SCRIPT), '--quarto', str(self.root / 'missing')], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(json.loads(result.stdout)['execution_verified'])

    def test_oversized_metadata_does_not_invent_a_truncated_version(self):
        self.version.write_text('1.2.3+' + 'x' * 200, encoding='utf-8')
        data = self.load().inventory(str(self.quarto))
        self.assertIsNone(data['quarto']['version'])
        self.assertFalse(data['render_verified'])

    def bundle_inventory(self, module):
        original = module.shutil.which
        with patch.object(module.shutil, 'which', side_effect=lambda name: original(name) if name == str(self.quarto) else None):
            with patch.object(module.os, 'uname', return_value=SimpleNamespace(machine='x86_64'), create=True):
                return module.inventory(str(self.quarto))

    def test_bundled_typst_is_found_without_executing_it(self):
        candidate = self.prefix / 'bin/tools/x86_64/typst'
        candidate.parent.mkdir(parents=True)
        candidate.write_text('not an executed program', encoding='utf-8')
        candidate.chmod(0o755)
        data = self.bundle_inventory(self.load())
        self.assertEqual(data['tools']['typst']['path'], str(candidate.resolve()))
        self.assertEqual(data['tools']['typst']['source'], 'bundled-file')
        self.assertFalse(data['execution_verified'])

    def test_bundled_symlink_outside_installation_is_not_announced(self):
        candidate = self.prefix / 'bin/tools/x86_64/typst'
        candidate.parent.mkdir(parents=True)
        outside = self.root / 'external-typst'
        outside.write_text('outside', encoding='utf-8')
        outside.chmod(0o755)
        candidate.symlink_to(outside)
        self.assertIsNone(self.bundle_inventory(self.load())['tools']['typst']['path'])

    def test_other_architecture_is_not_claimed_available(self):
        candidate = self.prefix / 'bin/tools/aarch64/typst'
        candidate.parent.mkdir(parents=True)
        candidate.write_text('other architecture', encoding='utf-8')
        candidate.chmod(0o755)
        self.assertIsNone(self.bundle_inventory(self.load())['tools']['typst']['path'])
