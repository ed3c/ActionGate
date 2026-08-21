from __future__ import annotations

import json
import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "check_provenance.py"
SPEC = importlib.util.spec_from_file_location("check_provenance", SCRIPT)
guard = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(guard)


class ProvenanceGuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self._write_minimum()

    def tearDown(self):
        self.tmp.cleanup()

    def write_json(self, rel, value):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def _write_minimum(self):
        for rel in guard.REQUIRED_FILES:
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# placeholder\n", encoding="utf-8")
        self.write_json(".provenance/upstreams.lock.json", {
            "schema":"actiongate-upstream-lock/v1",
            "repository":"ed3c/ActionGate",
            "state":"NO_DERIVED_UPSTREAM_ADMITTED",
            "upstreams":[]
        })
        self.write_json(".provenance/imported-paths.json", {
            "schema":"actiongate-imported-paths/v1",
            "repository":"ed3c/ActionGate",
            "state":"NO_IMPORTED_PATHS_ADMITTED",
            "mappings":[]
        })
        self.write_json(".provenance/release-gate.json", {
            "schema":"actiongate-provenance-release-gate/v1",
            "repository":"ed3c/ActionGate",
            "state":"BLOCKED",
            "blockers":["HUMAN_LEGAL_ADMIT_REQUIRED"]
        })
        self.write_json(".provenance/local-handoff-queue.json", {
            "schema":"actiongate-provenance-handoff/v1",
            "active_item":"ABSENT",
            "items":[]
        })
        self.write_json(".provenance/templates/clean-room-session.example.json", {
            "employer_source_accessed":None,
            "employer_resource_used":None,
            "private_material_included":None,
            "legal_admission":"HUMAN_ADMIT_REQUIRED"
        })
        self.write_json(".provenance/templates/outside-project-review.example.json", {
            "private_review_completed":None,
            "employment_agreement_reviewed":None,
            "employer_resources_used":None,
            "employer_confidential_material_used":None,
            "public_upstream_only":None,
            "private_urls_echoed":False
        })
        self.write_json("sbom/actiongate.spdx.json", {
            "spdxVersion":"SPDX-2.3",
            "dataLicense":"CC0-1.0",
            "packages":[{"SPDXID":"SPDXRef-Package-ActionGate"}]
        })

    def errors(self, release=False):
        return guard.validate_repository(self.root, release_gate=release)

    def test_empty_fail_closed_baseline_is_structurally_valid(self):
        self.assertEqual([], self.errors())

    def test_release_gate_stays_red(self):
        self.assertIn("release gate is not admitted", self.errors(release=True))

    def test_unlocked_import_is_rejected(self):
        self.write_json(".provenance/imported-paths.json", {
            "schema":"actiongate-imported-paths/v1",
            "repository":"ed3c/ActionGate",
            "state":"IMPORTED_PATHS_ADMITTED",
            "mappings":[{
                "upstream_id":"missing",
                "upstream_path":"src/a",
                "local_path":"vendor/a",
                "source_blob":"a"*40
            }]
        })
        self.assertTrue(any("unlocked upstream" in error for error in self.errors()))

    def test_derived_upstream_requires_exact_sha(self):
        self.write_json(".provenance/upstreams.lock.json", {
            "schema":"actiongate-upstream-lock/v1",
            "repository":"ed3c/ActionGate",
            "state":"UPSTREAMS_ADMITTED",
            "upstreams":[{
                "id":"up",
                "name":"up",
                "repository":"https://example.invalid/up",
                "commit":"main",
                "tree":"b"*40,
                "relationship":"DERIVED_PUBLIC_UPSTREAM",
                "license_spdx":"Apache-2.0",
                "license_file":"LICENSES/up/LICENSE",
                "license_sha256":"c"*64,
                "sbom_spdx_id":"SPDXRef-Up"
            }]
        })
        self.assertTrue(any("commit must be 40" in error for error in self.errors()))

    def test_license_digest_mismatch_is_rejected(self):
        license_path = self.root / "LICENSES/up/LICENSE"
        license_path.parent.mkdir(parents=True, exist_ok=True)
        license_path.write_text("license bytes", encoding="utf-8")
        self.write_json(".provenance/upstreams.lock.json", {
            "schema":"actiongate-upstream-lock/v1",
            "repository":"ed3c/ActionGate",
            "state":"UPSTREAMS_ADMITTED",
            "upstreams":[{
                "id":"up",
                "name":"up",
                "repository":"https://example.invalid/up",
                "commit":"a"*40,
                "tree":"b"*40,
                "relationship":"DEPENDENCY_ONLY",
                "license_spdx":"Apache-2.0",
                "license_file":"LICENSES/up/LICENSE",
                "license_sha256":"0"*64,
                "sbom_spdx_id":"SPDXRef-Up"
            }]
        })
        sbom = json.loads((self.root/"sbom/actiongate.spdx.json").read_text())
        sbom["packages"].append({"SPDXID":"SPDXRef-Up","versionInfo":"a"*40})
        self.write_json("sbom/actiongate.spdx.json", sbom)
        self.assertTrue(any("license digest mismatch" in error for error in self.errors()))

    def test_private_locator_is_rejected(self):
        private = "https://" + "docs." + "google.com" + "/document/d/" + "private-id"
        (self.root/"PROVENANCE.md").write_text(private, encoding="utf-8")
        self.assertTrue(any("PRIVATE_DOCUMENT_LOCATOR" in error for error in self.errors()))

    def test_secret_shape_is_rejected(self):
        token = "ghp_" + "A"*32
        (self.root/"PROVENANCE.md").write_text(token, encoding="utf-8")
        self.assertTrue(any("GITHUB_TOKEN" in error for error in self.errors()))

    def test_templates_cannot_self_assert_human_facts(self):
        clean = json.loads((self.root/".provenance/templates/clean-room-session.example.json").read_text())
        clean["employer_source_accessed"] = False
        self.write_json(".provenance/templates/clean-room-session.example.json", clean)
        self.assertTrue(any("must not self-assert" in error for error in self.errors()))

    def test_dco_missing_is_rejected(self):
        records = [{"sha":"a"*40,"author":"A","email":"a@example.com","body":"message"}]
        self.assertEqual(["DCO missing: " + "a"*40], guard.validate_dco_records(records))

    def test_dco_email_must_match_author(self):
        records = [{
            "sha":"a"*40,
            "author":"A",
            "email":"a@example.com",
            "body":"message\n\nSigned-off-by: B <b@example.com>\n"
        }]
        self.assertTrue(any("does not match" in e for e in guard.validate_dco_records(records)))

    def test_dco_matching_author_passes(self):
        records = [{
            "sha":"a"*40,
            "author":"A",
            "email":"a@example.com",
            "body":"message\n\nSigned-off-by: A <a@example.com>\n"
        }]
        self.assertEqual([], guard.validate_dco_records(records))


if __name__ == "__main__":
    unittest.main()
