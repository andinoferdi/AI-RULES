import { describe, expect, it } from 'vitest';

const cents = (amount: number) => Math.round(amount * 100);

describe('cents', () => {
  it('rounds to whole cents', () => {
    expect(cents(10.005)).toBe(1001);
  });
});
