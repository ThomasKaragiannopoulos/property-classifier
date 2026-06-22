# Notes

## Assumptions

Current operational use is the only signal that matters. A vacant former nursery is not a nursery target — it's a redevelopment opportunity. I treated "suitable for", "previously operated as", and similar phrases as disqualifying, and ignored points of interest entirely (nearby schools describe the neighbourhood, not the property). I also assumed confidence should reflect acquisition relevance, not just classification certainty — a vacant former nursery with retained fit-out gets Medium because it may still warrant a human look, even though the None call is unambiguous.

## Ambiguous Listings

Most ambiguity fell into three patterns: **former use with retained fit-out** (HK-F001, HK-F003, 88930830, 88931949) — classified None, flagged Medium; **suitability language** (72075420, 67195138, 758775441528961) — "suitable for healthcare" treated as None regardless of sector mentioned; and **what is actually being sold** (758756684610048) — Sainsbury's occupies the ground floor but the asset is airspace development rights, so classified by what is being acquired.

## What I'd Improve With More Time

Few-shot examples in the prompt for the hardest edge cases, structured extraction of `analyticsTaxonomy.propertyType` as a cross-check, and a calibration pass on the Medium/High confidence boundary using a larger labelled dataset. At scale, the Batch API would cut costs significantly.
