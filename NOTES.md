# Notes

## Assumptions

I classified by sector relevance rather than current operational use — Harkalm explicitly acquires vacant and former properties for conversion, so a vacant former nursery is `Nursery` and a former Costcutter is `Food Store`. Generic suitability language without a named former sector use still returns `None`. Confidence reflects acquisition relevance: Medium fires on any of former/vacant use, retained fit-out or planning consent, suitability language, or airspace above a target-sector tenant; High means the call is unambiguous in either direction.

## Ambiguous Listings

Most ambiguity fell into three patterns: **former use with retained fit-out** (HK-F001, HK-F003, 88930830, 88931949, 89908812) — all classified in their sector at Medium; **suitability language** (72075420, 67195138, 758775441528961) — generic `"suitable for"` without a named former sector use → `None` / `Medium`; and **what is actually being sold** (758756684610048) — Sainsbury's occupies the ground floor but the asset is airspace development rights, so classified by what is being acquired (`None` / `Medium`).

## What I'd Improve With More Time

Few-shot examples in the prompt for the hardest edge cases (vacant-with-fit-out, airspace rights, marketed-at-professionals) to tighten confidence calibration further. Structured extraction of `analyticsTaxonomy.propertyType` as a cross-check on the free-text classification. A calibration pass on the Medium/High confidence boundary using a larger labelled dataset — the current boundary is prompt-defined rather than empirically tuned. At scale, the Batch API would cut costs significantly.
