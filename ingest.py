import ast
import csv
from pathlib import Path

# Fields that carry useful classification signal
TEXT_FIELDS = [
    "summary",
    "displayAddress",
    "detailedDescription",
    "description",
    "useClass",
    "propertySubType",
    "pageTitle",
]


def load_listings(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_key_features(raw: str) -> list[str]:
    """Parse keyFeatures, which is stored as a stringified Python list."""
    if not raw or not raw.strip():
        return []
    try:
        result = ast.literal_eval(raw)
        if isinstance(result, list):
            return [str(item) for item in result if item]
    except (ValueError, SyntaxError):
        pass
    return [raw.strip()]


def extract_text(row: dict) -> str:
    """Flatten a listing row into a single text block for the LLM."""
    parts = []

    for field in TEXT_FIELDS:
        value = row.get(field, "").strip()
        if value:
            parts.append(f"{field}: {value}")

    features = parse_key_features(row.get("keyFeatures", ""))
    if features:
        parts.append("keyFeatures: " + "; ".join(features))

    return "\n".join(parts) if parts else "(no usable listing text)"


def get_listing_id(row: dict, index: int) -> str:
    raw = row.get("id", "").strip()
    return raw if raw else f"row_{index + 1}"
