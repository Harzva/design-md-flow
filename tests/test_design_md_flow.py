import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "design_md_flow.py"


SAMPLE_DESIGN = """---
name: Acme
description: A compact test design system.
---

# Acme DESIGN.md

## Color Palette
Primary: #111827

## Typography
Use Inter for interface text.

## Components
Buttons are square and direct.

## Layout
Use an 8px spacing grid.

## Responsive Behavior
Collapse navigation on small screens.
"""


class DesignMdFlowTests(unittest.TestCase):
    def run_cli(self, *args, cwd=None):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=cwd or ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def make_source(self, root):
        source = Path(root) / "awesome-design-md"
        design_dir = source / "design-md" / "acme"
        design_dir.mkdir(parents=True)
        (design_dir / "DESIGN.md").write_text(SAMPLE_DESIGN, encoding="utf-8")
        return source

    def test_list_local_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = self.make_source(tmp)
            result = self.run_cli("list", "--source", str(source))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("acme", result.stdout)
            self.assertIn("1 styles", result.stdout)

    def test_install_and_verify(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = self.make_source(tmp)
            project = Path(tmp) / "project"
            project.mkdir()

            install = self.run_cli("install", "acme", "--source", str(source), "--project", str(project))
            self.assertEqual(install.returncode, 0, install.stderr)
            self.assertTrue((project / "DESIGN.md").is_file())

            verify = self.run_cli("verify", "--project", str(project))
            self.assertEqual(verify.returncode, 0, verify.stderr)
            self.assertIn("status: ok", verify.stdout)

    def test_install_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = self.make_source(tmp)
            project = Path(tmp) / "project"
            project.mkdir()
            (project / "DESIGN.md").write_text("existing", encoding="utf-8")

            result = self.run_cli("install", "acme", "--source", str(source), "--project", str(project))
            self.assertEqual(result.returncode, 2)
            self.assertIn("already exists", result.stderr)


if __name__ == "__main__":
    unittest.main()
