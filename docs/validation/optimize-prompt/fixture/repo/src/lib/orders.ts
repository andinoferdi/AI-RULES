export type Order = { id: string; customer: string; total: number; createdAt: string };

export async function listOrders(): Promise<Order[]> {
  const response = await fetch(`${process.env.API_URL}/orders`);
  return response.json();
}
