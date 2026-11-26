// src/webhooks/paymentWebhook.ts
import { Request, Response } from "express";
import { PayGateClient } from "paygate-node";
import { pool } from "../db";
import { SesMailer } from "../mail/SesMailer";

// POST /webhooks/paygate
export async function paymentWebhook(req: Request, res: Response) {
  const paygate = new PayGateClient(process.env.PAYGATE_KEY!, { timeoutMs: 5000, retries: 2 });
  const event = await paygate.webhooks.verifyAndParse(
    (req as any).rawBody,
    req.header("PayGate-Signature") ?? "",
  );

  if (event.type === "charge.failed") {
    const subscriptionId = event.data.metadata.subscriptionId;
    await pool.query("UPDATE subscriptions SET status = 'past_due' WHERE id = $1", [subscriptionId]);
    const r = await pool.query(
      "SELECT c.email FROM subscriptions s JOIN customers c ON c.id = s.customer_id WHERE s.id = $1",
      [subscriptionId],
    );
    await new SesMailer().send(r.rows[0].email, "Payment failed", "Please update your card to keep your plan.");
  }

  if (event.type === "charge.succeeded" && event.data.metadata.subscriptionId) {
    await pool.query("UPDATE subscriptions SET status = 'active' WHERE id = $1 AND status = 'past_due'", [
      event.data.metadata.subscriptionId,
    ]);
  }

  res.sendStatus(200);
}
