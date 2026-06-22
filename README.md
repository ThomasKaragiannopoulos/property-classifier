# Property Classifier

Classifies commercial property listings into **Nursery**, **SEN School**, **Food Store**, or **None** using GPT-5 with structured outputs.

---

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # add your OPENAI_API_KEY
```

## Usage

**Evaluate against a known baseline** (produces colour-coded Excel comparing predictions to `data/manual_baseline.csv`):
```bash
py evaluate.py
```
Output: `results/predictions.csv` and `results/predictions.xlsx`

`results/predictions.csv` is the **submission output** — it contains the full original listing data alongside `classified_category`, `confidence`, and `reasoning` for each row.

**Classify unseen listings** (any CSV in the same column format):
```bash
py predict.py path/to/listings.csv
py predict.py path/to/listings.csv --output path/to/output.xlsx
```
Output: two files with the same stem — an Excel (colour-coded) and a CSV with the original listing columns plus `classified_category`, `confidence`, `reasoning`, and `requires_human_review` appended.

**Run tests:**
```bash
py -m pytest tests/ -v
```

---

## Output Schema

| Column | Description |
|---|---|
| `listing_id` | ID from source CSV, falls back to `row_N` if blank |
| `category` | `Nursery` / `SEN School` / `Food Store` / `None` |
| `confidence` | `High` / `Medium` / `Low` |
| `reasoning` | One sentence explaining the decision |
| `requires_human_review` | `True` if confidence is Medium or Low |

---

## Prompt Design

The core rule is **sector relevance**, not current use. Harkalm acquires both operating and vacant/former properties for conversion, so a vacant former nursery or former food store is acquisition-relevant and classified accordingly.

**Modelling choice:** I classified by sector relevance rather than current operational use. A vacant former nursery with retained fit-out is `Nursery`, not `None`. A former Costcutter with no current tenant is `Food Store`. The signal that matters is whether the property has a meaningful connection to one of the three sectors — not whether someone is trading there today. Generic suitability language alone (`"suitable for a variety of uses"`) does not qualify; a specific former use does.

Rules applied in order:
1. Classify by sector relevance — former or vacant use in a target sector qualifies
2. Generic suitability language alone (no named sector) → `None`
3. A specific former sector use → classified in that sector even if now vacant
4. Points of interest (nearby schools, stations) describe location — ignored entirely
5. Airspace or development rights → classify what is being sold, not the underlying tenant
6. Heritage-listed buildings where conversion is clearly impractical → `None`

Confidence is calibrated to reflect whether the acquisitions team should take a second look:
- `High`: property either currently operates in a target sector with an explicit operator named, or has no connection to any target sector and no suitability/alternative-use language
- `Medium`: any one of — former/vacant use in a target sector, retained fit-out or planning consent, suitability language, or airspace above a target-sector tenant

---

## Ambiguous Cases

Several listings are genuinely tricky:

- **HK-F001** (former Co-op): Vacant, retains chiller cabinets and shelving. `Food Store` / `Medium` — specific former food-retail use with retained fit-out qualifies under sector relevance.
- **88930830 / 88931949** (vacant nurseries): Buildings configured for nursery use, offered with vacant possession. Both `Nursery` / `Medium` — no current operator, but former nursery use with retained fit-out is acquisition-relevant.
- **HK-F003** (former nursery): Most recently trading as a nursery, D1 consent retained. `Nursery` / `Medium`.
- **89908812** (former Costcutter): Vacant former supermarket. `Food Store` / `Medium`.
- **758756684610048** (Sainsbury's airspace): Ground floor is a Sainsbury's, but the asset being sold is roof-extension development rights. Classified by what is being sold: `None` / `Medium`.
- **758775441528961** (healthcare unit): Marketed at medical professionals — but current tenants are a gym, an animal supplies shop, and a grooming parlour. `None` / `Medium`.
- **HK-F004**: Listing explicitly states no consent for childcare, education, or food retail — unusually clear, `None` / `High`.

---

## Confidence Calibration

The initial prompt returned `High` on all 23 rows — correct on categories but wrong on confidence, since clearly-None properties with no target-sector connection were treated the same as genuinely ambiguous ones.

The fix: Medium fires on **any** connection to a target sector — former use, retained fit-out, planning consent, suitability language, or marketed-at language — regardless of how confident the None call is. Two listings remain false Mediums (a woodland plot and a former café flagged due to generic "suitable for" developer language). These were accepted as the safer failure mode: over-flagging for human review is preferable to under-flagging.

Final result: **23/23 matched my manual baseline on category, 19/23 on confidence** (4 false Mediums on clearly-None properties — accepted as the safer failure mode).

---

## What I'd Improve With More Time

- **Few-shot examples** in the prompt for the hardest edge cases (vacant-with-fit-out, airspace rights, marketed-at-professionals) to tighten confidence calibration further
- **Batch API** for cost efficiency on larger datasets — 23 rows is fine synchronously, but at scale this would matter
- **Confidence threshold tuning** with a larger labelled dataset — the Medium/High boundary is currently defined by prompt rules rather than empirical calibration
- **Column coverage** — `analyticsTaxonomy.propertyType` is a useful structured signal that could supplement or sanity-check the free-text classification; currently only free-text fields are used
