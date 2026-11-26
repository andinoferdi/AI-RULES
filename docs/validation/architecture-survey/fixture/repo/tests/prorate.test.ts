// tests/prorate.test.ts
import { fromCents } from "../src/money/money";
import { prorate } from "../src/proration/prorate";

describe("prorate", () => {
  const price = fromCents(3000);

  test("charges the used share of the period", () => {
    expect(prorate(price, 10, 30)).toEqual(fromCents(1000));
  });

  test("rounds to the nearest cent", () => {
    expect(prorate(fromCents(1000), 1, 3)).toEqual(fromCents(333));
  });

  test("clamps days used to the period", () => {
    expect(prorate(price, 45, 30)).toEqual(price);
    expect(prorate(price, -2, 30)).toEqual(fromCents(0));
  });

  test("rejects an empty period", () => {
    expect(() => prorate(price, 1, 0)).toThrow(RangeError);
  });
});
