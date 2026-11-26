# Shelf

Shelf runs the Northside Tool Library, a volunteer-run library that lends hand and garden tools.
About 600 members borrow tools. About 25 volunteers staff the desk on Saturdays 9:00-13:00 and
Wednesdays 17:00-19:00.

## How it works today

- Members browse the catalog and place holds in the web app (`web/routes.ts`).
- Volunteers check items out and in at the desk in the same web app, signed in as volunteers.
- A loan lasts 14 days. A member may renew a loan once, and not at all while another member has a
  hold on that tool (`src/loans/service.ts`).
- When an item comes back and a hold is waiting, the member gets an email and has 3 days to collect
  the item (`src/holds/service.ts`).
- Every Friday at 22:00 a cron job writes `overdue.csv` to the shared volunteer drive
  (`src/reports/overdue.ts`, `deploy/crontab`). On Saturday the desk volunteer phones the members
  on that list.
- There are no late fees (`docs/adr/0001-no-late-fees.md`).

## Stack

Node 20, TypeScript, Express and PostgreSQL. Email goes through Postmark (`POSTMARK_TOKEN`). The
app runs on one small VM. One part-time volunteer developer maintains it.
