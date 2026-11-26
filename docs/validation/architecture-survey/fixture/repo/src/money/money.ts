// src/money/money.ts
export interface Money {
  cents: number;
  currency: "USD";
}

export function fromCents(cents: number, currency: "USD" = "USD"): Money {
  if (!Number.isInteger(cents)) throw new RangeError("cents must be an integer");
  return { cents, currency };
}

export function add(a: Money, b: Money): Money {
  sameCurrency(a, b);
  return fromCents(a.cents + b.cents, a.currency);
}

export function subtract(a: Money, b: Money): Money {
  sameCurrency(a, b);
  return fromCents(a.cents - b.cents, a.currency);
}

/** Split an amount by ratios; the rounding remainder goes to the first share. */
export function allocate(amount: Money, ratios: number[]): Money[] {
  const total = ratios.reduce((s, r) => s + r, 0);
  if (total <= 0) throw new RangeError("ratios must sum to a positive number");
  const shares = ratios.map((r) => Math.floor((amount.cents * r) / total));
  const remainder = amount.cents - shares.reduce((s, c) => s + c, 0);
  shares[0] += remainder;
  return shares.map((c) => fromCents(c, amount.currency));
}

export function format(m: Money): string {
  const sign = m.cents < 0 ? "-" : "";
  const abs = Math.abs(m.cents);
  return `${sign}$${Math.floor(abs / 100)}.${String(abs % 100).padStart(2, "0")}`;
}

function sameCurrency(a: Money, b: Money) {
  if (a.currency !== b.currency) throw new Error("currency mismatch");
}
