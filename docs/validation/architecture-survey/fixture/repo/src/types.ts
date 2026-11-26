// src/types.ts
export type PlanId = "basic" | "pro" | "team";

export interface Subscription {
  id: string;
  customerId: string;
  email: string;
  customerCountry: string;
  planId: PlanId;
  status: "active" | "past_due" | "cancelled";
  cancelAtPeriodEnd: boolean;
  currentPeriodStart: Date;
  currentPeriodEnd: Date;
  pausedDays: number;
}
