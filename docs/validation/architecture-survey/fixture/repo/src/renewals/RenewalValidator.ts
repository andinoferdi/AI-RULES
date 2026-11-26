// src/renewals/RenewalValidator.ts
import { Subscription } from "../types";

export class RenewalValidator {
  isRenewable(sub: Subscription): boolean {
    return sub.status === "active" && !sub.cancelAtPeriodEnd;
  }
}
