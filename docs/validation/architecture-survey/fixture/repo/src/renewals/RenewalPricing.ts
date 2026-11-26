// src/renewals/RenewalPricing.ts
import { Money } from "../money/money";
import { priceFor } from "../pricing/priceFor";
import { Subscription } from "../types";

export class RenewalPricing {
  amountFor(sub: Subscription): Money {
    return priceFor(sub.planId, sub.customerCountry);
  }
}
