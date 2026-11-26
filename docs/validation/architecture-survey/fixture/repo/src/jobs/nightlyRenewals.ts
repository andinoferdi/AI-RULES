// src/jobs/nightlyRenewals.ts
import * as ledger from "../ledger/ledger";
import { SesMailer } from "../mail/SesMailer";
import { prorate } from "../proration/prorate";
import { RenewalNotifier } from "../renewals/RenewalNotifier";
import { RenewalPricing } from "../renewals/RenewalPricing";
import { RenewalRepoWrapper } from "../renewals/RenewalRepoWrapper";
import { RenewalValidator } from "../renewals/RenewalValidator";
import { findDueSubscriptions } from "../subscriptions/loadSubscription";

const DAY_MS = 24 * 60 * 60 * 1000;

const validator = new RenewalValidator();
const pricing = new RenewalPricing();
const repo = new RenewalRepoWrapper();
const notifier = new RenewalNotifier(new SesMailer());

// Runs at 02:00 UTC from the scheduler.
export async function runNightlyRenewals(now = new Date()): Promise<{ renewed: number; failed: number }> {
  const due = await findDueSubscriptions(now);
  let renewed = 0;
  let failed = 0;

  for (const sub of due) {
    if (!validator.isRenewable(sub)) continue;

    let amount = pricing.amountFor(sub);
    if (sub.pausedDays > 0) {
      // Paused subscriptions pay only for the calendar days they were active.
      const daysInPeriod = Math.round(
        (sub.currentPeriodEnd.getTime() - sub.currentPeriodStart.getTime()) / DAY_MS,
      );
      amount = prorate(amount, daysInPeriod - sub.pausedDays, daysInPeriod);
    }

    const client = await repo.begin();
    try {
      const invoiceId = await repo.insertInvoice(client, sub.id, amount);
      await notifier.sendRenewalEmail(sub.email, invoiceId, amount);
      await repo.advancePeriod(client, sub.id);
      await ledger.write(client, { customerId: sub.customerId, invoiceId, amount, kind: "renewal" });
      await repo.commit(client);
      renewed++;
    } catch (err) {
      await repo.rollback(client);
      failed++;
      console.error("nightly renewal failed", { subscriptionId: sub.id, err });
    }
  }

  return { renewed, failed };
}
