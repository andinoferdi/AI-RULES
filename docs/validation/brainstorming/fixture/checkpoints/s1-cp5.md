# Checkpoint s1-cp5

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

## You

That is much clearer: the overdue list is out of date by the time the calls start, and the desk
cannot tell a member when a tool will come back. A few decisions before I suggest how to build it:

1. Should the call list reflect returns up to the moment the volunteer looks at it, instead of
   Friday night? I recommend yes, because the complaint is calls about tools already returned.
2. You said "reservation". In Shelf that is a Hold, a member's place in the queue for a tool. I will
   call it a Hold. All right?
3. Should members also see the expected return date on their own Holds page, or only volunteers at
   the desk?
4. Should the Friday CSV keep running for now? I recommend yes, until volunteers trust the new list.

## User

1 yes. 2 yes, it's a hold. 3 whatever you think. 4 yes.

## You

Thanks. For 3 I will keep it to the desk for now: members can still ask at the desk, and we can add
the date to their Holds page once the dates prove reliable. Here are three ways to build it:

- A. A desk page in the existing web app that reads open loans live, and for each tool with a Hold
  shows when its first item is due back. Small change, same database and volunteer login; a
  volunteer has to open the page.
- B. Keep the CSV but regenerate it every 15 minutes on Saturday mornings. Least change for
  volunteers, but it is still a file that goes stale, and it does not answer the Hold question.
- C. Text overdue members automatically on Saturday morning instead of phoning. Removes calls, but
  the library has no SMS provider, and it changes how the library talks to members.

I recommend A. Which way do you want to go?

## User

A, and desk only is fine. Looks good, write it up so we can get started.
