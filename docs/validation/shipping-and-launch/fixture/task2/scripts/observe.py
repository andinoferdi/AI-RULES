"""Print cohort metrics: the flag cohort (candidate) against everyone else (control)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    percent = json.loads((ROOT / "ops" / "flags.json").read_text(encoding="utf-8")).get("bulk_edit", 0)
    data = json.loads((ROOT / "data" / ("live.json" if percent > 0 else "after_stop.json")).read_text(encoding="utf-8"))
    print(f"bulk_edit flag: {percent}%")
    print("window            candidate req / 5xx      control req / 5xx")
    for w in data["windows"]:
        c, k = w["candidate"], w["control"]
        print(f"{w['from']:>8}-{w['to']:<8}  {c['requests']:>8} / {c['errors_5xx']:<4}        {k['requests']:>8} / {k['errors_5xx']}")
    print(f"p95 latency ms: candidate {data['p95_ms']['candidate']}, control {data['p95_ms']['control']}")
    print(f"sessions: candidate {data['sessions']['candidate']}, control {data['sessions']['control']}")
    for e in data["new_client_errors"]:
        print(f"new client error: {e['type']}: candidate sessions {e['candidate_sessions']}, control sessions {e['control_sessions']}")
    s = data["task_saves"]
    print(f"task saves started/completed: candidate {s['candidate']['started']}/{s['candidate']['completed']}, "
          f"control {s['control']['started']}/{s['control']['completed']}")
    print(f"bulk_edit_log rows: {data['bulk_edit_log_rows']}")


if __name__ == "__main__":
    main()
