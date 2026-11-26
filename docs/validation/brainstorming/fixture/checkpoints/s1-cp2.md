# Checkpoint s1-cp2

Conversation so far. Write your next message to the user.

## User

Can you build a dashboard for our volunteers?

## You

I looked at how the desk works today. Volunteers check items in and out in the web app
(`web/routes.ts`), and every Friday night a job writes `overdue.csv` to the shared drive for the
Saturday phone calls (`src/reports/overdue.ts`). Before I suggest what a dashboard should show:
what do volunteers need to do or decide that is hard for them right now?

## User

We want something modern and scalable, like a proper admin dashboard. You know, best practice for
this kind of app, with charts and KPIs.
