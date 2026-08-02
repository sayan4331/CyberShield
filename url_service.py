"""Heuristic URL / phishing-pattern scanner.

Performs static, rule-based analysis of a URL's structure only. It does
not fetch the URL, execute anything, or call a live threat-intel API —
it looks for shapes commonly associated with phishing or obfuscated
links, for educational purposes. Not a replacement for a real
threat-intelligence service.
"""
import re

from sqlalchemy.orm import Session

from app.services import history_service
from app.utils.validators import is_ip_host, normalize_url

SHORTENER_DOMAINS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd",
    "buff.ly", "rebrand.ly", "cutt.ly", "shorte.st",
}

SUSPICIOUS_TLDS = {
    "zip", "mov", "top", "xyz", "gq", "tk", "ml", "cf", "ga", "work",
    "click", "link", "loan", "download",
}

SENSITIVE_KEYWORDS = [
    "login", "verify", "secure", "account", "update", "confirm",
    "signin", "banking", "password", "wallet", "invoice", "billing",
]

BRAND_LOOKALIKES = [
    "paypal", "amazon", "apple", "microsoft", "google", "netflix",
    "facebook", "instagram", "bankofamerica", "chase", "wellsfargo",
]


def analyze_url(raw_url: str) -> dict:
    url = raw_url.strip()
    flags: list[str] = []
    score = 0

    parts = normalize_url(url)
    host = parts.hostname or ""
    labels = host.split(".") if host else []

    if not host:
        return {"url": url, "domain": None, "risk_score": 100, "verdict": "Invalid",
                "flags": ["Could not parse a valid host from the input"]}

    if parts.scheme == "http":
        score += 15
        flags.append("Uses unencrypted HTTP instead of HTTPS")

    if is_ip_host(host):
        score += 30
        flags.append("Host is a raw IP address rather than a domain name")

    if "@" in url:
        score += 25
        flags.append("Contains '@', which can hide the real destination host")

    if len(url) > 90:
        score += 10
        flags.append("Unusually long URL")

    if len(labels) > 4:
        score += 15
        flags.append(f"Excessive number of subdomains ({len(labels)} labels)")

    tld = labels[-1].lower() if labels else ""
    if tld in SUSPICIOUS_TLDS:
        score += 15
        flags.append(f"Top-level domain '.{tld}' is frequently abused for phishing/spam")

    if host.lower() in SHORTENER_DOMAINS:
        score += 15
        flags.append("Known URL-shortener domain (destination is hidden)")

    if re.search(r"xn--", host, re.IGNORECASE):
        score += 25
        flags.append("Punycode-encoded host — possible homograph/lookalike domain")

    path_and_query = (parts.path or "") + "?" + (parts.query or "")
    hits = [kw for kw in SENSITIVE_KEYWORDS if kw in path_and_query.lower()]
    if hits:
        score += min(5 * len(hits), 20)
        flags.append(f"Contains sensitive-action keywords: {', '.join(sorted(set(hits)))}")

    registrable = ".".join(labels[-2:]) if len(labels) >= 2 else host
    for brand in BRAND_LOOKALIKES:
        if brand in host.lower() and brand not in registrable.lower().split(".")[0]:
            score += 20
            flags.append(f"Brand name '{brand}' appears outside the main domain (possible impersonation)")
            break
        if brand in host.lower() and re.search(rf"{brand}[-0-9]", host.lower()):
            score += 20
            flags.append(f"Domain resembles '{brand}' with extra characters (typosquatting pattern)")
            break

    if re.search(r"\d{4,}", host):
        score += 10
        flags.append("Domain contains an unusually long digit sequence")

    score = max(0, min(100, score))
    if score >= 60:
        verdict = "High Risk"
    elif score >= 35:
        verdict = "Medium Risk"
    elif score >= 15:
        verdict = "Low Risk"
    else:
        verdict = "Likely Safe"

    if not flags:
        flags.append("No common phishing/obfuscation patterns detected")

    return {"url": url, "domain": host, "risk_score": score, "verdict": verdict, "flags": flags}


def scan_and_log(db: Session, url: str) -> dict:
    result = analyze_url(url)
    history_service.log_scan(
        db, scan_type="url", label=result["verdict"], score=result["risk_score"],
        subject=result["domain"] or result["url"][:255],
        details={"flags": result["flags"]},
    )
    return result
