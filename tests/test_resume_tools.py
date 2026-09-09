import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents/skills/headhunter-resume"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


helpers = module("resume_tools", SKILL / "scripts/resume_tools.py")
builder = module("build_catalog", ROOT / "scripts/build_catalog.py")
installer = module("install_skill", ROOT / "scripts/install_skill.py")


def inventory():
    return {
        "schema_version": 1,
        "candidate_id": "fictional-01",
        "target": {"mode": "tailor", "role": "Backend developer", "seniority": "Junior", "market": "Canada"},
        "sources": [{"id": "s1", "kind": "interview", "locator": "Synthetic test answer 1", "accessed": "2026-09-09", "note": "Candidate describes writing Python filters."}],
        "experiences": [{"id": "e1", "kind": "internship", "title": "Developer intern", "organization": "Example organization", "start": "2025-05", "end": "2025-08", "description": "File-search prototype"}],
        "claims": [{"id": "c1", "experience_id": "e1", "text": "Wrote Python filters for a file-search prototype.", "status": "confirmed", "ownership": "personal", "source_ids": ["s1"], "keywords": ["Python"], "confirmation": "Explicit synthetic candidate answer"}],
        "requirements": [{"id": "r1", "text": "Python", "priority": "required", "assessment": "supported", "claim_ids": ["c1"]}],
        "open_questions": [], "notes": [],
    }


class EvidenceTests(unittest.TestCase):
    def test_valid_inventory_and_draft(self):
        data = inventory()
        self.assertEqual(helpers.validate_inventory(data), [])
        self.assertEqual(helpers.audit_draft(data, {"claims": [{"text": data["claims"][0]["text"], "evidence_ids": ["c1"]}]}), [])

    def test_missing_source_and_duplicate_ids(self):
        data = inventory()
        data["claims"][0]["source_ids"] = ["not-here"]
        data["sources"].append(copy.deepcopy(data["sources"][0]))
        errors = helpers.validate_inventory(data)
        self.assertTrue(any("unknown reference" in e for e in errors))
        self.assertTrue(any("Duplicate" in e for e in errors))

    def test_unconfirmed_conflicting_rejected_and_unknown_ownership_block_draft(self):
        for status, ownership in [("unconfirmed", "personal"), ("conflict", "personal"), ("rejected", "personal"), ("confirmed", "unknown")]:
            with self.subTest(status=status, ownership=ownership):
                data = inventory()
                data["requirements"] = []
                data["claims"][0].update(status=status, ownership=ownership)
                self.assertTrue(helpers.audit_draft(data, {"claims": [{"text": "Used Python", "evidence_ids": ["c1"]}]}))

    def test_draft_without_known_evidence_fails(self):
        for refs in ([], ["missing"], [None], "c1"):
            self.assertTrue(helpers.audit_draft(inventory(), {"claims": [{"text": "Used Python", "evidence_ids": refs}]}))

    def test_unknown_requirement_can_remain_unanswered(self):
        data = inventory()
        data["requirements"].append({"id": "r2", "text": "AWS", "priority": "required", "assessment": "unknown", "claim_ids": []})
        self.assertEqual(helpers.validate_inventory(data), [])

    def test_unsupported_requirement_cannot_be_marked_supported(self):
        data = inventory()
        data["requirements"][0]["claim_ids"] = []
        self.assertTrue(helpers.validate_inventory(data))

    def test_invalid_dates_and_reversed_dates_fail(self):
        for start, end in [("2025-13", None), ("2026-06", "2026-01"), ("present", "2026-01")]:
            data = inventory()
            data["experiences"][0].update(start=start, end=end)
            self.assertTrue(helpers.validate_inventory(data))

    def test_unknown_dates_are_preserved(self):
        data = inventory()
        data["experiences"][0].update(start=None, end=None)
        self.assertEqual(helpers.validate_inventory(data), [])

    def test_incomplete_intake_preserves_unknown_experience_fields(self):
        data = inventory()
        data["experiences"][0].update(title=None, organization=None, description=None)
        self.assertEqual(helpers.validate_inventory(data), [])

    def test_experience_fields_reject_nontext_values(self):
        data = inventory()
        data["experiences"][0].update(title=[], organization=42, description={})
        self.assertGreaterEqual(len(helpers.validate_inventory(data)), 3)

    def test_malformed_data_is_reported_without_traceback(self):
        for data in (None, [], {}, {"claims": "bad"}):
            self.assertTrue(helpers.validate_inventory(data))
        data = inventory()
        data["claims"][0]["experience_id"] = []
        self.assertTrue(helpers.validate_inventory(data))

    def test_malformed_enum_types_are_reported(self):
        data = inventory()
        data["target"]["mode"] = []
        data["claims"][0]["status"] = {}
        data["claims"][0]["ownership"] = []
        data["requirements"][0]["priority"] = {}
        data["requirements"][0]["assessment"] = []
        self.assertGreaterEqual(len(helpers.validate_inventory(data)), 5)

    def test_structural_audit_does_not_claim_semantic_verification(self):
        # This documents a deliberate boundary: the agent must catch changed meaning.
        draft = {"claims": [{"text": "Saved 99% of costs for 10000 customers", "evidence_ids": ["c1"]}]}
        self.assertEqual(helpers.audit_draft(inventory(), draft), [])

    def test_cli_errors_and_exit_codes(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "inventory.json"
            path.write_text(json.dumps(inventory()), encoding="utf-8")
            cmd = [sys.executable, str(SKILL / "scripts/resume_tools.py"), "validate", str(path)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(json.loads(result.stdout)["ok"])
            path.write_text("{}", encoding="utf-8")
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 1)
            path.write_text("broken json", encoding="utf-8")
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 2)


class CatalogTests(unittest.TestCase):
    def test_enclosing_html_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "wrapper.html"
            path.write_text("<html><body>No table</body></html>", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "no table rows"):
                builder.build(path, path, path, "2026-09-09")

    def test_local_catalog_search_and_empty_result(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "catalog.json"
            path.write_text(json.dumps({"snapshot_date": "2026-09-09", "market": "Synthetic test", "episodes": [{"job_title": "Software Engineer", "episode": 1}], "qualifications": [{"job_title": "Accountant", "qualifications": "Synthetic example"}]}), encoding="utf-8")
            self.assertEqual(helpers.search_catalog("software engineer", "episodes", catalog_path=path)["total_matches"], 1)
            self.assertEqual(helpers.search_catalog("accountant", "qualifications", catalog_path=path)["total_matches"], 1)
            self.assertEqual(helpers.search_catalog("no-such-role-982734", "episodes", catalog_path=path)["results"], [])
            result = subprocess.run([sys.executable, str(SKILL / "scripts/resume_tools.py"), "search", "accountant", "--kind", "qualifications", "--catalog", str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
        with self.assertRaises(ValueError):
            helpers.search_catalog(" ", "episodes")

    def test_search_requires_user_catalog(self):
        with self.assertRaisesRegex(ValueError, "No catalog bundled"):
            helpers.search_catalog("software engineer", "episodes")
        result = subprocess.run([sys.executable, str(SKILL / "scripts/resume_tools.py"), "search", "accountant"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("--catalog", result.stderr)

    def test_url_parser(self):
        self.assertEqual(builder.youtube_url("https://youtu.be/aeoSJdrFb7U?t=30"), "https://www.youtube.com/watch?v=aeoSJdrFb7U")
        self.assertEqual(builder.youtube_url("https://www.google.com/url?q=https%3A%2F%2Fyoutu.be%2FaeoSJdrFb7U"), "https://www.youtube.com/watch?v=aeoSJdrFb7U")
        self.assertIsNone(builder.youtube_url("https://youtube.com.evil.example/watch?v=aeoSJdrFb7U"))
        self.assertIsNone(builder.youtube_url("Title with no URL"))

    def test_recover_hyperlink_and_preserve_unresolved_row(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            episodes = folder / "episodes.csv"
            quals = folder / "quals.csv"
            html = folder / "sheet.html"
            episodes.write_text('Job Title,Episode,Link to Episode,Release Date,Good Resume\nEngineer,1,Review title,September 1st 2026,Good Resume\nAnalyst,2,Missing title,,\n', encoding="utf-8")
            quals.write_text('Job Title,Quilfications ,Last Updated\nEngineer,"Python\nSQL",9/1/2026\n', encoding="utf-8")
            html.write_text('<table><tr><td>Engineer</td><td>1</td><td><a href="https://youtu.be/aeoSJdrFb7U">Review title</a></td></tr></table>', encoding="utf-8")
            result = builder.build(episodes, quals, html, "2026-09-09")
            self.assertTrue(result["episodes"][0]["url"])
            self.assertIsNone(result["episodes"][1]["url"])
            self.assertEqual(result["qualifications"][0]["qualifications"], "Python\nSQL")


class InstallTests(unittest.TestCase):
    def test_portable_install_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            target = installer.install(Path(folder) / "skills")
            self.assertTrue((target / "SKILL.md").exists())
            self.assertTrue((target / "LICENSE").exists())
            self.assertFalse((target / "references/catalog.json").exists())
            script = target / "scripts/resume_tools.py"
            path = Path(folder) / "inventory.json"
            path.write_text(json.dumps(inventory()), encoding="utf-8")
            result = subprocess.run([sys.executable, str(script), "validate", str(path)], cwd=folder, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(json.loads(result.stdout)["ok"])
            with self.assertRaises(FileExistsError):
                installer.install(Path(folder) / "skills")

    def test_installer_cli_with_spaces_in_destination(self):
        with tempfile.TemporaryDirectory() as folder:
            dest = Path(folder) / "custom skills"
            cmd = [sys.executable, str(ROOT / "scripts/install_skill.py"), "--destination", str(dest)]
            result = subprocess.run(cmd, cwd=folder, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((dest / "headhunter-resume/SKILL.md").is_file())
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 1)


if __name__ == "__main__":
    unittest.main()
