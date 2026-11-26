// src/legacy/csvExport.ts
// Old finance export. Still linked from the admin menu; nobody has touched it since launch.
import { pool } from "../db";
import { format, fromCents } from "../money/money";

export async function exportInvoicesCsv(from: any, to: any) {
  var out = "id,subscription,amount\n";
  var res: any = await pool.query("select * from invoices where created_at >= '" + from + "' and created_at < '" + to + "'");
  for (var i = 0; i < res.rows.length; i++) {
    var r = res.rows[i];
    out = out + r.id + "," + r.subscription_id + "," + format(fromCents(r.amount_cents)) + "\n";
  }
  return out;
}
