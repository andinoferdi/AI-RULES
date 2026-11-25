CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  email TEXT NOT NULL,
  phone TEXT,
  push_token TEXT,
  prefs JSONB NOT NULL DEFAULT '{}'
);

CREATE TABLE payments (
  id BIGSERIAL PRIMARY KEY,
  request_id TEXT,
  customer_id BIGINT NOT NULL REFERENCES users(id),
  amount_cents INTEGER NOT NULL,
  currency CHAR(3) NOT NULL,
  charge_id TEXT,
  status TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE payment_methods (
  id BIGSERIAL PRIMARY KEY,
  customer_id BIGINT NOT NULL REFERENCES users(id),
  label TEXT NOT NULL,
  card_token TEXT NOT NULL,
  is_default BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE notifications (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users(id),
  channel TEXT NOT NULL,
  template TEXT NOT NULL,
  sent_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
