#!/usr/bin/env sh
set -eu

health_url="${OPENMETADATA_HEALTH_URL:-http://localhost:8585/api/v1/system/version}"
attempts="${OPENMETADATA_WAIT_ATTEMPTS:-60}"

attempt=1
while [ "$attempt" -le "$attempts" ]; do
  if curl --fail --silent "$health_url" >/dev/null 2>&1; then
    printf 'OpenMetadata is ready at %s\n' "$health_url"
    exit 0
  fi
  printf 'Waiting for OpenMetadata (%s/%s)...\n' "$attempt" "$attempts"
  attempt=$((attempt + 1))
  sleep 5
done

printf 'OpenMetadata did not become ready at %s\n' "$health_url" >&2
exit 1
