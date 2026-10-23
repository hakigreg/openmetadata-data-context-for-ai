"""Small standard-library client for the local OpenMetadata demo API."""

from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


class OpenMetadataClient:
    def __init__(self) -> None:
        self.base_url = os.getenv(
            "OPENMETADATA_HOST_PORT", "http://localhost:8585/api"
        ).rstrip("/")
        self.token = os.getenv("OPENMETADATA_JWT_TOKEN") or self._login()

    def _login(self) -> str:
        email = os.getenv("OPENMETADATA_ADMIN_EMAIL", "admin@open-metadata.org")
        password = os.getenv("OPENMETADATA_ADMIN_PASSWORD", "admin")
        response = self.request(
            "POST",
            "/v1/users/login",
            {
                "email": email,
                "password": base64.b64encode(password.encode()).decode(),
            },
            authenticated=False,
        )
        token = response.get("accessToken")
        if not token:
            raise RuntimeError("OpenMetadata login did not return an access token")
        return str(token)

    def request(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | list[dict[str, Any]] | None = None,
        *,
        authenticated: bool = True,
        content_type: str = "application/json",
    ) -> dict[str, Any] | list[Any] | str:
        headers = {"Accept": "application/json"}
        if payload is not None:
            headers["Content-Type"] = content_type
        if authenticated:
            headers["Authorization"] = f"Bearer {self.token}"
        request = urllib.request.Request(
            f"{self.base_url}{path}",
            data=json.dumps(payload).encode() if payload is not None else None,
            headers=headers,
            method=method,
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                body = response.read()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode(errors="replace")
            raise RuntimeError(f"{method} {path} failed ({exc.code}): {detail}") from exc
        if not body:
            return {}
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return body.decode(errors="replace")

    def get_by_name(self, collection: str, fqn: str, fields: str = "") -> dict[str, Any]:
        encoded_fqn = urllib.parse.quote(fqn, safe="")
        suffix = f"?fields={urllib.parse.quote(fields)}" if fields else ""
        response = self.request("GET", f"/v1/{collection}/name/{encoded_fqn}{suffix}")
        if not isinstance(response, dict):
            raise RuntimeError(f"Unexpected response for {collection} {fqn}")
        return response
