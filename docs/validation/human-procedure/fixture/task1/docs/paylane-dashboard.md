# PayLane dashboard steps

Checked by Dewi against the live dashboard on 2026-11-18. Test mode only; production keys come
later.

## API keys

1. Open https://dashboard.paylane.example/test/developers/api-keys (log in if asked).
2. The **Publishable key** row shows a key that starts with `pk_test_`. Click **Copy**.
3. On the **Secret key** row click **Reveal test key**, then **Copy**. It starts with
   `sk_test_`. PayLane shows it again later, so nothing is lost if you close the page.

## Webhook signing secret

The webhook endpoint for production is `https://kedai.example/webhooks/paylane`.

1. Open https://dashboard.paylane.example/test/developers/webhooks.
2. Click **Add endpoint**. Endpoint URL: `https://kedai.example/webhooks/paylane`. Events:
   tick `payment.succeeded` and `payment.refunded`. Click **Add endpoint** at the bottom.
   This creates the endpoint in PayLane; adding it twice creates two endpoints that both
   receive events.
3. On the new endpoint's page, under **Signing secret**, click **Reveal**, then **Copy**. It
   starts with `whsec_`.
