import { pool } from "../db";
import { notifyNextHold } from "../holds/service";

export const LOAN_DAYS = 14;
export const MAX_RENEWALS = 1;

export async function checkout(itemId: string, memberId: string) {
  await pool.query(
    `INSERT INTO loans (item_id, member_id, checked_out_at, due_at, renewals)
     VALUES ($1, $2, now(), now() + make_interval(days => $3), 0)`,
    [itemId, memberId, LOAN_DAYS],
  );
}

export async function renew(loanId: string) {
  const { rows } = await pool.query(
    `SELECT l.renewals, i.tool_id
       FROM loans l JOIN items i ON i.id = l.item_id
      WHERE l.id = $1`,
    [loanId],
  );
  const loan = rows[0];
  if (loan.renewals >= MAX_RENEWALS) throw new Error("RENEWAL_LIMIT");
  const waiting = await pool.query(
    `SELECT 1 FROM holds WHERE tool_id = $1 AND ready_at IS NULL LIMIT 1`,
    [loan.tool_id],
  );
  if (waiting.rowCount) throw new Error("HOLD_WAITING");
  await pool.query(
    `UPDATE loans
        SET due_at = due_at + make_interval(days => $2), renewals = renewals + 1
      WHERE id = $1`,
    [loanId, LOAN_DAYS],
  );
}

export async function checkin(itemId: string) {
  const { rows } = await pool.query(
    `UPDATE loans SET returned_at = now()
      WHERE item_id = $1 AND returned_at IS NULL
      RETURNING item_id`,
    [itemId],
  );
  if (rows.length) await notifyNextHold(itemId);
}
