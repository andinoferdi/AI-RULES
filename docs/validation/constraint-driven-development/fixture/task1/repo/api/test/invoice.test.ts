import { describe, expect, it } from "vitest";
import { subtotalCents, totalCents, validate, type Invoice } from "../src/domain/invoice";

const invoice: Invoice = {
  id: "inv_1",
  customerId: "cus_1",
  currency: "EUR",
  lines: [
    { description: "Hosting", quantity: 2, unitCents: 500 },
    { description: "Support", quantity: 1, unitCents: 0 },
  ],
};

describe("invoice", () => {
  it("adds line totals", () => {
    expect(subtotalCents(invoice)).toBe(1000);
  });

  it("adds Dutch VAT", () => {
    const total = totalCents(invoice, "NL");
    expect(total).toBe(1210);
  });

  it("rejects an empty invoice", () => {
    expect(validate({ ...invoice, lines: [] })?.code).toBe("invoice_empty");
  });
});
