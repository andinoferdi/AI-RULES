// src/routes/changePlan.ts
import { Request, Response } from "express";
import { pool } from "../db";
import * as ledger from "../ledger/ledger";
import { subtract } from "../money/money";
import { priceFor } from "../pricing/priceFor";
import { prorate } from "../proration/prorate";
import { loadSubscription } from "../subscriptions/loadSubscription";
import { PlanId } from "../types";

const DAY_MS = 24 * 60 * 60 * 1000;
const DAYS_IN_PERIOD = 30;

// POST /subscriptions/:id/plan  { planId }
export async function changePlan(req: Request, res: Response) {
  const sub = await loadSubscription(req.params.id);
  const newPlan = req.body.planId as PlanId;

  const oldPrice = priceFor(sub.planId, sub.customerCountry);
  const newPrice = priceFor(newPlan, sub.customerCountry);

  // Credit the unused part of the current plan against the new plan.
  const daysUsed = Math.floor((Date.now() - sub.currentPeriodStart.getTime()) / DAY_MS);
  const usedCharge = prorate(oldPrice, daysUsed, DAYS_IN_PERIOD);
  const unusedCredit = subtract(oldPrice, usedCharge);
  const amountDue = subtract(newPrice, unusedCredit);

  const client = await pool.connect();
  try {
    await client.query("BEGIN");
    await client.query("UPDATE subscriptions SET plan_id = $1 WHERE id = $2", [newPlan, sub.id]);
    const inv = await client.query(
      "INSERT INTO invoices (subscription_id, amount_cents) VALUES ($1, $2) RETURNING id",
      [sub.id, amountDue.cents],
    );
    await ledger.write(client, {
      customerId: sub.customerId,
      invoiceId: inv.rows[0].id,
      amount: amountDue,
      kind: "plan_change",
    });
    await client.query("COMMIT");
    res.status(200).json({ invoiceId: inv.rows[0].id, amountDueCents: amountDue.cents });
  } catch (err) {
    await client.query("ROLLBACK");
    res.status(500).json({ error: "plan change failed" });
  } finally {
    client.release();
  }
}
