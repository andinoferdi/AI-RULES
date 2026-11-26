# Checkpoint s1-cp3

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

## You

Charts and KPIs can mean many things, so let me ask it another way. If you didn't have to show this
to anyone, what would you want a volunteer to be able to do on a Saturday morning that they can't
do now? My guess is that it is about the overdue calls, since the CSV is the main thing the desk
uses.

## User

Honestly, it's the Saturday calls. The volunteer at the desk phones everyone on the overdue list,
and half the time the person already brought the tool back late Friday or that morning, so they get
annoyed. And when a member asks when a tool they want will be back, the volunteer has no idea how
long their reservation will take. That's what I want fixed.
