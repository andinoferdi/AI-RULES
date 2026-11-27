import { cartTotal } from '@/lib/cart';

export default function CheckoutPage() {
  const items = [{ sku: 'KOPI-1', price: 50000, qty: 2 }];
  return (
    <main>
      <h1>Checkout</h1>
      <p>Total: Rp {cartTotal(items, 10).toLocaleString('id-ID')}</p>
      <button type="submit">Bayar</button>
    </main>
  );
}
