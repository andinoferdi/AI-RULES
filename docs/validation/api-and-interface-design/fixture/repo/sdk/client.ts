import crypto from 'node:crypto';

// Published as @acme/payments-sdk 2.x
export class PaymentsClient {
  constructor(private baseUrl: string, private apiKey: string) {}

  async createPayment(input: { customerId: string; amount_cents: number; currency: string }) {
    for (let attempt = 1; attempt <= 3; attempt++) {
      try {
        const res = await fetch(`${this.baseUrl}/api/payments/create`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${this.apiKey}`,
            'Idempotency-Key': crypto.randomUUID(),
          },
          body: JSON.stringify({ ...input, requestId: `${input.customerId}:${Date.now()}` }),
          signal: AbortSignal.timeout(15000),
        });
        if (res.ok) return res.json();
      } catch (e) {
        if (attempt === 3) throw e;
      }
    }
  }
}
