import { describe, expect, it } from 'vitest';
import { cartTotal } from './cart';

describe('cartTotal', () => {
  it('sums items without a discount', () => {
    expect(cartTotal([{ sku: 'A', price: 50000, qty: 2 }])).toBe(100000);
  });
});
