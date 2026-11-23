"""Basic repo-local Codex skill metadata validation (no external dependencies)."""
import re
import unittest
from pathlib import Path

DIR = Path(__file__).resolve().parents[1] / ".agents" / "skills"


class CodexSkillTests(unittest.TestCase):
    def test_discovery_metadata(self):
        files = sorted(DIR.glob("*/SKILL.md"))
        self.assertGreaterEqual(len(files), 15)
        self.assertLessEqual(len(files), 25)
        descriptions = []
        for file in files:
            source = file.read_text(encoding="utf-8")
            self.assertTrue(source.startswith("---\n"), file)
            parts = source.split("---", 2)
            metadata = dict(line.split(": ", 1) for line in parts[1].strip().splitlines())
            self.assertEqual(set(metadata), {"name", "description"})
            self.assertEqual(metadata["name"], file.parent.name)
            self.assertRegex(metadata["name"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
            self.assertLess(len(source), 2200)
            description = metadata["description"].strip('"')
            self.assertTrue(description.startswith("Use "), file)
            descriptions.append(description)
        self.assertEqual(len(set(descriptions)), len(files))


    def test_autonomous_coordinator_requires_all_promotion_gates(self):
        source = (DIR / "goemon-autonomous-decomp" / "SKILL.md").read_text()
        for requirement in ("stable/decomp", "COMPILER_QUIRKS.md", "EXISTING_QUIRK_NOT_APPLICABLE", "decomp.verify", "decomp.inventory",
                            "decomp.local_ci", "PROGRESS.md", "FAILED_ROM", "BLOCKED_INPUT"):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, source)

    def test_connector_bridge_never_equates_api_to_local_checkout(self):
        source = (DIR / "goemon-github-source-bridge" / "SKILL.md").read_text()
        for requirement in ("Connector text replies", "Git blob SHA", "expected_sha",
                            "BLOCKED_INPUT", "full-ROM verification"):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, source)

    def test_mandatory_skills(self):
        names = {p.parent.name for p in DIR.glob("*/SKILL.md")}
        self.assertTrue({"goemon-full-rom-proof",
                         "goemon-ido-codegen", "goemon-vm-stream",
                         "goemon-rea-evidence", "goemon-overlay-analysis",
                         "goemon-evidence-publish"} <= names)
