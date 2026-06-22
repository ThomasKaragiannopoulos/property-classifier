"""
Compare predictions.csv against manual_baseline.csv.
Prints a row-by-row match/mismatch table and a summary.
"""

import csv
from pathlib import Path

PREDICTIONS = Path("predictions.csv")
BASELINE = Path("manual_baseline.csv")


def load_keyed(path: Path, id_field: str, value_field: str) -> dict[str, str]:
    with open(path, newline="", encoding="utf-8") as f:
        return {row[id_field]: row[value_field] for row in csv.DictReader(f)}


def main() -> None:
    predicted = load_keyed(PREDICTIONS, "id", "classified_category")
    expected = load_keyed(BASELINE, "listing_id", "category")

    all_ids = sorted(set(predicted) | set(expected))

    matches = 0
    mismatches = []

    col = "{:<30} {:<15} {:<15} {}"
    print(col.format("listing_id", "expected", "predicted", "match"))
    print("-" * 75)

    for lid in all_ids:
        exp = expected.get(lid, "MISSING")
        pred = predicted.get(lid, "MISSING")
        ok = exp == pred
        if ok:
            matches += 1
        else:
            mismatches.append(lid)
        print(col.format(lid[:30], exp, pred, "OK" if ok else "FAIL"))

    total = len(all_ids)
    print(f"\n{matches}/{total} correct")

    if mismatches:
        print(f"\nMismatches ({len(mismatches)}):")
        for lid in mismatches:
            print(f"  {lid}  expected={expected.get(lid)}  predicted={predicted.get(lid)}")


if __name__ == "__main__":
    main()
