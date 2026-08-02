"""Validation and normalization helpers shared across services."""
import ipaddress
import re
from urllib.parse import SplitResult, urlsplit


def normalize_url(raw_url: str) -> SplitResult:
    """Ensure the URL has a scheme so urlsplit parses the host correctly."""
    url = raw_url.strip()
    target = url if re.match(r"^[a-zA-Z]+://", url) else f"http://{url}"
    return urlsplit(target)


def is_ip_host(host: str) -> bool:
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def is_non_empty(value: str) -> bool:
    return bool(value and value.strip())
