# ADR-0002: Pricing rules stay in their own folder

## Status
Accepted (2025-03)

## Context
Finance audits every change to plan prices and VAT rates. The audit tooling watches one folder and
requires a finance reviewer on any change inside it.

## Decision
All price and VAT rules live in `src/pricing/`. Other modules call `priceFor` and never embed
prices, VAT rates or rounding rules for prices.

## Consequences
- Do not merge pricing rules into renewals, plan changes or invoices, even when only one caller
  uses a rule.
- Changes to `src/pricing/` need a finance reviewer, so they are slower to land.
