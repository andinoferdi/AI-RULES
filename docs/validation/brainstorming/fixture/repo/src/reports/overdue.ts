// Run by deploy/crontab every Friday at 22:00. Writes overdue.csv to the
// volunteer shared drive for the Saturday phone calls.
import { writeFile } from "node:fs/promises";
import { pool } from "../db";

const LOAN_DAYS = 14; // keep in sync with src/loans/service.ts

export async function writeOverdueCsv(path = "/mnt/volunteer-drive/overdue.csv") {
  const { rows } = await pool.query(
    `SELECT m.name, m.phone, t.name AS tool, i.barcode,
            date_part('day', now() - l.checked_out_at) - $1 AS days_overdue
       FROM loans l
       JOIN members m ON m.id = l.member_id
       JOIN items i ON i.id = l.item_id
       JOIN tools t ON t.id = i.tool_id
      WHERE l.returned_at IS NULL
        AND l.checked_out_at < now() - make_interval(days => $1)
      ORDER BY days_overdue DESC`,
    [LOAN_DAYS],
  );
  const lines = [
    "name,phone,tool,barcode,days_overdue",
    ...rows.map((r) => [r.name, r.phone, r.tool, r.barcode, r.days_overdue].join(",")),
  ];
  await writeFile(path, lines.join("\n") + "\n");
}

if (require.main === module) {
  writeOverdueCsv().then(() => process.exit(0));
}
