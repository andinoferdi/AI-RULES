// src/proration/prorate.ts
import { Money, fromCents } from "../money/money";

/**
 * Charge for the used part of a period. Pure, so it is easy to test (tests/prorate.test.ts).
 * daysUsed is clamped to [0, daysInPeriod].
 */
export function prorate(amount: Money, daysUsed: number, daysInPeriod: number): Money {
  if (daysInPeriod <= 0) throw new RangeError("daysInPeriod must be positive");
  const used = Math.max(0, Math.min(daysUsed, daysInPeriod));
  return fromCents(Math.round((amount.cents * used) / daysInPeriod), amount.currency);
}
