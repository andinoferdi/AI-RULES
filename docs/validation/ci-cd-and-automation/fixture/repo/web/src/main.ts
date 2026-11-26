const customer = new URLSearchParams(location.search).get('customer');
const table = document.querySelector<HTMLTableElement>('#orders')!;

if (customer) {
  const orders: { id: number; total_cents: number }[] = await (await fetch(`/api/customers/${customer}/orders`)).json();
  for (const order of orders) {
    const row = table.insertRow();
    row.insertCell().textContent = String(order.id);
    row.insertCell().textContent = (order.total_cents / 100).toFixed(2);
  }
}
