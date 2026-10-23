#!/usr/bin/env python3
"""Obtain a short-lived JWT from the local OpenMetadata basic-auth endpoint."""

from __future__ import annotations

import base64
import json
import os
import sys
import urllib.error
import urllib.request


def main() -> int:
    host = os.getenv("OPENMETADATA_HOST_PORT", "http://localhost:8585/api").rstrip("/")
    email = os.getenv("OPENMETADATA_ADMIN_EMAIL", "admin@open-metadata.org")
    password = os.getenv("OPENMETADATA_ADMIN_PASSWORD", "admin")
    payload = json.dumps(
        {
            "email": email,
            "password": base64.b64encode(password.encode()).decode(),
        }
    ).encode()
    request = urllib.request.Request(
        f"{host}/v1/users/login",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            token = json.load(response).get("accessToken")
    except (urllib.error.URLError, json.JSONDecodeError) as exc:
        print(f"Unable to authenticate with OpenMetadata: {exc}", file=sys.stderr)
        return 1
    if not token:
        print("OpenMetadata did not return an access token", file=sys.stderr)
        return 1
    print(token)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
