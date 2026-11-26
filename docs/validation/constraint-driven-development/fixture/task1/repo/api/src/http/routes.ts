import type { FastifyInstance } from "fastify";
import { totalCents, validate, type Invoice } from "../domain/invoice";

export async function routes(app: FastifyInstance): Promise<void> {
  app.post("/invoices/total", async (request, reply) => {
    const { invoice, country } = request.body as { invoice: Invoice; country: string };
    const error = validate(invoice);
    if (error) {
      return reply.status(error.status).send(error);
    }
    return { total_cents: totalCents(invoice, country) };
  });
}
