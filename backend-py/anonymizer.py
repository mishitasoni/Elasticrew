"""
anonymizer.py
Resume anonymization logic — three-layer PII removal:

  Layer 1 — Field drop     : known PII keys deleted from dicts
  Layer 2 — Pattern redact : regex masks applied to every string value
  Layer 3 — Name scrub     : candidate's own name tokens removed from free text
"""

from __future__ import annotations
import re
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

# ── 1. PII FIELD NAMES ────────────────────────────────────────────────────────
PII_FIELDS: frozenset[str] = frozenset({
    "name", "full_name", "first_name", "last_name", "preferred_name",
    "email", "email_address",
    "phone", "phone_number", "mobile", "mobile_number", "fax",
    "address", "address_line1", "address_line2", "street_address",
    "city", "state", "province", "region",
    "zip_code", "post_code", "postal_code",
    "country", "country_code", "nationality", "citizenship",
    "date_of_birth", "dob", "birth_date", "age",
    "gender", "sex", "pronouns",
    "photo", "avatar", "profile_picture", "headshot",
    "linked_in", "linked_in_url", "github", "github_url",
    "twitter", "twitter_handle", "instagram",
    "portfolio", "portfolio_url", "website", "personal_website",
    "passport_number", "ssn", "national_id", "tax_id", "employee_id",
    "ip_address", "device_id", "location", "coordinates",
    # camelCase variants (for any JS-style keys that sneak in)
    "fullName", "firstName", "lastName", "preferredName",
    "emailAddress", "phoneNumber", "mobileNumber",
    "addressLine1", "addressLine2", "streetAddress",
    "zipCode", "postCode", "postalCode", "countryCode",
    "dateOfBirth", "birthDate", "profilePicture",
    "linkedIn", "linkedInUrl", "githubUrl", "twitterHandle",
    "portfolioUrl", "personalWebsite",
    "passportNumber", "nationalId", "taxId", "employeeId",
    "ipAddress", "deviceId",
})

# ── 2. INLINE PII PATTERNS ────────────────────────────────────────────────────
_PII_PATTERNS: list[tuple[re.Pattern, str]] = [
    # Email
    (re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"), "[EMAIL REDACTED]"),
    # Phone — international and US local
    (re.compile(
        r"(\+\d[\d\s\-().]{7,}\d"
        r"|\b(?:\(\d{3}\)[\s\-]?\d{3}[\s\-]\d{4}"
        r"|\d{3}[\s\-]\d{3}[\s\-]\d{4}))\b"
    ), "[PHONE REDACTED]"),
    # Social / personal profile URLs
    (re.compile(
        r"https?://(www\.)?(linkedin|github|twitter|instagram|facebook|behance|dribbble)\.com/\S+",
        re.IGNORECASE,
    ), "[PROFILE URL REDACTED]"),
    # Any remaining URL
    (re.compile(r"https?://\S+"), "[URL REDACTED]"),
    # US zip codes
    (re.compile(r"\b\d{5}(-\d{4})?\b"), "[ZIP REDACTED]"),
    # SSN
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[ID REDACTED]"),
]


def redact_text(text: str) -> str:
    """Apply all PII regex patterns to a string, returning the masked result."""
    for pattern, replacement in _PII_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def _build_name_regex(raw_name: str) -> re.Pattern | None:
    """
    Build a case-insensitive word-boundary regex from the candidate's name tokens.
    Tokens shorter than 3 chars are skipped to avoid false positives.
    Returns None if no usable tokens found.
    """
    if not raw_name:
        return None
    tokens = [
        re.escape(t)
        for t in re.split(r"\s+", raw_name.strip())
        if len(re.sub(r"[^a-zA-Z'-]", "", t)) >= 3
    ]
    if not tokens:
        return None
    return re.compile(r"\b(" + "|".join(tokens) + r")\b", re.IGNORECASE)


def _anonymize_value(value: Any, name_re: re.Pattern | None) -> Any:
    """
    Recursively walk a value:
      - dicts  → drop PII keys, recurse on values
      - lists  → recurse on each element
      - str    → redact patterns, then scrub name tokens
      - other  → return unchanged
    """
    if isinstance(value, dict):
        return {
            k: _anonymize_value(v, name_re)
            for k, v in value.items()
            if k not in PII_FIELDS
        }
    if isinstance(value, list):
        return [_anonymize_value(item, name_re) for item in value]
    if isinstance(value, str):
        result = redact_text(value)
        if name_re:
            result = name_re.sub("[NAME REDACTED]", result)
        return result
    return value


def anonymize_resume(candidate: dict) -> dict:
    """
    Return a new dict with all PII removed and inline patterns masked.
    The original dict is NOT mutated.

    Raises ValueError for non-dict input.
    """
    if not isinstance(candidate, dict):
        raise ValueError("anonymize_resume: candidate must be a dict")

    raw_name = candidate.get("name") or candidate.get("full_name") or ""
    name_re  = _build_name_regex(raw_name)

    anon = _anonymize_value(deepcopy(candidate), name_re)
    anon["_anonymized"]    = True
    anon["_anonymized_at"] = datetime.now(timezone.utc).isoformat()
    return anon


def anonymize_batch(candidates: list[dict]) -> list[dict]:
    """Anonymize a list of candidate records."""
    if not isinstance(candidates, list):
        raise ValueError("anonymize_batch: candidates must be a list")
    return [anonymize_resume(c) for c in candidates]
