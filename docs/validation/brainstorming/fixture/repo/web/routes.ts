import { Router } from "express";
import * as desk from "./desk";
import * as member from "./member";
import { requireMember, requireVolunteer } from "./auth";

export const routes = Router();

routes.get("/catalog", member.catalog);
routes.get("/me/loans", requireMember, member.loans);
routes.get("/me/holds", requireMember, member.holds);
routes.post("/me/holds", requireMember, member.placeHold);

routes.post("/desk/checkout", requireVolunteer, desk.checkout);
routes.post("/desk/checkin", requireVolunteer, desk.checkin);
routes.post("/desk/renew", requireVolunteer, desk.renew);
