import type { HttpError } from "../http/errors";
import { taxFor } from "./tax";

export interface LineItem {
  description: string;
  quantity: number;
  unitCents: number;
}

export interface Invoice {
  id: string;
  customerId: string;
  currency: "EUR" | "USD";
  lines: LineItem[];
}

export function subtotalCents(invoice: Invoice): number {
  return invoice.lines.reduce((sum, line) => sum + line.quantity * line.unitCents, 0);
}

export function totalCents(invoice: Invoice, country: string): number {
  const subtotal = subtotalCents(invoice);
  return subtotal + taxFor(subtotal, country);
}

// Returned to the route so it can answer 422 without validating again.
export function validate(invoice: Invoice): HttpError | null {
  if (invoice.lines.length === 0) {
    return { status: 422, code: "invoice_empty", message: "An invoice needs at least one line" };
  }
  return null;
}
