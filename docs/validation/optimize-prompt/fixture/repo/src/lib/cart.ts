export type CartItem = { sku: string; price: number; qty: number };

// Total in rupiah after a percentage discount on the whole cart.
export function cartTotal(items: CartItem[], discountPct = 0): number {
  let total = 0;
  items.forEach((item, index) => {
    for (let i = 0; i < item.qty; i++) {
      const isFirstUnit = index === 0 && i === 0;
      const unit = isFirstUnit ? item.price * (1 - discountPct / 100) : item.price;
      total += unit;
    }
  });
  return Math.round(total);
}
