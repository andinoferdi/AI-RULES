import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_semantic_preservation import check, FAIL, NEEDS_REVIEW, PASS, WARNING  # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures" / "natural_writing"
SCRIPT = ROOT / "scripts" / "check_semantic_preservation.py"


def read(name):
    return (FIX / name).read_text(encoding="utf-8")


def kinds(report):
    return {kind for _level, kind, _detail in report.findings}


class RewriteModeTests(unittest.TestCase):
    def setUp(self):
        self.en = read("en_original.txt")
        self.id = read("id_original.txt")

    def test_good_english_rewrite_passes(self):
        self.assertEqual(PASS, check(self.en, read("en_good.txt")).verdict)

    def test_good_indonesian_rewrite_passes(self):
        self.assertEqual(PASS, check(self.id, read("id_good.txt")).verdict)

    def test_changed_percentage_fails(self):
        report = check(self.en, read("en_good.txt").replace("23.5%", "25.3%"))
        self.assertEqual(FAIL, report.verdict)
        self.assertIn("protected_missing", kinds(report))
        self.assertIn("protected_added", kinds(report))

    def test_changed_decimal_comma_fails(self):
        self.assertEqual(FAIL, check(self.id, read("id_good.txt").replace("12,5%", "12.5%")).verdict)

    def test_changed_pvalue_fails(self):
        self.assertEqual(FAIL, check(self.en, read("en_good.txt").replace("p < 0.05", "p < 0.01")).verdict)

    def test_added_fabricated_citation_fails(self):
        report = check(self.en, read("en_good.txt").replace("remote work,", "remote work (Jones, 2019),"))
        self.assertEqual(FAIL, report.verdict)

    def test_edited_inline_code_fails(self):
        self.assertEqual(FAIL, check(self.en, read("en_good.txt").replace("load_data()", "load_dataset()")).verdict)

    def test_changed_url_fails(self):
        self.assertEqual(FAIL, check(self.en, read("en_good.txt").replace("example.org/data", "example.org/info")).verdict)

    def test_changed_doi_fails(self):
        a = "The method follows the protocol (doi:10.1000/xyz123) closely."
        b = "The method follows the protocol (doi:10.1000/xyz124) closely."
        self.assertEqual(PASS, check(a, a).verdict)
        self.assertEqual(FAIL, check(a, b).verdict)

    def test_changed_fenced_block_fails(self):
        a = "Run:\n```\nnpm test\n```\nthen stop."
        self.assertEqual(PASS, check(a, "First run:\n```\nnpm test\n```\nthen stop.").verdict)
        self.assertEqual(FAIL, check(a, "Run:\n```\nnpm run test\n```\nthen stop.").verdict)

    def test_quote_and_identifier_changes_fail(self):
        a = 'He said "the results were not final" and set max_retries to 3 in Config.yaml.'
        self.assertEqual(PASS, check(a, a).verdict)
        self.assertEqual(FAIL, check(a, a.replace("not final", "never final")).verdict)
        self.assertEqual(FAIL, check(a, a.replace("max_retries", "maxRetries")).verdict)

    def test_curly_quote_passage_is_protected(self):
        a = "She wrote “the sample was too small” in the notes."
        self.assertEqual(FAIL, check(a, a.replace("too small", "large enough")).verdict)

    def test_numbers_inside_citation_not_double_counted(self):
        a = "Prior work (Smith et al., 2020) found this. See [3] and 2020."
        self.assertEqual(PASS, check(a, "See [3] and 2020. Prior work (Smith et al., 2020) found this.").verdict)

    def test_english_correlation_to_causation_needs_review(self):
        a = "Higher screen time is associated with lower grades, and this may be due to sleep loss."
        b = "Higher screen time causes lower grades, and this is due to sleep loss."
        self.assertEqual(NEEDS_REVIEW, check(a, b).verdict)

    def test_indonesian_correlation_to_causation_needs_review(self):
        a = "Penggunaan gawai berkorelasi dengan nilai yang lebih rendah."
        b = "Penggunaan gawai menyebabkan nilai yang lebih rendah."
        self.assertEqual(NEEDS_REVIEW, check(a, b).verdict)

    def test_hypothesis_to_finding_needs_review(self):
        a = "The hypothesis was that sleep affects memory. The result is pending."
        b = "The finding was that sleep affects memory. The results are final."
        self.assertIn("hypothesis_to_finding", kinds(check(a, b)))

    def test_dropped_limitation_needs_review(self):
        a = "The results are promising. However, the study has an important limitation: the sample was only 30 students."
        b = "The results are promising. The sample was 30 students."
        report = check(a, b)
        self.assertEqual(NEEDS_REVIEW, report.verdict)
        self.assertIn("limitation_dropped", kinds(report))

    def test_negation_change_needs_review(self):
        self.assertEqual(NEEDS_REVIEW, check("The drug did not reduce pain.", "The drug did reduce pain.").verdict)

    def test_heavy_truncation_warns(self):
        a = " ".join(["The committee reviewed the proposal carefully and wrote down each point."] * 10)
        b = "The committee reviewed the proposal carefully and wrote down each point."
        self.assertEqual(WARNING, check(a, b).verdict)

    def test_invalid_mode_raises(self):
        with self.assertRaises(ValueError):
            check("a", "b", mode="nope")


class WriteModeTests(unittest.TestCase):
    def test_faithful_draft_passes(self):
        self.assertEqual(PASS, check(read("notes.txt"), read("draft_good.txt"), mode="write").verdict)

    def test_unsourced_number_fails(self):
        draft = read("draft_good.txt") + " Also, 87% attended weekly."
        self.assertEqual(FAIL, check(read("notes.txt"), draft, mode="write").verdict)

    def test_unsourced_citation_fails(self):
        draft = read("draft_good.txt").replace("(Lee, 2019)", "(Lee, 2019; Kim, 2021)")
        self.assertEqual(FAIL, check(read("notes.txt"), draft, mode="write").verdict)

    def test_missing_source_fact_needs_review(self):
        draft = "The study involved 120 students. Mean scores rose. The hypothesis was only partly supported."
        self.assertEqual(NEEDS_REVIEW, check(read("notes.txt"), draft, mode="write").verdict)


class ReviewModeTests(unittest.TestCase):
    def test_unchanged_passes_even_with_line_ending_difference(self):
        text = read("en_original.txt")
        self.assertEqual(PASS, check(text, text, mode="review").verdict)
        self.assertEqual(PASS, check("a\nb\n", "a\r\nb\r\n", mode="review").verdict)

    def test_any_modification_fails(self):
        text = read("en_original.txt")
        self.assertEqual(FAIL, check(text, text.replace("utilization", "use"), mode="review").verdict)
        self.assertEqual(FAIL, check(text, text + " ", mode="review").verdict)


class CliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, encoding="utf-8")

    def test_exit_codes(self):
        orig, good = FIX / "en_original.txt", FIX / "en_good.txt"
        self.assertEqual(0, self.run_cli(str(orig), str(good)).returncode)
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp) / "base.txt"
            base.write_text("Screen time is associated with lower grades.", encoding="utf-8")
            causal = Path(tmp) / "causal.txt"
            causal.write_text("Screen time causes lower grades.", encoding="utf-8")
            self.assertEqual(1, self.run_cli(str(base), str(causal)).returncode)
            bad = Path(tmp) / "bad.txt"
            bad.write_text(good.read_text(encoding="utf-8").replace("23.5%", "99%"), encoding="utf-8")
            result = self.run_cli(str(orig), str(bad))
            self.assertEqual(2, result.returncode)
            self.assertIn("FAIL", result.stdout)

    def test_json_output_and_mode(self):
        result = self.run_cli(str(FIX / "notes.txt"), str(FIX / "draft_good.txt"), "--mode", "write", "--json")
        self.assertEqual(0, result.returncode)
        self.assertEqual("PASS", json.loads(result.stdout)["verdict"])

    def test_help_states_limits(self):
        out = " ".join(self.run_cli("--help").stdout.split())
        self.assertIn("NOT semantic equivalence", out)
        self.assertIn("2 FAIL", out)

    def test_missing_file_is_error(self):
        self.assertEqual(2, self.run_cli("nope1.txt", "nope2.txt").returncode)


if __name__ == "__main__":
    unittest.main()
