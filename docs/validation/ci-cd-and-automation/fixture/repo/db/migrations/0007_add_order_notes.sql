-- Up Migration
ALTER TABLE orders ADD COLUMN notes text;

-- Down Migration
ALTER TABLE orders DROP COLUMN notes;
