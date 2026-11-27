# Hookdesk

Hookdesk sends signed event webhooks to our customers' servers. Each customer is a
tenant; people belong to one tenant with one role: `owner`, `admin` or `member`.

- Owners and admins manage the tenant's webhook settings (URL and signing secret).
- Members can read invoices and see whether a webhook is configured.

`hookdesk.app.handle(request)` routes a `Request` to a handler and returns a `Response`.
The HTTP front end (not in this repository) authenticates the session and fills
`Request.user_id`; handlers must do their own authorization. `data/tenants.json` holds
the development data that `hookdesk.store` loads.

Outbound HTTP goes through `hookdesk.net`. Tests never touch the network: patch
`hookdesk.net.resolve` and `hookdesk.net.post_json` with fakes.

Every webhook delivery is a JSON `POST` signed with the tenant's secret
(`X-Hookdesk-Signature`, see `hookdesk.signing`). Hookdesk runs in a cloud VPC next to
the billing database and the internal admin API.

Tests: `python -m unittest discover -s tests -t .`
