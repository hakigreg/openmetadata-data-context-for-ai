#!/usr/bin/env sh
set -eu

version="${1:?OpenMetadata version is required}"
destination="${2:?Destination path is required}"
url="https://github.com/open-metadata/OpenMetadata/releases/download/${version}-release/docker-compose.yml"

mkdir -p "$(dirname "$destination")"
curl --fail --silent --show-error --location "$url" --output "$destination.tmp"
mv "$destination.tmp" "$destination"
printf 'Downloaded OpenMetadata %s Compose to %s\n' "$version" "$destination"
