// src/cli/adminRenew.ts
// Usage: npm run admin:renew -- <subscriptionId> [--dry-run]
import { format } from "../money/money";
import { SesMailer } from "../mail/SesMailer";
import { RenewalNotifier } from "../renewals/RenewalNotifier";
import { RenewalPricing } from "../renewals/RenewalPricing";
import { RenewalRepoWrapper } from "../renewals/RenewalRepoWrapper";
import { loadSubscription } from "../subscriptions/loadSubscription";

const pricing = new RenewalPricing();
const repo = new RenewalRepoWrapper();
const notifier = new RenewalNotifier(new SesMailer());

async function main(argv: string[]) {
  const [subscriptionId, flag] = argv;
  if (!subscriptionId) throw new Error("usage: admin:renew <subscriptionId> [--dry-run]");

  const sub = await loadSubscription(subscriptionId);
  const amount = pricing.amountFor(sub);
  if (flag === "--dry-run") {
    console.log(`would renew ${sub.id} for ${format(amount)}`);
    return;
  }

  const client = await repo.begin();
  try {
    const invoiceId = await repo.insertInvoice(client, sub.id, amount);
    await repo.advancePeriod(client, sub.id);
    await repo.commit(client);
    await notifier.sendRenewalEmail(sub.email, invoiceId, amount);
    console.log(`renewed ${sub.id}: invoice ${invoiceId} for ${format(amount)}`);
  } catch (err) {
    await repo.rollback(client);
    throw err;
  }
}

main(process.argv.slice(2)).catch((err) => {
  console.error(err);
  process.exit(1);
});
