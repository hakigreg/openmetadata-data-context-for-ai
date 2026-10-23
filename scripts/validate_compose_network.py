#!/usr/bin/env python3
"""Reject Compose configurations that publish demo services beyond loopback."""

from __future__ import annotations

import json
import sys
from typing import Any


LOOPBACK_ADDRESSES = {"127.0.0.1", "::1"}
INTERNAL_ONLY_SERVICES = {"elasticsearch", "mysql"}


def main() -> int:
    config: dict[str, Any] = json.load(sys.stdin)
    violations: list[str] = []

    for service_name, service in config.get("services", {}).items():
        ports = service.get("ports", [])
        if service_name in INTERNAL_ONLY_SERVICES and ports:
            violations.append(f"{service_name} must not publish host ports")

        for port in ports:
            host_ip = port.get("host_ip", "0.0.0.0")
            if host_ip not in LOOPBACK_ADDRESSES:
                published = port.get("published", "unknown")
                violations.append(
                    f"{service_name}:{published} binds to {host_ip}, not loopback"
                )

    if violations:
        raise RuntimeError("Unsafe Compose port publishing: " + "; ".join(violations))

    print("Compose host ports are restricted to loopback")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
