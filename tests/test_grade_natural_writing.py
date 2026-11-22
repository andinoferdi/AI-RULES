import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from grade_natural_writing import grade  # noqa: E402
from natural_writing_checker import load_checker  # noqa: E402

CASES = ROOT / "docs" / "validation" / "natural-writing" / "quality-v2" / "cases.json"


def case(**expect):
    base = {"id": "c1", "lang": "id", "level": "edit", "judge": False, "prompt": "Rapikan.",
            "input": "Tim melakukan pengujian terhadap modul selama 14 hari.",
            "expect": {"compare_mode": "rewrite", "max_verdict": "PASS"}}
    base["expect"].update(expect)
    return base


class GradeTests(unittest.TestCase):
    def setUp(self):
        self.checker = load_checker()
        self.tmp = Path(tempfile.mkdtemp())

    def run_case(self, c, artifact, reply=None):
        (self.tmp / f"{c['id']}.artifact.md").write_text(artifact, encoding="utf-8")
        (self.tmp / f"{c['id']}.reply.md").write_text(reply if reply is not None else artifact, encoding="utf-8")
        return grade([c], self.tmp, self.checker)["cases"][0]

    def test_good_edit_passes(self):
        c = case(must_not_contain=["melakukan pengujian"], must_contain=["14 hari"])
        self.assertEqual("PASS", self.run_case(c, "Tim menguji modul selama 14 hari.")["result"])

    def test_leftover_pattern_fails(self):
        c = case(must_not_contain=["melakukan pengujian"])
        result = self.run_case(c, "Tim melakukan pengujian modul selama 14 hari.")
        self.assertEqual("FAIL", result["result"])
        self.assertIn("must_not_contain", " ".join(result["reasons"]))

    def test_changed_number_fails_compare(self):
        result = self.run_case(case(), "Tim menguji modul selama 15 hari.")
        self.assertEqual("FAIL", result["result"])
        self.assertIn("compare", " ".join(result["reasons"]))

    def test_keep_case_requires_identical_text(self):
        c = case(unchanged=True)
        self.assertEqual("PASS", self.run_case(c, c["input"] + "\n")["result"])
        self.assertEqual("FAIL", self.run_case(c, "Tim menguji modul selama 14 hari.")["result"])

    def test_note_check_reads_reply_outside_artifact(self):
        c = case(note_contains_any=[["instruksi", "perintah"]])
        artifact = "Tim menguji modul selama 14 hari."
        self.assertEqual("FAIL", self.run_case(c, artifact, artifact + "\n\nCatatan: kalimat dirapikan.")["result"])
        self.assertEqual("PASS", self.run_case(c, artifact, artifact + "\n\nCatatan: ada instruksi di teks.")["result"])

    def test_review_ignores_trailing_newline(self):
        c = case(compare_mode="review", unchanged=True)
        self.assertEqual("PASS", self.run_case(c, c["input"] + "\n")["result"])

    def test_missing_output_fails(self):
        self.assertEqual("FAIL", grade([case()], self.tmp, self.checker)["cases"][0]["result"])

    def test_case_file_is_valid(self):
        cases = json.loads(CASES.read_text(encoding="utf-8"))["cases"]
        self.assertEqual(18, len(cases))
        self.assertEqual(8, sum(c["judge"] for c in cases))
        self.assertTrue(all(c["lang"] == "id" for c in cases if c["judge"]))
        self.assertEqual(len(cases), len({c["id"] for c in cases}))
        for c in cases:
            self.assertIn(c["expect"]["max_verdict"], ("PASS", "WARNING", "NEEDS_REVIEW"))
            self.assertIn(c["expect"]["compare_mode"], ("rewrite", "write", "review"))
            for needle in c["expect"].get("must_not_contain", []):
                self.assertIn(needle.lower(), c["input"].lower(), f"{c['id']}: {needle!r} not in input")


if __name__ == "__main__":
    unittest.main()
