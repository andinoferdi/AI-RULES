import { listOrders } from '@/lib/orders';

export default async function AdminOrdersPage() {
  const orders = await listOrders();
  return (
    <table>
      <tbody>
        {orders.map((order) => (
          <tr key={order.id}><td>{order.id}</td><td>{order.customer}</td><td>{order.total}</td></tr>
        ))}
      </tbody>
    </table>
  );
}
