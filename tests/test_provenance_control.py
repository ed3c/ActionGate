from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
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
        self.lineage = CHECK.load_json(ROOT / ".provenance/patch-lineage.json")
        self.policy = CHECK.load_json(ROOT / ".provenance/policy.json")

    def valid_upstream(self, relationship: str = "DERIVED_SOURCE") -> dict:
        return {
            "id": "public-upstream",
            "name": "Public Upstream",
            "repository": "https://github.com/public/upstream",
            "commit": "1" * 40,
            "tree": "2" * 40,
            "tag": "v1.0.0",
            "license_spdx": "Apache-2.0",
            "license_sha256": "3" * 64,
            "relationship": relationship,
            "imported_paths": ["src/core"],
            "excluded_paths": ["examples"],
            "observed_at": "2026-08-21T00:00:00Z",
        }

    def admitted_lock(self, relationship: str = "DERIVED_SOURCE") -> dict:
        lock = copy.deepcopy(self.lock)
        lock["state"] = "UPSTREAMS_ADMITTED"
        lock["no_source_imports_admitted"] = False
        lock["upstreams"] = [self.valid_upstream(relationship)]
        return lock

    def mapping(self, **overrides) -> dict:
        value = {
            "upstream_id": "public-upstream",
            "source_path": "src/core/a.cpp",
            "target_path": "vendor/core/a.cpp",
            "source_blob": "4" * 40,
            "import_mode": "MODIFIED_DERIVATIVE",
        }
        value.update(overrides)
        return value

    def lineage_record(self, **overrides) -> dict:
        value = {
            "change_id": "chg-1",
            "target_path": "vendor/core/a.cpp",
            "authorship": "DERIVED_PATCH",
            "upstream_id": "public-upstream",
            "source_path": "src/core/a.cpp",
            "upstream_blob": "4" * 40,
            "receipt": ".provenance/receipts/clean-room-session-1.json",
        }
        value.update(overrides)
        return value

    def test_current_control_plane_passes(self) -> None:
        self.assertEqual([], CHECK.validate_control(ROOT))

    def test_placeholder_upstream_rejected(self) -> None:
        lock = self.admitted_lock()
        lock["upstreams"][0]["repository"] = "https://example.invalid/<UPSTREAM>"
        self.assertTrue(any("repository" in error for error in CHECK.validate_lock(lock)))

    def test_private_or_local_repository_locator_rejected(self) -> None:
        lock = self.admitted_lock()
        lock["upstreams"][0]["repository"] = "https://" + "company" + ".internal/repo"
        self.assertTrue(any("repository" in error for error in CHECK.validate_lock(lock)))

    def test_unknown_root_field_rejected(self) -> None:
        lock = self.admitted_lock()
        lock["legal_clearance"] = True
        self.assertTrue(any("unknown keys" in error for error in CHECK.validate_lock(lock)))

    def test_missing_exact_tree_rejected(self) -> None:
        lock = self.admitted_lock()
        lock["upstreams"][0]["tree"] = "unknown"
        self.assertTrue(any(".tree" in error for error in CHECK.validate_lock(lock)))

    def test_unknown_license_rejected(self) -> None:
        lock = self.admitted_lock()
        lock["upstreams"][0]["license_spdx"] = "UNKNOWN"
        self.assertTrue(any("license_spdx" in error for error in CHECK.validate_lock(lock)))

    def test_invalid_observation_timestamp_rejected(self) -> None:
        lock = self.admitted_lock()
        lock["upstreams"][0]["observed_at"] = "2026-08-21"
        self.assertTrue(any("observed_at" in error for error in CHECK.validate_lock(lock)))

    def test_windows_or_parent_path_rejected(self) -> None:
        self.assertFalse(CHECK.relative_path_is_safe(r"..\private\source.cpp"))
        self.assertFalse(CHECK.relative_path_is_safe("../private/source.cpp"))
        self.assertFalse(CHECK.relative_path_is_safe("src//a.cpp"))

    def test_duplicate_and_nested_boundaries_rejected(self) -> None:
        lock = self.admitted_lock()
        lock["upstreams"][0]["imported_paths"] = ["src/core", "src/core", "src/core/sub"]
        errors = CHECK.validate_lock(lock)
        self.assertTrue(any("duplicates" in error for error in errors))
        self.assertTrue(any("overlapping" in error for error in errors))

    def test_import_without_upstream_rejected(self) -> None:
        imports = copy.deepcopy(self.imports)
        imports["state"] = "IMPORTS_CLASSIFIED"
        imports["mappings"] = [self.mapping(upstream_id="missing")]
        self.assertTrue(any(
            "unadmitted upstream" in error
            for error in CHECK.validate_imports(imports, self.lock)
        ))

    def test_invalid_import_mode_rejected(self) -> None:
        lock = self.admitted_lock()
        imports = {
            "schema": "actiongate-imported-paths/v1",
            "repository": "ed3c/ActionGate",
            "state": "IMPORTS_CLASSIFIED",
            "mappings": [self.mapping(import_mode="COPY_WHATEVER")],
        }
        self.assertTrue(any("import_mode" in error for error in CHECK.validate_imports(imports, lock)))

    def test_generated_from_spec_requires_spec_relationship(self) -> None:
        imports = {
            "schema": "actiongate-imported-paths/v1",
            "repository": "ed3c/ActionGate",
            "state": "IMPORTS_CLASSIFIED",
            "mappings": [self.mapping(import_mode="GENERATED_FROM_PUBLIC_SPEC")],
        }
        errors = CHECK.validate_imports(imports, self.admitted_lock("DERIVED_SOURCE"))
        self.assertTrue(any("SPECIFICATION_ONLY" in error for error in errors))

    def test_reference_implementation_cannot_be_copied(self) -> None:
        imports = {
            "schema": "actiongate-imported-paths/v1",
            "repository": "ed3c/ActionGate",
            "state": "IMPORTS_CLASSIFIED",
            "mappings": [self.mapping()],
        }
        errors = CHECK.validate_imports(imports, self.admitted_lock("REFERENCE_IMPLEMENTATION"))
        self.assertTrue(any("DERIVED_SOURCE or DEPENDENCY" in error for error in errors))

    def test_source_outside_admitted_boundary_rejected(self) -> None:
        imports = {
            "schema": "actiongate-imported-paths/v1",
            "repository": "ed3c/ActionGate",
            "state": "IMPORTS_CLASSIFIED",
            "mappings": [self.mapping(source_path="other/a.cpp")],
        }
        errors = CHECK.validate_imports(imports, self.admitted_lock())
        self.assertTrue(any("outside" in error for error in errors))

    def test_overlapping_import_targets_rejected(self) -> None:
        lock = self.admitted_lock()
        imports = {
            "schema": "actiongate-imported-paths/v1",
            "repository": "ed3c/ActionGate",
            "state": "IMPORTS_CLASSIFIED",
            "mappings": [
                self.mapping(target_path="vendor/core"),
                self.mapping(
                    source_path="src/core/b.cpp",
                    target_path="vendor/core/sub",
                    source_blob="5" * 40,
                ),
            ],
        }
        self.assertTrue(any(
            "overlapping" in error
            for error in CHECK.validate_imports(imports, lock)
        ))

    def test_nonexistent_import_target_rejected_when_root_is_bound(self) -> None:
        lock = self.admitted_lock()
        imports = {
            "schema": "actiongate-imported-paths/v1",
            "repository": "ed3c/ActionGate",
            "state": "IMPORTS_CLASSIFIED",
            "mappings": [self.mapping(target_path="vendor/does-not-exist.cpp")],
        }
        self.assertTrue(any(
            "does not exist" in error
            for error in CHECK.validate_imports(imports, lock, ROOT)
        ))

    def test_derived_patch_requires_exact_source_path_and_blob(self) -> None:
        lock = self.admitted_lock()
        lineage = {
            "schema": "actiongate-patch-lineage/v1",
            "repository": "ed3c/ActionGate",
            "state": "PATCHES_RECORDED",
            "records": [self.lineage_record(source_path=None, upstream_blob=None)],
        }
        errors = CHECK.validate_patch_lineage(lineage, lock)
        self.assertTrue(any("source_path" in error for error in errors))
        self.assertTrue(any("upstream blob" in error for error in errors))

    def test_original_patch_cannot_claim_upstream_source(self) -> None:
        lineage = {
            "schema": "actiongate-patch-lineage/v1",
            "repository": "ed3c/ActionGate",
            "state": "PATCHES_RECORDED",
            "records": [self.lineage_record(authorship="ORIGINAL_PATCH")],
        }
        self.assertTrue(any(
            "must not claim" in error
            for error in CHECK.validate_patch_lineage(lineage, self.admitted_lock())
        ))

    def test_generated_from_spec_lineage_requires_spec_relationship(self) -> None:
        lineage = {
            "schema": "actiongate-patch-lineage/v1",
            "repository": "ed3c/ActionGate",
            "state": "PATCHES_RECORDED",
            "records": [self.lineage_record(authorship="GENERATED_FROM_PUBLIC_SPEC")],
        }
        errors = CHECK.validate_patch_lineage(lineage, self.admitted_lock())
        self.assertTrue(any("SPECIFICATION_ONLY" in error for error in errors))

    def test_imported_target_requires_matching_lineage(self) -> None:
        imports = {
            "schema": "actiongate-imported-paths/v1",
            "repository": "ed3c/ActionGate",
            "state": "IMPORTS_CLASSIFIED",
            "mappings": [self.mapping()],
        }
        lineage = {
            "schema": "actiongate-patch-lineage/v1",
            "repository": "ed3c/ActionGate",
            "state": "PATCHES_RECORDED",
            "records": [self.lineage_record(target_path="vendor/core/other.cpp")],
        }
        errors = CHECK.validate_patch_lineage(lineage, self.admitted_lock(), imports)
        self.assertTrue(any("lacks patch-lineage" in error for error in errors))

    def test_release_cannot_precede_human_legal_admission(self) -> None:
        lock = self.admitted_lock()
        lock["release_state"] = "RELEASE_ELIGIBLE"
        lock["legal_admission"] = "HUMAN_ADMIT_REQUIRED"
        self.assertTrue(any(
            "Human legal admission" in error for error in CHECK.validate_lock(lock)
        ))

    def test_human_legal_admission_requires_complete_redacted_review(self) -> None:
        receipt = {
            "schema": "outside-project-review-receipt/v1",
            "review_id": "ip-1",
            "repository": "ed3c/ActionGate",
            "subject_sha": "1" * 40,
            "subject_tree": "2" * 40,
            "reviewed_at": "2026-08-21T00:00:00Z",
            "employment_agreement_reviewed": False,
            "invention_assignment_reviewed": False,
            "confidentiality_reviewed": False,
            "moonlighting_conflict_reviewed": False,
            "public_upstream_only": False,
            "employer_resources_used": False,
            "employer_confidential_material_used": False,
            "business_overlap_state": "UNRESOLVED",
            "written_notice_state": "NOT_REVIEWED",
            "counsel_state": "NOT_REVIEWED",
            "legal_admission": "HUMAN_ADMITTED",
            "private_urls_echoed": False,
        }
        errors = CHECK.validate_outside_review(receipt, "1" * 40, "2" * 40)
        self.assertTrue(any("requires" in error for error in errors))

    def test_independent_admission_requires_all_falsifiers_pass(self) -> None:
        receipt = {
            "schema": "independent-provenance-review-receipt/v1",
            "review_id": "review-1",
            "repository": "ed3c/ActionGate",
            "subject_sha": "1" * 40,
            "subject_tree": "2" * 40,
            "reviewed_at": "2026-08-21T00:00:00Z",
            "reviewer_kind": "INDEPENDENT_EXTERNAL_AGENT",
            "builder_participation": False,
            "read_only": True,
            "changed_path_denominator": 1,
            "upstream_lock_sha256": "3" * 64,
            "imported_paths_sha256": "4" * 64,
            "patch_lineage_sha256": "5" * 64,
            "sbom_sha256": None,
            "verdict": "ADMIT_STATIC_PROVENANCE",
            "falsifiers": [{"id": "f-1", "state": "NOT_EXERCISED", "detail": "not run"}],
            "private_urls_echoed": False,
            "dissent": [],
            "evidence_ceiling": "STATIC_PROVENANCE_CONTROL_ONLY",
        }
        errors = CHECK.validate_independent_review(receipt, "1" * 40, "2" * 40)
        self.assertTrue(any("every falsifier PASS" in error for error in errors))

    def test_private_url_detected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "leak.md").write_text(
                self.policy["forbidden_public_substrings"][0] + "private-id",
                encoding="utf-8",
            )
            errors = CHECK.scan_private_material(root, self.policy)
            self.assertTrue(any("leak.md" in error for error in errors))

    def test_queue_requires_exactly_one_active_item(self) -> None:
        queue = CHECK.load_json(ROOT / ".provenance/local-handoff-queue.json")
        queue["items"][1]["state"] = "ACTIVE_EXECUTION"
        self.assertTrue(any(
            "exactly one active" in error for error in CHECK.validate_queue(queue)
        ))

    def test_same_source_boundary_in_different_upstreams_is_allowed(self) -> None:
        lock = self.admitted_lock()
        second = self.valid_upstream()
        second["id"] = "other-upstream"
        second["repository"] = "https://github.com/public/other-upstream"
        second["commit"] = "7" * 40
        second["tree"] = "8" * 40
        second["license_sha256"] = "9" * 64
        lock["upstreams"].append(second)
        self.assertFalse(any(
            "overlapping upstream imported boundaries" in error
            for error in CHECK.validate_lock(lock)
        ))

    def test_non_original_patch_requires_import_mapping(self) -> None:
        lineage = {
            "schema": "actiongate-patch-lineage/v1",
            "repository": "ed3c/ActionGate",
            "state": "PATCHES_RECORDED",
            "records": [self.lineage_record()],
        }
        imports = {
            "schema": "actiongate-imported-paths/v1",
            "repository": "ed3c/ActionGate",
            "state": "NO_IMPORTS_ADMITTED",
            "mappings": [],
        }
        errors = CHECK.validate_patch_lineage(
            lineage, self.admitted_lock(), imports
        )
        self.assertTrue(any("lacks imported-path mapping" in error for error in errors))

    def test_queue_unknown_authority_field_rejected(self) -> None:
        queue = CHECK.load_json(ROOT / ".provenance/local-handoff-queue.json")
        queue["items"][0]["auto_merge"] = True
        self.assertTrue(any(
            "unknown keys" in error for error in CHECK.validate_queue(queue)
        ))

    def test_policy_scan_exclusions_are_fail_closed(self) -> None:
        policy = copy.deepcopy(self.policy)
        policy["private_scan_exclusions"].append("tests/test_provenance_control.py")
        self.assertTrue(any(
            "scan exclusions" in error for error in CHECK.validate_policy(policy)
        ))

    def test_source_bearing_commit_without_dco_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
            (root / ".provenance").mkdir()
            for name in ("upstreams.lock.json", "imported-paths.json", "policy.json"):
                source = ROOT / ".provenance" / name
                (root / ".provenance" / name).write_bytes(source.read_bytes())
            (root / "README.md").write_text("base\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "base"], cwd=root, check=True, capture_output=True)
            base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
            (root / "contracts").mkdir()
            (root / "contracts" / "demo.txt").write_text("source\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "add source"], cwd=root, check=True, capture_output=True)
            head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
            errors = CHECK.check_commits(root, base, head)
            self.assertTrue(any("lacks a real DCO" in error for error in errors))

    def test_deleted_private_locator_remains_rejected_in_history(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
            (root / ".provenance").mkdir()
            (root / ".provenance" / "policy.json").write_bytes(
                (ROOT / ".provenance" / "policy.json").read_bytes()
            )
            (root / ".provenance" / "upstreams.lock.json").write_bytes(
                (ROOT / ".provenance" / "upstreams.lock.json").read_bytes()
            )
            (root / ".provenance" / "imported-paths.json").write_bytes(
                (ROOT / ".provenance" / "imported-paths.json").read_bytes()
            )
            (root / "README.md").write_text("base\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "base"], cwd=root, check=True, capture_output=True)
            base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
            forbidden = self.policy["forbidden_public_substrings"][0] + "history-id"
            (root / "ephemeral.md").write_text(forbidden, encoding="utf-8")
            subprocess.run(["git", "add", "ephemeral.md"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "add then remove leak"], cwd=root, check=True, capture_output=True)
            (root / "ephemeral.md").unlink()
            subprocess.run(["git", "add", "-u"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "remove leak"], cwd=root, check=True, capture_output=True)
            head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
            errors = CHECK.check_commits(root, base, head)
            self.assertTrue(any("forbidden public substring persisted" in error for error in errors))

    def test_fake_spdx_sbom_rejected(self) -> None:
        sbom = {
            "spdxVersion": "SPDX-2.3",
            "dataLicense": "CC0-1.0",
            "SPDXID": "SPDXRef-DOCUMENT",
            "documentNamespace": "https://example.invalid/<NAMESPACE>",
            "documentDescribes": [],
            "packages": [],
        }
        errors = CHECK.validate_spdx_sbom(sbom)
        self.assertTrue(any("Namespace" in error or "namespace" in error for error in errors))
        self.assertTrue(any("non-empty" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
