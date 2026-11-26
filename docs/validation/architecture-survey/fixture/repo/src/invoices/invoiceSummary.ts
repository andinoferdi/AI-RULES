// src/invoices/invoiceSummary.ts
import { Money, allocate, format } from "../money/money";

export interface SummaryLine {
  label: string;
  amount: string;
}

/** Split an invoice total across its seats for the invoice PDF. */
export function seatLines(total: Money, seats: { name: string; weight: number }[]): SummaryLine[] {
  const shares = allocate(total, seats.map((s) => s.weight));
  return seats.map((seat, i) => ({ label: seat.name, amount: format(shares[i]) }));
}
