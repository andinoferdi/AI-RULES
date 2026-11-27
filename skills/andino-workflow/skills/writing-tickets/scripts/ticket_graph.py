"""Check a folder of local tickets before anyone works from it.

    python ticket_graph.py <issues-folder>

Reads every `NN-<slug>.md` in the folder. Each ticket has a `# NN: Title` heading, a
`**Blocked by:**` line (ticket numbers such as `01`, `#01`, or `None ...`) and `- [ ]`
acceptance criteria. Prints one finding per line and exits 1 when any exist; prints
`OK <n> tickets` and exits 0 when none do; exits 2 when the folder is missing.

Findings: unknown blocker, cycle, blocked by later ticket, duplicate title, no acceptance
criteria, no Blocked by line, no title heading, and a repository file path or line number in
the body outside fenced code blocks.
"""
import re
import sys
from pathlib import Path

NAME = re.compile(r"^(\d{2,})-.+\.md$")
HEADING = re.compile(r"^#\s+(\d{2,})\s*:\s*(.+?)\s*$", re.M)
BLOCKED = re.compile(r"^\*\*Blocked by:\*\*\s*(.*)$", re.M | re.I)
CRITERION = re.compile(r"^\s*[-*]\s+\[[ xX]\]\s+\S", re.M)
FENCE = re.compile(r"^```.*?^```[^\n]*$", re.M | re.S)
PATH = re.compile(r"(?<![\w./-])(?:[\w.-]+/)+[\w.-]+\.(?:py|pyi|js|jsx|ts|tsx|go|rb|java|kt|rs|"
                  r"c|h|cpp|cs|php|swift|sql|json|ya?ml|toml|ini|cfg|md|html|css|scss|sh)\b")
LINE_NUMBER = re.compile(r"\bline\s+\d+\b", re.I)


def norm(title):
    return re.sub(r"[^a-z0-9]+", " ", title.casefold()).strip()


def read_tickets(folder):
    tickets = {}
    for path in sorted(folder.iterdir()):
        match = NAME.match(path.name)
        if path.is_file() and match:
            tickets[match[1]] = path.read_text(encoding="utf-8")
    return tickets


def findings_for(tickets):
    findings, titles, deps = [], {}, {}
    for number, text in tickets.items():
        heading = HEADING.search(text)
        if heading:
            titles[number] = heading[2]
        else:
            findings.append((number, "no title heading"))
        blocked = BLOCKED.search(text)
        if not blocked:
            findings.append((number, "no Blocked by line"))
            deps[number] = []
        else:
            value = blocked[1].strip()
            deps[number] = [] if value.casefold().startswith("none") else re.findall(r"\d{2,}", value)
        if not CRITERION.search(text):
            findings.append((number, "no acceptance criteria"))
        prose = FENCE.sub("", text)
        findings += [(number, f"file path in body {p}") for p in dict.fromkeys(PATH.findall(prose))]
        findings += [(number, f"line number in body {m.group(0)}") for m in LINE_NUMBER.finditer(prose)]

    for number, blockers in deps.items():
        for blocker in blockers:
            if blocker not in tickets:
                findings.append((number, f"unknown blocker {blocker}"))
            elif int(blocker) > int(number):
                findings.append((number, f"blocked by later ticket {blocker}"))

    def reaches(start, goal, seen):
        for dep in deps.get(start, []):
            if dep == goal:
                return True
            if dep in deps and dep not in seen and reaches(dep, goal, seen | {dep}):
                return True
        return False

    cyclic = {number for number in deps if reaches(number, number, set())}
    findings += [(number, "cycle") for number in cyclic]
    # A cycle already explains a later-numbered blocker inside it.
    findings = [(n, m) for n, m in findings
                if not (n in cyclic and m.startswith("blocked by later ticket"))]

    first_by_title = {}
    for number in sorted(titles, key=int):
        key = norm(titles[number])
        if key in first_by_title:
            findings.append((number, f"duplicate title of {first_by_title[key]}"))
        else:
            first_by_title[key] = number
    order = {"no title heading": 0}
    return sorted(dict.fromkeys(findings), key=lambda f: (int(f[0]), order.get(f[1], 1)))


def main(argv):
    if len(argv) != 2:
        print("usage: python ticket_graph.py <issues-folder>", file=sys.stderr)
        return 2
    folder = Path(argv[1])
    if not folder.is_dir():
        print(f"not a folder: {folder}", file=sys.stderr)
        return 2
    tickets = read_tickets(folder)
    if not tickets:
        print("no NN-*.md tickets found")
        return 1
    findings = findings_for(tickets)
    for number, message in findings:
        print(f"{number}: {message}")
    if findings:
        return 1
    print(f"OK {len(tickets)} tickets")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
