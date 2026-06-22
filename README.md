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
Output: Excel with category, confidence, reasoning, and requires_human_review

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

The core rule is **current use only**. The model is explicitly instructed to ignore former use, potential use, and suitability language — these are the main sources of noise in agent copy.

**Modelling choice:** I interpreted the four labels as *current operational use*. This deliberately avoids classifying properties based only on historic use or agent suitability language, which are the main sources of noise in agent copy. The trade-off is that a vacant former nursery with retained fit-out is classified `None`, not `Nursery` — acquisitions-relevant signal is preserved via `Medium` confidence and `requires_human_review = True` rather than the category label. In a production workflow I would likely add a separate `candidate_sector` field so vacant/former assets surface in sector-specific views without conflating them with currently operating properties.

Rules applied in order:
1. Vacancy signals (`"former"`, `"previously"`, `"vacant possession"`, `"lease expired"`) → `None`
2. Suitability language (`"suitable for"`, `"ideal for"`, `"marketed at professionals"`) → `None` unless a named current tenant in the target sector is also stated
3. Points of interest (nearby schools, stations) describe location — ignored entirely
4. Airspace or development rights → classify what is being sold, not the underlying tenant

Confidence is calibrated to reflect whether the acquisitions team should take a second look, not just how certain the category call is. A clearly vacant former nursery is `None` with `Medium` confidence — the category is unambiguous, but the property warrants human review. A woodland plot is `None` with `High` confidence — no connection to any target sector.

---

## Ambiguous Cases

Several listings are genuinely tricky:

- **HK-F001** (former Co-op): Vacant, retains chiller cabinets and shelving. Classified `None` because the current operator has left. Medium confidence because the fit-out makes it sector-relevant.
- **88930830 / 88931949** (vacant nurseries): Buildings configured for nursery use, offered with vacant possession. Both `None` / `Medium` — fit-out retained but no current operator.
- **758756684610048** (Sainsbury's airspace): Ground floor is a Sainsbury's, but the asset being sold is roof-extension development rights. Classified by what is being sold: `None`.
- **758775441528961** (healthcare unit): Marked as `HEALTHCARE_FACILITY`, marketed at medical professionals — but current tenants are a gym, an animal supplies shop, and a grooming parlour. `None` / `Medium`.
- **HK-F004**: Listing explicitly states no consent for childcare, education, or food retail — unusually clear, `None` / `High`.

---

## Confidence Calibration

The initial prompt returned `High` on all 23 rows — correct on categories but wrong on confidence, since clearly-None properties with no target-sector connection were treated the same as genuinely ambiguous ones.

The fix: Medium fires on **any** connection to a target sector — former use, retained fit-out, planning consent, suitability language, or marketed-at language — regardless of how confident the None call is. Two listings remain false Mediums (a woodland plot and a former café flagged due to generic "suitable for" developer language). These were accepted as the safer failure mode: over-flagging for human review is preferable to under-flagging.

Final result: **23/23 matched my manual baseline on category, 21/23 on confidence**.

---

## What I'd Improve With More Time

- **Few-shot examples** in the prompt for the hardest edge cases (vacant-with-fit-out, airspace rights, marketed-at-professionals) to tighten confidence calibration further
- **Batch API** for cost efficiency on larger datasets — 23 rows is fine synchronously, but at scale this would matter
- **Confidence threshold tuning** with a larger labelled dataset — the Medium/High boundary is currently defined by prompt rules rather than empirical calibration
- **Column coverage** — `analyticsTaxonomy.propertyType` is a useful structured signal that could supplement or sanity-check the free-text classification; currently only free-text fields are used
