from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import build_release_bundles


class ReleaseBundleBuilderTests(unittest.TestCase):
    def test_release_bundle_count(self) -> None:
        bundles = build_release_bundles.build_release_bundles()
        self.assertEqual(len(bundles), 3)

    def test_release_readmes_exist(self) -> None:
        for bundle in build_release_bundles.build_release_bundles():
            readme_path = build_release_bundles.RELEASE_READMES_DIR / bundle.readme_source
            self.assertTrue(readme_path.is_file(), readme_path)

    def test_release_sources_exist(self) -> None:
        for bundle in build_release_bundles.build_release_bundles():
            for rel_path_str in bundle.included_files:
                src = REPO_ROOT / rel_path_str
                self.assertTrue(src.is_file(), src)


if __name__ == "__main__":
    unittest.main()
