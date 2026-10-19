#!/usr/bin/env python3
"""Bounded semantic-preservation safeguard for rewritten prose.

This is NOT a semantic-equivalence checker and cannot prove that meaning is
preserved. It only catches a narrow, mechanical class of damage:

* deterministic (FAIL): protected tokens that were added or went missing
  (numbers, percentages, dates/years, statistics such as "p < 0.05", citations,
  DOIs, URLs, code, long quoted passages, identifiers, version strings);
* heuristic (NEEDS_REVIEW): shifts in hedging/certainty, causal wording,
  hypothesis-to-finding wording, contrast/limitation markers and negations;
* WARNING: a rewrite that is much shorter than the original (possible truncation).

A PASS means only "none of these checks fired"; a human or the model must still
read the result. Modes:

  rewrite  CANDIDATE is a rewrite of ORIGINAL (default).
  write    ORIGINAL holds source notes, CANDIDATE is a draft from them. Numbers,
           citations, DOIs, URLs and quotes absent from the notes are FAIL
           (fabrication); source facts absent from the draft are NEEDS_REVIEW.
  review   ORIGINAL and CANDIDATE are the file before/after a review; any
           difference (line endings normalized) is FAIL.

Exit codes: 0 = PASS or WARNING, 1 = NEEDS_REVIEW, 2 = FAIL.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from typing import List, Tuple

PASS, WARNING, NEEDS_REVIEW, FAIL = "PASS", "WARNING", "NEEDS_REVIEW", "FAIL"
_RANK = {PASS: 0, WARNING: 1, NEEDS_REVIEW: 2, FAIL: 3}
EXIT_CODES = {PASS: 0, WARNING: 0, NEEDS_REVIEW: 1, FAIL: 2}

Finding = Tuple[str, str, str]


@dataclass
class Report:
    findings: List[Finding] = field(default_factory=list)

    @property
    def verdict(self) -> str:
        worst = PASS
        for level, _kind, _detail in self.findings:
            if _RANK[level] > _RANK[worst]:
                worst = level
        return worst

    def to_dict(self) -> dict:
        return {
            "verdict": self.verdict,
            "findings": [{"level": a, "kind": b, "detail": c} for a, b, c in self.findings],
        }


_YEAR = r"(?:1[5-9]|20)\d{2}[a-z]?"
_AUTHOR = r"[A-Z][\w'’\-]+"

# (kind, compiled regex, group to normalise). Applied in order; each match is
# masked so later patterns do not count the same characters twice.
_PATTERNS = [
    ("code_block", re.compile(r"```.*?```", re.S), 0),
    ("code", re.compile(r"`[^`\n]+`"), 0),
    ("url", re.compile(r"https?://[^\s<>)\]]+[^\s<>)\].,;:!?]|www\.[^\s<>)\]]+[^\s<>)\].,;:!?]"), 0),
    ("doi", re.compile(r"\b10\.\d{4,9}/[^\s<>\"]*[^\s<>\".,;:!?)\]]", re.I), 0),
    ("quote", re.compile(r"\"([^\"\n]+)\"|“([^”\n]+)”"), -1),
    ("citation", re.compile(r"\((?:e\.g\.,?\s*|see\s+|lihat\s+)?" + _AUTHOR + r"[^()]*?" + _YEAR + r"[^()]*\)"), 0),
    ("citation", re.compile(_AUTHOR + r"(?:\s+(?:et al\.|dkk\.|dan|and|&)(?:\s+" + _AUTHOR + r")?)?\s*\(\s*" + _YEAR + r"\s*\)"), 0),
    ("citation", re.compile(r"\[\d+(?:\s*[,–—-]\s*\d+)*\]"), 0),
    ("stat", re.compile(r"(?<!\w)(?:[pP]|r|R2|t|F|M|SD|n|N|df|d|OR|CI|β|α)\s*(?:<|>|=|≤|≥)\s*[-−]?\d*[.,]?\d+"), 0),
    ("version", re.compile(r"(?<![\w.])v?\d+(?:\.\d+){2,}\b"), 0),
    ("percent", re.compile(r"(?<![\w.,])\d+(?:[.,]\d+)*\s?(?:%|percent\b|persen\b)"), 0),
    ("number", re.compile(r"(?<![\w.,])\d+(?:[.,]\d+)*"), 0),
    ("identifier", re.compile(r"\b[A-Za-z0-9]+(?:_[A-Za-z0-9]+)+\b"), 0),
    ("identifier", re.compile(r"\b[a-z]+(?:[A-Z][a-z0-9]+)+\b"), 0),
    ("identifier", re.compile(r"\b[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]+)+\b"), 0),
    ("identifier", re.compile(r"\b[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+\b"), 0),
    ("identifier", re.compile(r"\b[A-Z]{2,}\b"), 0),
]
_DOTTED_SKIP = {"e.g", "i.e", "etc", "et.al"}
_FACT_KINDS = {"number", "percent", "stat", "citation", "doi", "url", "version", "quote"}


def _norm(kind: str, text: str) -> str:
    if kind in ("percent", "stat"):
        text = re.sub(r"percent|persen", "%", text)
        return re.sub(r"\s+", "", text)
    if kind in ("code_block", "code"):
        return text
    return re.sub(r"\s+", " ", text).strip()


def extract(text: str) -> Counter:
    """Return a multiset of (kind, token) protected tokens, masking as it goes."""
    tokens: Counter = Counter()
    work = text.replace("\r\n", "\n")
    for kind, rx, group in _PATTERNS:
        def repl(m, kind=kind, group=group):
            raw = m.group(0)
            if kind == "quote":
                inner = m.group(1) or m.group(2) or ""
                if len(inner.split()) < 3:
                    return raw
                tokens[(kind, _norm(kind, inner))] += 1
                return " "
            if kind == "identifier" and raw.lower().rstrip(".") in _DOTTED_SKIP:
                return raw
            tokens[(kind, _norm(kind, raw))] += 1
            return " "
        work = rx.sub(repl, work)
    return tokens


_WORD = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)?", re.U)


def _count(pattern: str, text: str) -> int:
    return len(re.findall(pattern, text, re.I | re.U))


_HEDGE = r"\b(?:may|might|could|suggest\w*|indicat\w*|appear\w*|likely|possibl[ey]|perhaps|correlat\w*|associated with|mungkin|diduga|cenderung|menunjukkan|mengindikasikan|berkorelasi|berhubungan|kemungkinan|korelasi)\b"
_STRONG = r"\b(?:causes?|caused|causing|leads? to|led to|prove[sd]?|proven|demonstrate[sd]?|confirm(?:s|ed|ing)?|definitely|certainly|menyebabkan|mengakibatkan|membuktikan|memastikan|pasti|terbukti)\b"
_HYPOTHESIS = r"\b(?:hypothes[ie]s|hipotesis)\b"
_FINDING = r"\b(?:findings?|temuan|results?|hasil)\b"
_NEGATION = r"\b(?:not|no|never|none|neither|nor|cannot|tidak|bukan|belum|tanpa|tak)\b|n't\b|n’t\b"
_GROUPS = (
    ("limitation", r"\b(?:limitations?|keterbatasan)\b"),
    ("contrast", r"\b(?:however|although|though|but|namun|tetapi|meskipun|walaupun)\b"),
    ("scope", r"\b(?:only|hanya|sekadar)\b"),
)


def _heuristics(original: str, candidate: str) -> List[Finding]:
    out: List[Finding] = []
    h0, h1 = _count(_HEDGE, original), _count(_HEDGE, candidate)
    if h1 < h0:
        out.append((NEEDS_REVIEW, "hedging_reduced", f"hedging/certainty words {h0} -> {h1}; claim may be stronger"))
    s0, s1 = _count(_STRONG, original), _count(_STRONG, candidate)
    if s1 > s0:
        out.append((NEEDS_REVIEW, "strong_claim_added", f"causal/certainty words {s0} -> {s1}"))
    y0, y1 = _count(_HYPOTHESIS, original), _count(_HYPOTHESIS, candidate)
    f0, f1 = _count(_FINDING, original), _count(_FINDING, candidate)
    if y1 < y0 and f1 > f0:
        out.append((NEEDS_REVIEW, "hypothesis_to_finding", f"hypothesis {y0} -> {y1} while finding/result {f0} -> {f1}"))
    for name, pat in _GROUPS:
        a, b = _count(pat, original), _count(pat, candidate)
        if b < a:
            out.append((NEEDS_REVIEW, "limitation_dropped", f"{name} markers {a} -> {b}"))
    n0, n1 = _count(_NEGATION, original), _count(_NEGATION, candidate)
    if n0 != n1:
        out.append((NEEDS_REVIEW, "negation_changed", f"negation words {n0} -> {n1}"))
    return out


def _fmt(items) -> str:
    return "; ".join(f"{k}:{t!r}" + (f" x{n}" if n > 1 else "") for (k, t), n in sorted(items.items()))


def check(original: str, candidate: str, mode: str = "rewrite") -> Report:
    """Run the bounded checks. See the module docstring for what they do not cover."""
    if mode not in ("rewrite", "write", "review"):
        raise ValueError(f"unknown mode: {mode}")
    report = Report()
    if mode == "review":
        if original.replace("\r\n", "\n") != candidate.replace("\r\n", "\n"):
            report.findings.append((FAIL, "review_modified", "file differs from the original; review must not edit it"))
        return report

    orig_tokens, cand_tokens = extract(original), extract(candidate)
    missing = orig_tokens - cand_tokens
    added = cand_tokens - orig_tokens
    if mode == "rewrite":
        if missing:
            report.findings.append((FAIL, "protected_missing", _fmt(missing)))
        if added:
            report.findings.append((FAIL, "protected_added", _fmt(added)))
    else:
        fabricated = Counter({k: v for k, v in added.items() if k[0] in _FACT_KINDS})
        lost = Counter({k: v for k, v in missing.items() if k[0] in _FACT_KINDS})
        if fabricated:
            report.findings.append((FAIL, "fabricated", "not in source notes: " + _fmt(fabricated)))
        if lost:
            report.findings.append((NEEDS_REVIEW, "source_fact_missing", "not in draft: " + _fmt(lost)))

    report.findings.extend(_heuristics(original, candidate))

    if mode == "rewrite":
        w0, w1 = len(_WORD.findall(original)), len(_WORD.findall(candidate))
        if w0 and w1 < 0.6 * w0:
            report.findings.append((WARNING, "possible_truncation", f"candidate has {w1} words vs {w0} (<60%)"))
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Bounded safeguard, NOT semantic equivalence: compares protected tokens "
            "(numbers, statistics, citations, DOIs, URLs, code, quotes, identifiers) "
            "and flags hedging/causality/limitation shifts. PASS does not prove "
            "meaning is preserved. Exit codes: 0 PASS or WARNING, 1 NEEDS_REVIEW, 2 FAIL."
        )
    )
    parser.add_argument("original", help="original text file (source notes in write mode)")
    parser.add_argument("candidate", help="rewritten/drafted/after-review text file")
    parser.add_argument("--mode", choices=("rewrite", "write", "review"), default="rewrite")
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    args = parser.parse_args(argv)
    try:
        with open(args.original, encoding="utf-8-sig", newline="") as fh:
            original = fh.read()
        with open(args.candidate, encoding="utf-8-sig", newline="") as fh:
            candidate = fh.read()
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    report = check(original, candidate, args.mode)
    if args.json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(report.verdict)
        for level, kind, detail in report.findings:
            print(f"  {level} {kind}: {detail}")
        print("Bounded check only; not proof of preserved meaning.")
    return EXIT_CODES[report.verdict]


if __name__ == "__main__":
    raise SystemExit(main())
