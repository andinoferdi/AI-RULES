# Glossary

**Customer**: a person or company that holds one or more subscriptions.
_Avoid_: user, account.

**Plan**: a priced offering (`basic`, `pro`, `team`) billed every month.
_Avoid_: tier, package.

**Subscription**: a customer's agreement to pay for one plan, with a current period that starts and
ends on calendar dates.
_Avoid_: membership.

**Renewal**: charging a subscription for its next period: price it, issue an invoice, move the
period forward, record a ledger entry and email the customer.
_Avoid_: rebill, recharge.

**Proration**: the part of a plan price that belongs to the days actually used in a period.
_Avoid_: partial charge.

**Invoice**: the record of an amount a customer owes for a period or a plan change.

**Ledger entry**: one signed movement on a customer's balance (renewal, refund or plan change),
with the balance after it.
_Avoid_: transaction (reserved for database transactions).

**Refund**: money returned against an invoice, never more than the invoice amount.
