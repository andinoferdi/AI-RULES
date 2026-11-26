// src/routes/renewNow.ts
import { Request, Response } from "express";
import * as ledger from "../ledger/ledger";
import { SesMailer } from "../mail/SesMailer";
import { RenewalNotifier } from "../renewals/RenewalNotifier";
import { RenewalPricing } from "../renewals/RenewalPricing";
import { RenewalRepoWrapper } from "../renewals/RenewalRepoWrapper";
import { RenewalValidator } from "../renewals/RenewalValidator";
import { loadSubscription } from "../subscriptions/loadSubscription";

const validator = new RenewalValidator();
const pricing = new RenewalPricing();
const repo = new RenewalRepoWrapper();
const notifier = new RenewalNotifier(new SesMailer());

// POST /subscriptions/:id/renew
export async function renewNow(req: Request, res: Response) {
  const sub = await loadSubscription(req.params.id);
  if (!validator.isRenewable(sub)) {
    return res.status(409).json({ error: "subscription is not renewable" });
  }
  const amount = pricing.amountFor(sub);

  const client = await repo.begin();
  let invoiceId: string;
  try {
    invoiceId = await repo.insertInvoice(client, sub.id, amount);
    await repo.advancePeriod(client, sub.id);
    await ledger.write(client, { customerId: sub.customerId, invoiceId, amount, kind: "renewal" });
    await repo.commit(client);
  } catch (err) {
    await repo.rollback(client);
    return res.status(500).json({ error: "renewal failed" });
  }

  await notifier.sendRenewalEmail(sub.email, invoiceId, amount);
  return res.status(201).json({ invoiceId });
}
