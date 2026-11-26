# Changelog

## 1.8 (2026-11-10)

- Partner prices are rounded to whole rupiah after the markup (CAT-305).
- Products are de-duplicated per SKU and variant, comparing SKUs case-insensitively,
  because the partner feed lists some of our SKUs in lower case (CAT-311).
- The feed reader strips whitespace in every column.

## 1.7 (2026-10-14)

- Partner feed support with a configurable markup.
