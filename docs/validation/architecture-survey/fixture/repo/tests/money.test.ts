// tests/money.test.ts
import { add, allocate, format, fromCents, subtract } from "../src/money/money";

test("adds and subtracts cents", () => {
  expect(add(fromCents(150), fromCents(250))).toEqual(fromCents(400));
  expect(subtract(fromCents(150), fromCents(250))).toEqual(fromCents(-100));
});

test("allocate gives the remainder to the first share", () => {
  expect(allocate(fromCents(100), [1, 1, 1]).map((m) => m.cents)).toEqual([34, 33, 33]);
});

test("formats negative amounts", () => {
  expect(format(fromCents(-1234))).toBe("-$12.34");
});
