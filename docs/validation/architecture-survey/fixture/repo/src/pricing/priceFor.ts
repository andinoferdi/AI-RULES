// src/pricing/priceFor.ts
// Finance reviews every change in this folder (docs/adr/0002-pricing-stays-separate.md).
import { Money, fromCents } from "../money/money";
import { PlanId } from "../types";

const NET_CENTS: Record<PlanId, number> = { basic: 900, pro: 2900, team: 9900 };
const VAT: Record<string, number> = { ID: 0.11, DE: 0.19, NL: 0.21 };

export function priceFor(planId: PlanId, country: string): Money {
  const net = NET_CENTS[planId];
  if (net === undefined) throw new Error(`unknown plan ${planId}`);
  const vat = Math.round(net * (VAT[country] ?? 0));
  return fromCents(net + vat);
}
