import { pool } from "../db";
import { sendEmail } from "../notifications/email";

export const PICKUP_DAYS = 3;

export async function placeHold(toolId: string, memberId: string) {
  await pool.query(
    `INSERT INTO holds (tool_id, member_id, placed_at) VALUES ($1, $2, now())`,
    [toolId, memberId],
  );
}

export async function notifyNextHold(itemId: string) {
  const { rows } = await pool.query(
    `SELECT h.id, m.email, t.name
       FROM holds h
       JOIN items i ON i.tool_id = h.tool_id
       JOIN members m ON m.id = h.member_id
       JOIN tools t ON t.id = h.tool_id
      WHERE i.id = $1 AND h.ready_at IS NULL
      ORDER BY h.placed_at
      LIMIT 1`,
    [itemId],
  );
  if (!rows.length) return;
  const hold = rows[0];
  await pool.query(
    `UPDATE holds
        SET ready_at = now(), item_id = $2, expires_at = now() + make_interval(days => $3)
      WHERE id = $1`,
    [hold.id, itemId, PICKUP_DAYS],
  );
  await sendEmail(hold.email, "hold-ready", { tool: hold.name, days: PICKUP_DAYS });
}
