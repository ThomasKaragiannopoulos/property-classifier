# Notes

## Assumptions

I interpreted the four labels as current operational use. This is an explicit modelling choice, not a given — the brief doesn't specify whether a vacant former nursery with retained fit-out should be "Nursery" or "None." I took the conservative route: historic use and suitability language are disqualifying, and points of interest are ignored entirely (nearby schools describe the neighbourhood, not the property). The trade-off is that acquisition-relevant vacant assets are classified None rather than into a sector bucket — I preserved that signal via Medium confidence and a requires_human_review flag instead. In a production workflow I'd likely add a candidate_sector field to surface these without conflating them with currently operating properties. I also treated confidence as reflecting acquisition relevance rather than classification certainty — a vacant former nursery with retained fit-out gets Medium because it may still warrant a human look, even though the None call is unambiguous.

## Ambiguous Listings

Most ambiguity fell into three patterns: **former use with retained fit-out** (HK-F001, HK-F003, 88930830, 88931949) — classified None, flagged Medium; **suitability language** (72075420, 67195138, 758775441528961) — "suitable for healthcare" treated as None regardless of sector mentioned; and **what is actually being sold** (758756684610048) — Sainsbury's occupies the ground floor but the asset is airspace development rights, so classified by what is being acquired.

## What I'd Improve With More Time

Few-shot examples in the prompt for the hardest edge cases, structured extraction of `analyticsTaxonomy.propertyType` as a cross-check, and a calibration pass on the Medium/High confidence boundary using a larger labelled dataset. At scale, the Batch API would cut costs significantly.
