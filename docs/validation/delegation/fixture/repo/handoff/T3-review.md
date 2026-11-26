# Task 3 review (agent R)

## Spec compliance

❌ Issues found:

- `src/shopline/auth/tokens.py:52`: `expires_in` defaults to 900; the plan's Task 3 says 600.

⚠️ Cannot verify from diff: an expired link is refused by the `export` command with a clear
message. That code is not in this diff.

## Strengths

Claims follow the `sign_session` format; order ids are part of the signed body, so a token
cannot be reused for other orders.

## Issues

### Critical

- `src/shopline/auth/tokens.py:61`: `verify_download` compares the MAC with `==`. A timing
  attack can recover a valid signature. Use `hmac.compare_digest`.

### Important

- `src/shopline/auth/tokens.py:66`: expiry is checked against `exp + LEEWAY_SECONDS`, and
  `LEEWAY_SECONDS` is 3600, so a link stays valid for 75 minutes. The plan says to reuse
  `LEEWAY_SECONDS`, so this is plan-mandated.

### Minor

- `src/shopline/auth/tokens.py:48`: parameter name `oids` is unclear; `order_ids` matches
  the plan.

## Tests

The implementer reports the new tests pass; not re-run.

## Assessment

Task quality: Needs fixes. The timing-unsafe comparison must be fixed before this ships.
