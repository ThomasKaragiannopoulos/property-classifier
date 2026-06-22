import csv
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from classify import classify
from ingest import extract_text, get_listing_id, load_listings

load_dotenv()

INPUT = Path("listings.csv")
OUTPUT = Path("predictions.csv")

RESULT_FIELDS = ["classified_category", "confidence", "reasoning"]


def main() -> None:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not set.", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(api_key=api_key)
    rows = load_listings(INPUT)
    print(f"Loaded {len(rows)} listings.\n")

    results = []
    for i, row in enumerate(rows):
        listing_id = get_listing_id(row, i)
        listing_text = extract_text(row)

        print(f"[{i + 1}/{len(rows)}] {listing_id} ...", end=" ", flush=True)
        result = classify(client, listing_id, listing_text)
        print(f"{result.category} ({result.confidence})")

        out_row = dict(row)
        out_row["classified_category"] = result.category
        out_row["confidence"] = result.confidence
        out_row["reasoning"] = result.reasoning
        results.append(out_row)

    original_fields = list(rows[0].keys())
    fieldnames = original_fields + RESULT_FIELDS

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(results)

    print(f"\nPredictions written to {OUTPUT}")


if __name__ == "__main__":
    main()
