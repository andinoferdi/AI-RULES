import Fastify from "fastify";
import { routes } from "./http/routes";

const app = Fastify();
await app.register(routes);
await app.listen({ port: Number(process.env.PORT ?? 3000) });
