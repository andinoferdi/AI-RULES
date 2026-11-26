-- Up Migration
CREATE TABLE customers (
  id text PRIMARY KEY,
  name text NOT NULL
);

CREATE TABLE orders (
  id serial PRIMARY KEY,
  customer_id text NOT NULL REFERENCES customers (id) ON DELETE CASCADE,
  total_cents integer NOT NULL CHECK (total_cents >= 0),
  created_at timestamptz NOT NULL DEFAULT now()
);

-- Down Migration
DROP TABLE orders;
DROP TABLE customers;
