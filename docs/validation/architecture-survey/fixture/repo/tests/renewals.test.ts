// tests/renewals.test.ts
jest.mock("../src/renewals/RenewalValidator");
jest.mock("../src/renewals/RenewalPricing");
jest.mock("../src/renewals/RenewalRepoWrapper");
jest.mock("../src/renewals/RenewalNotifier");
jest.mock("../src/mail/SesMailer");
jest.mock("../src/ledger/ledger");
jest.mock("../src/subscriptions/loadSubscription");

import { RenewalNotifier } from "../src/renewals/RenewalNotifier";
import { RenewalPricing } from "../src/renewals/RenewalPricing";
import { RenewalRepoWrapper } from "../src/renewals/RenewalRepoWrapper";
import { RenewalValidator } from "../src/renewals/RenewalValidator";
import { renewNow } from "../src/routes/renewNow";
import { loadSubscription } from "../src/subscriptions/loadSubscription";

const sub = { id: "sub_1", customerId: "cus_1", email: "a@example.com", planId: "pro", customerCountry: "ID" };

function res() {
  const r: any = {};
  r.status = jest.fn(() => r);
  r.json = jest.fn(() => r);
  return r;
}

beforeEach(() => {
  (loadSubscription as jest.Mock).mockResolvedValue(sub);
  (RenewalValidator.prototype.isRenewable as jest.Mock).mockReturnValue(true);
  (RenewalPricing.prototype.amountFor as jest.Mock).mockReturnValue({ cents: 3219, currency: "USD" });
  (RenewalRepoWrapper.prototype.begin as jest.Mock).mockResolvedValue({});
  (RenewalRepoWrapper.prototype.insertInvoice as jest.Mock).mockResolvedValue("inv_1");
});

test("renewNow calls each step in order", async () => {
  const r = res();
  await renewNow({ params: { id: "sub_1" } } as any, r);
  expect(RenewalRepoWrapper.prototype.insertInvoice).toHaveBeenCalledWith({}, "sub_1", { cents: 3219, currency: "USD" });
  expect(RenewalRepoWrapper.prototype.advancePeriod).toHaveBeenCalled();
  expect(RenewalRepoWrapper.prototype.commit).toHaveBeenCalled();
  expect(RenewalNotifier.prototype.sendRenewalEmail).toHaveBeenCalledWith("a@example.com", "inv_1", { cents: 3219, currency: "USD" });
  expect(r.status).toHaveBeenCalledWith(201);
});

test("renewNow rejects a subscription that is not renewable", async () => {
  (RenewalValidator.prototype.isRenewable as jest.Mock).mockReturnValue(false);
  const r = res();
  await renewNow({ params: { id: "sub_1" } } as any, r);
  expect(RenewalRepoWrapper.prototype.begin).not.toHaveBeenCalled();
  expect(r.status).toHaveBeenCalledWith(409);
});
