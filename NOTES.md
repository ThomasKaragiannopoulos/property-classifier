# Notes

## Assumptions

I interpreted the four labels as current operational use — a modelling choice, not a given. Historic use and suitability language are disqualifying; points of interest are ignored entirely. The trade-off is that a vacant former nursery with retained fit-out is classified None rather than Nursery; I preserved that signal via Medium confidence and requires_human_review rather than the category label. I also treated confidence as reflecting acquisition relevance rather than classification certainty.

## Ambiguous Listings

Most ambiguity fell into three patterns: **former use with retained fit-out** (HK-F001, HK-F003, 88930830, 88931949) — classified None, flagged Medium; **suitability language** (72075420, 67195138, 758775441528961) — "suitable for healthcare" treated as None regardless of sector mentioned; and **what is actually being sold** (758756684610048) — Sainsbury's occupies the ground floor but the asset is airspace development rights, so classified by what is being acquired.

## What I'd Improve With More Time

Few-shot examples in the prompt for the hardest edge cases, structured extraction of `analyticsTaxonomy.propertyType` as a cross-check, and a calibration pass on the Medium/High confidence boundary using a larger labelled dataset. At scale, the Batch API would cut costs significantly.
