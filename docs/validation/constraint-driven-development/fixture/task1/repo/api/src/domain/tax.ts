const RATES: Record<string, number> = { NL: 0.21, DE: 0.19, US: 0 };

export function taxFor(subtotalCents: number, country: string): number {
  const rate = RATES[country];
  if (rate === undefined) {
    throw new Error(`No tax rate for ${country}`);
  }
  return Math.round(subtotalCents * rate);
}
