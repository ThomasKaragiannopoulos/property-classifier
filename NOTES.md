# Notes

## Assumptions

I classified by sector relevance rather than current operational use. Harkalm's acquisition criteria explicitly include vacant and former properties for conversion, so a vacant former nursery with retained fit-out is `Nursery`, not `None`. The trade-off of a pure "current use" approach is that it treats a former Costcutter and a woodland plot identically — both `None` — when they have very different acquisition value. Sector relevance avoids that conflation while still rejecting generic suitability language (`"suitable for a variety of uses"`) that does not name a specific former sector use.

Confidence is calibrated to reflect acquisition relevance, not classification certainty. A clearly vacant former nursery is `Nursery` / `Medium` — the category is unambiguous, but the absence of a current operator warrants a human check. A currently trading convenience store is `Food Store` / `High`. A woodland plot is `None` / `High`. The Medium trigger fires on any of: former or vacant use in a target sector, retained fit-out or planning consent (D1/F1/E), suitability language, or airspace above a target-sector tenant.

## Ambiguous Listings

Most ambiguity fell into three patterns: **former use with retained fit-out** (HK-F001, HK-F003, 88930830, 88931949, 89908812) — all classified in their sector at Medium; **suitability language** (72075420, 67195138, 758775441528961) — generic `"suitable for"` without a named former sector use → `None` / `Medium`; and **what is actually being sold** (758756684610048) — Sainsbury's occupies the ground floor but the asset is airspace development rights, so classified by what is being acquired (`None` / `Medium`).

## What I'd Improve With More Time

Few-shot examples in the prompt for the hardest edge cases (vacant-with-fit-out, airspace rights, marketed-at-professionals) to tighten confidence calibration further. Structured extraction of `analyticsTaxonomy.propertyType` as a cross-check on the free-text classification. A calibration pass on the Medium/High confidence boundary using a larger labelled dataset — the current boundary is prompt-defined rather than empirically tuned. At scale, the Batch API would cut costs significantly.
