from __future__ import annotations

import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "provenance_check", ROOT / "scripts/check_provenance_control.py"
)
assert SPEC and SPEC.loader
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


class ProvenanceControlTests(unittest.TestCase):
    def setUp(self) -> None:
        self.lock = CHECK.load_json(ROOT / ".provenance/upstreams.lock.json")
        self.imports = CHECK.load_json(ROOT / ".provenance/imported-paths.json")

    def valid_upstream(self) -> dict:
        return {
            "id": "public-upstream",
            "name": "Public Upstream",
            "repository": "https://github.com/public/upstream",
            "commit": "1" * 40,
            "tree": "2" * 40,
            "tag": "v1.0.0",
            "license_spdx": "Apache-2.0",
            "license_sha256": "3" * 64,
            "relationship": "DERIVED_SOURCE",
            "imported_paths": ["src/core"],
            "excluded_paths": ["examples"],
            "observed_at": "2026-08-21T00:00:00Z",
        }

    def admitted_lock(self) -> dict:
        lock = copy.deepcopy(self.lock)
        lock["state"] = "UPSTREAMS_ADMITTED"
        lock["no_source_imports_admitted"] = False
        lock["upstreams"] = [self.valid_upstream()]
        return lock

    def test_current_control_plane_passes(self) -> None:
        self.assertEqual([], CHECK.validate_control(ROOT))

    def test_placeholder_upstream_rejected(self) -> None:
        lock = self.admitted_lock()
        lock["upstreams"][0]["repository"] = "https://example.invalid/<UPSTREAM>"
        self.assertTrue(any("placeholder" in error for error in CHECK.validate_lock(lock)))

    def test_missing_exact_tree_rejected(self) -> None:
        lock = self.admitted_lock()
        lock["upstreams"][0]["tree"] = "unknown"
        self.assertTrue(any(".tree" in error for error in CHECK.validate_lock(lock)))

    def test_unknown_license_rejected(self) -> None:
        lock = self.admitted_lock()
        lock["upstreams"][0]["license_spdx"] = "UNKNOWN"
        self.assertTrue(any("license_spdx" in error for error in CHECK.validate_lock(lock)))

    def test_import_without_upstream_rejected(self) -> None:
        imports = copy.deepcopy(self.imports)
        imports["state"] = "IMPORTS_CLASSIFIED"
        imports["mappings"] = [{
            "upstream_id": "missing",
            "source_path": "src/a.cpp",
            "target_path": "vendor/a.cpp",
            "source_blob": "4" * 40,
            "import_mode": "MODIFIED_DERIVATIVE",
        }]
        self.assertTrue(any(
            "unadmitted upstream" in error
            for error in CHECK.validate_imports(imports, self.lock)
        ))

    def test_overlapping_import_targets_rejected(self) -> None:
        lock = self.admitted_lock()
        imports = {
            "schema": "actiongate-imported-paths/v1",
            "repository": "ed3c/ActionGate",
            "state": "IMPORTS_CLASSIFIED",
            "mappings": [
                {
                    "upstream_id": "public-upstream",
                    "source_path": "src/a",
                    "target_path": "vendor/core",
                    "source_blob": "4" * 40,
                    "import_mode": "UNCHANGED_IMPORT",
                },
                {
                    "upstream_id": "public-upstream",
                    "source_path": "src/b",
                    "target_path": "vendor/core/sub",
                    "source_blob": "5" * 40,
                    "import_mode": "UNCHANGED_IMPORT",
                },
            ],
        }
        self.assertTrue(any(
            "overlapping" in error
            for error in CHECK.validate_imports(imports, lock)
        ))

    def test_derived_patch_requires_exact_upstream_blob(self) -> None:
        lock = self.admitted_lock()
        lineage = {
            "schema": "actiongate-patch-lineage/v1",
            "repository": "ed3c/ActionGate",
            "state": "PATCHES_RECORDED",
            "records": [{
                "change_id": "chg-1",
                "target_path": "vendor/core/a.cpp",
                "authorship": "DERIVED_PATCH",
                "upstream_id": "public-upstream",
                "upstream_blob": None,
                "receipt": ".provenance/receipts/cr-1.json",
            }],
        }
        self.assertTrue(any(
            "upstream blob" in error
            for error in CHECK.validate_patch_lineage(lineage, lock)
        ))

    def test_release_cannot_precede_human_legal_admission(self) -> None:
        lock = self.admitted_lock()
        lock["release_state"] = "RELEASE_ELIGIBLE"
        lock["legal_admission"] = "HUMAN_ADMIT_REQUIRED"
        self.assertTrue(any(
            "Human legal admission" in error
            for error in CHECK.validate_lock(lock)
        ))

    def test_private_url_detected(self) -> None:
        policy = CHECK.load_json(ROOT / ".provenance/policy.json")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "leak.md").write_text(
                policy["forbidden_public_substrings"][0] + "private-id",
                encoding="utf-8",
            )
            errors = CHECK.scan_private_material(root, policy)
            self.assertTrue(any("leak.md" in error for error in errors))

    def test_original_patch_cannot_claim_upstream_blob(self) -> None:
        lineage = {
            "schema": "actiongate-patch-lineage/v1",
            "repository": "ed3c/ActionGate",
            "state": "PATCHES_RECORDED",
            "records": [{
                "change_id": "chg-2",
                "target_path": "src/new.py",
                "authorship": "ORIGINAL_PATCH",
                "upstream_id": "public-upstream",
                "upstream_blob": "6" * 40,
                "receipt": ".provenance/receipts/cr-2.json",
            }],
        }
        self.assertTrue(any(
            "must not claim" in error
            for error in CHECK.validate_patch_lineage(lineage, self.admitted_lock())
        ))


if __name__ == "__main__":
    unittest.main()
