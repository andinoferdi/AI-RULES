#!/usr/bin/env bash
# Waits until Postgres on localhost:5432 accepts connections (up to 10 tries, 2 s apart).
set -u
for i in $(seq 1 10); do
  if pg_isready -h localhost -p 5432 -U postgres; then
    exit 0
  fi
  echo "postgres not ready yet, retrying ($i/10)"
  sleep 2
done
echo "postgres did not become ready" >&2
exit 1
