# threejs-combat-animation

Build, fix and review character combat animations (melee strikes, bow shots, spell casts, skills, monster attacks, whole move sets) so they read like Diablo IV, Baldur's Gate 3 or Elden Ring and never stretch, lock, wring or break an arm, wrist or hand. A written standard with numbered rules, per-frame tests on the real skinned mesh, keys designed from upper-arm, forearm and blade intents, checks from every camera the player sees, two blind critics plus a blind A/B against the last release, and every critic claim verified against full-resolution frames and live-rig numbers. Use when creating or reworking any attack, skill or move set; when the user says arms, hands, wrists, elbows or weapons look stretched, weird, broken or wrong; when they ask for a standard, rules or tests for animations; or when they ask to score animations or get them to N out of 10.

This is an internal method bundled in `threejs-skills`, not an individual installer
choice or native skill. Read [GUIDE.md](GUIDE.md) for the method; its supporting
resources remain relative to this directory. Install the complete family:

```sh
ai-rules setup --host codex --capability threejs-skills --scope project --project-root . --source latest
```

Use "threejs-skills, specifically threejs-combat-animation" or let the family select by need.
With Andino, return evidence/results to its single task context. Preserve supplied
notices, observe project versions, and get task authorization for paid services.
Update the family through the existing CLI; modified/unmanaged targets are preserved.
