import { expect, it } from "vitest";
import { taxFor } from "../src/domain/tax";

it("uses the German rate", () => {
  expect(taxFor(1000, "DE")).toBe(190);
});

it("throws for an unknown country", () => {
  expect(() => taxFor(1000, "XX")).toThrow("No tax rate");
});
