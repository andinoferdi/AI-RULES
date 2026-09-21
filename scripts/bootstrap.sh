#!/usr/bin/env sh
set -eu
: "${AI_RULES_RELEASE_BASE_URL:=https://github.com/andinoferdi/AI-RULES/releases/latest/download}"
case "$(uname -s):$(uname -m)" in
  Darwin:arm64) asset="ai-rules-macos-arm64" ;;
  Linux:x86_64) asset="ai-rules-linux-x64" ;;
  *) echo "unsupported platform: $(uname -s) $(uname -m)" >&2; exit 2 ;;
esac
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
curl --fail --location --silent --show-error "$AI_RULES_RELEASE_BASE_URL/$asset" -o "$tmp/$asset"
curl --fail --location --silent --show-error "$AI_RULES_RELEASE_BASE_URL/SHA256SUMS" -o "$tmp/SHA256SUMS"
expected="$(awk -v name="$asset" '$2 == name {print $1}' "$tmp/SHA256SUMS")"
if command -v sha256sum >/dev/null 2>&1; then
  actual="$(sha256sum "$tmp/$asset" | awk '{print $1}')"
elif command -v shasum >/dev/null 2>&1; then
  actual="$(shasum -a 256 "$tmp/$asset" | awk '{print $1}')"
else
  echo "no SHA-256 utility available (need sha256sum or shasum)" >&2
  exit 2
fi
[ "$actual" = "$expected" ] || { echo "checksum verification failed for $asset" >&2; exit 1; }
install_dir="${AI_RULES_INSTALL_DIR:-$HOME/.local/bin}"
mkdir -p "$install_dir"
install "$tmp/$asset" "$install_dir/ai-rules"
exec "$install_dir/ai-rules" setup "$@"
