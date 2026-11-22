# Frontend runtime stability

Read only for UI/runtime symptoms in the actual target. These diagnostic principles
normalize user field notes; symptoms suggest hypotheses, not a proven cause. First
identify the browser/device, input type, framework if any, runtime owners and exact
reproduction. A Python service without UI does not need this reference.

## Symptom vocabulary

| Human alias | Engineering category | Discriminating evidence |
| --- | --- | --- |
| flickering / kedip | Rendering and compositing instability | Correlate flashes with DOM/state changes, paint/layer activity, opacity, asset loading and interaction. |
| kejang / guncang | Scroll/input contention | Compare intended input direction, nested overflow, event handling and actual scroll travel. |
| lag / 30 FPS | Runtime/animation performance contention | Trace scripting, layout, paint/compositing and initialization in the affected time window. |
| trampolin / mantul | Layout/scroll synchronization instability | Correlate unexpected reversals with layout shifts, mount, resize and position-restoring work. |

The categories overlap. Flicker can involve logic or loading, and slow frames can
reflect device/power behavior as well as workload. A reversal is not automatically
a defect: distinguish intentional input reversal, elastic overscroll and snapping.

## Rendering and compositing

Reproduce repeated taps/hover/scroll and inspect whether the element disappears,
becomes transparent or reveals a lower layer. Examine relevant transforms, filters,
opacity, stacking contexts and state churn. Compare with the specific effect
disabled to narrow the cause; do not apply CSS fixes to every component.

If evidence implicates transparent layer transitions, evaluate opaque backing,
stable layer ownership or an appropriate stacking/backface change. These can alter
transparency, clipping and depth, so preserve the intended visual contract and
compare before/after. Do not add permanent will-change or 3D promotion everywhere;
layer memory and rendering costs can increase. Batch redundant visual writes and
reduce proven state churn using the target's native patterns, without assuming React.

## Scroll and input ownership

Map which code/native scroller handles each axis and which listeners prevent default
or stop propagation. Measure actual overflow; inspect touch-action, overflow,
overscroll behavior and snap rules at the nested scroller and its ancestors.
Test empty/short lists, overflowed lists and their start/end boundaries, with wheel
and touch separately. Protect keyboard navigation and intended carousel gestures.

If a scroll library exists, verify its installed version, configuration and current
official behavior before changing prevent attributes, tickers or snap integration.
Lenis is an example, not a prerequisite. Removing input interception or changing
snap can help only when evidence connects it to the failure and intended behavior
allows the change. Do not universally disable nested scrolling or snapping.

## Runtime and animation work

Profile the failing interaction window, including image decode, library startup,
layout work and other concurrent tasks. Compare entry animation with later scroll
animation to localize contention rather than concluding the entire page is slow.
Transforms/opacity may still be expensive with large filtered surfaces; property
names alone do not prove compositor-only or cheap execution.

Where measurement supports it, simplify large blur/shadow effects, reduce redundant
layout writes, or separate optional initialization from critical interaction.
A gradient may approximate a glow but is not universally equivalent or free.
Avoid copying fixed startup delays; derive scheduling from actual dependencies and
readiness while preserving immediate interaction. Compare frame distributions and
visual output on representative devices, including reduced-motion behavior.

## Layout and scroll synchronization

Trace document/section size and scroll position around deferred mounts, fonts,
images and data arrival. Correlate resize/refresh calls with unexpected movement;
correlation is a lead, so isolate redundant calls or competing position writers.
Distinguish layout shifts and native anchoring from library synchronization faults.

Reserve stable asset dimensions when appropriate. Avoid refreshes for events that
do not change relevant geometry. Give required synchronization a clear owner and
coalesce duplicate work without delaying necessary updates indefinitely. Match
placeholders to measured responsive layout; tune preload distance only with evidence
of timing/resource tradeoffs. A double animation frame or fixed debounce does not
guarantee all fonts, images and asynchronous content have settled.

## Historical cases from the supplied notes

These are reported cases from one portfolio project, not verified facts about the
current target or prescriptions for every site. Original project paths, event names,
commit IDs and timing constants are deliberately not carried into the method.

- **Flickering:** a mobile 3D card exposed a fixed translucent hero through transparent
  layers during interaction. The notes report opaque backing, stable layer treatment
  and reduced state churn. Transfer the layering hypothesis and shared-primitive
  verification, not the assumption that every page has that hero structure.
- **Kejang:** Lenis interception on non-overflowing lists and a horizontal carousel
  reportedly trapped vertical gestures. Overflow-aware handling and revised snap/
  input ownership helped. Recheck library/version behavior and both axes locally.
- **Lag:** large animated glows/shadows, width animation and several startup tasks
  overlapped in an entry window. The notes report simpler effects and rescheduling
  optional work. Transfer profiling of simultaneous costs, not their delay values
  or claimed visual equivalence.
- **Trampolin:** wrapper and child components repeatedly requested Lenis/ScrollTrigger
  synchronization during mount and fixed-size image loads. The notes report removing
  redundant child requests while retaining required layout synchronization. Transfer
  ownership and geometry checks, not a universal ban on child-triggered refresh.

## Verification and cleanup

Repeat the original interaction, first-load/fast-scroll case and affected shared
primitives. Check nested gestures, focus/keyboard, responsive layout and reduced
motion as relevant. Inspect listeners, observers, timers and animation loops across
mount/unmount or navigation; remove temporary probes. Use real devices when the
failure depends on their GPU/input behavior and label emulation limitations.
Use native lint/build checks in addition to runtime evidence. No visual or speed
claim is proven by lint, build success or the mere presence of a library CSS class.
