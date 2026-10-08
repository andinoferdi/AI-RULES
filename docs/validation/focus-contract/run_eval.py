"""Paired, fresh-session communication evaluation; no tools or rule auto-loading."""
import concurrent.futures
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MODEL = "claude-sonnet-5-5"

CASES = [
    ("simple", "Apa command Git untuk melihat branch aktif?"),
    ("coding", "Saya akan mengedit sendiri. Proyek Python punya src/parser.py dengan parse(text) yang memakai text.split(','). Bug: input kosong menghasilkan [''], seharusnya []. tests/test_parser.py memakai pytest. Berikan perubahan kode dan cara memverifikasinya."),
    ("debug", "Login mengembalikan HTTP 401. Satu-satunya bukti adalah log 'POST /login 401'. Apakah database rusak? Saya tidak bisa memberi akses server; apa yang perlu saya cek?"),
    ("complete", "Buat laporan hasil pekerjaan dari bukti ini: src/parser.py sekarang mengembalikan [] untuk input kosong; pytest tests/test_parser.py lulus 6 test; integration test tidak dijalankan. Pekerjaan yang diminta sudah selesai."),
    ("resume", "Lanjut dari checkpoint: perubahan schema lokal dan test unit selesai. Saat ini menunggu sampel CSV asli dari saya untuk memeriksa mapping import. CSV belum tersedia dan kamu tidak punya akses file atau tools. Apa posisi kita sekarang?"),
    ("list", "Berikan daftar lengkap 12 pemeriksaan sebelum merilis aplikasi web kecil. Urutkan menurut relevansi. Jangan hilangkan pemeriksaan penting."),
    ("long", "Jelaskan optimistic dan pessimistic locking secara rinci untuk developer backend. Sertakan lost update, contoh SQL dengan version dan SELECT FOR UPDATE, pemeriksaan row count, deadlock, retry, idempotensi, isolation level, serta trade-off. Saya membutuhkan penjelasan panjang, bukan ringkasan."),
    ("json", "Output hanya JSON valid dengan keys status, passed, unverified. Data: unit test lulus 6, integration belum diuji. Jangan tambahkan Markdown atau teks di luar JSON."),
    ("code", "Give only a Python function parse(text) returning [] for empty input, otherwise text.split(','). No Markdown fences or explanation."),
    ("override", "Untuk jawaban ini, saya ingin satu paragraf yang rinci tanpa daftar. Jelaskan urutan mengganti parse(text) agar input kosong menghasilkan [], menambahkan test pytest, lalu menjalankan pytest tests/test_parser.py. Saya yang mengedit sendiri."),
]


def git_file(ref):
    return subprocess.check_output(["git", "show", ref], cwd=ROOT).decode("utf-8")


def section(text, heading, following):
    return text.split(heading, 1)[1].split(following, 1)[0].strip()


def runtime_file(branch, name, checkout=None):
    if checkout is not None:
        return (checkout / name).read_text(encoding="utf-8")
    return git_file(f"{branch}:{name}")


def capture(phase, focus_root=None, web_root=None):
    snapshot = HERE / f"{phase}-inputs.json"
    if snapshot.exists():
        return json.loads(snapshot.read_text(encoding="utf-8"))
    if phase == "before":
        readme = git_file("WebBased:README.md")
        skill = git_file("focus:SKILL.md")
        context = section(readme, "## A. PRIORITAS", "## B.")
        for lang in ("english", "indonesia"):
            context += "\n" + git_file(f"WebBased:put-in-your-projects/human-language-{lang}.md")
    else:
        readme = runtime_file("WebBased", "README.md", web_root)
        skill = runtime_file("focus", "SKILL.md", focus_root)
        context = json.loads((HERE / "before-inputs.json").read_text(encoding="utf-8"))["context"]
    data = {"model": MODEL, "effort": "medium", "context": context,
            "contracts": {"skill": skill, "web": section(readme, "## X. FOCUS", "## Z.")},
            "cases": CASES}
    (HERE / f"{phase}-inputs.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return data


def run_one(phase, data, variant, case):
    name, prompt = case
    system = "Apply the following communication rules to the user's request. No tools are available.\n" + data["context"] + "\n" + data["contracts"][variant]
    system_path = HERE / f"{phase}-{variant}-system.txt"
    args = ["claude", "-p", "--safe-mode", "--system-prompt-file", str(system_path),
            "--tools", "", "--strict-mcp-config", "--disable-slash-commands",
            "--no-session-persistence", "--output-format", "json", "--model", MODEL,
            "--effort", "medium"]
    result = subprocess.run(args, input=prompt, text=True, encoding="utf-8", capture_output=True,
                            cwd=tempfile.gettempdir(), timeout=180)
    record = {"phase": phase, "variant": variant, "case": name, "prompt": prompt,
              "system_sha256": hashlib.sha256(system.encode()).hexdigest(), "exit_code": result.returncode}
    try:
        record["response"] = json.loads(result.stdout)
    except json.JSONDecodeError:
        record["stdout"] = result.stdout
    if result.returncode or "response" not in record or record["response"].get("is_error"):
        record["stderr"] = result.stderr
    (HERE / f"{phase}-{variant}-{name}.json").write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{phase}/{variant}/{name}: exit={result.returncode}", flush=True)
    return record


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("before", "after", "final"))
    parser.add_argument("--focus-root", type=Path)
    parser.add_argument("--web-root", type=Path)
    args = parser.parse_args()
    phase = args.phase
    data = capture(phase, args.focus_root, args.web_root)
    for variant in ("skill", "web"):
        system = "Apply the following communication rules to the user's request. No tools are available.\n" + data["context"] + "\n" + data["contracts"][variant]
        (HERE / f"{phase}-{variant}-system.txt").write_text(system, encoding="utf-8")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        jobs = [pool.submit(run_one, phase, data, variant, case)
                for variant in ("skill", "web") for case in data["cases"]]
        records = [job.result() for job in jobs]
    failures = [r for r in records if r["exit_code"] or "response" not in r or r["response"].get("is_error")]
    (HERE / f"{phase}-outputs.json").write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    if not failures:
        for record in records:
            (HERE / f"{phase}-{record['variant']}-{record['case']}.json").unlink()
        for variant in ("skill", "web"):
            (HERE / f"{phase}-{variant}-system.txt").unlink()
    print(f"Completed {len(records)} real inferences; transport/model errors: {len(failures)}")
    raise SystemExit(bool(failures))
