import json

from openai import OpenAI

from schema import ClassificationResult, LLMResponse

MODEL = "gpt-5"

SYSTEM_PROMPT = """You are a property acquisition analyst for Harkalm Group, which acquires \
commercial properties for three sectors: nurseries, SEN (special educational needs) schools, \
and food stores.

Classify each listing into exactly one of:
- "Nursery": property currently operating as a children's day nursery or childcare facility
- "SEN School": property currently operating as a special educational needs school
- "Food Store": property currently operating as a food retail store (convenience store, supermarket, etc.)
- "None": does not currently operate as any of the above

Rules — apply strictly in this order:
1. Base classification on CURRENT USE only. Former, past, or potential future use does not count.
2. Any of these phrases signals "None": "former", "previously", "vacant possession", \
"most recently trading as", "offered with vacant possession", "lease expired", "ceased trading".
3. "Suitable for", "ideal for", "could be used as", "marketed at [sector] professionals" signals \
"None" unless a named current tenant in that sector is also stated.
4. Points of interest (nearby schools, stations) describe the location — ignore them entirely \
for classification.
5. If airspace or development rights above a property are being sold, classify what is being \
sold, not the underlying tenant.

Confidence:
- High: current operation stated explicitly and unambiguously
- Medium: ambiguous signals, former use with retained fit-out, "suitable for" language, \
or thin listing text requiring some inference
- Low: very little usable text, classification is heavy inference"""


def classify(client: OpenAI, listing_id: str, listing_text: str) -> ClassificationResult:
    for attempt in range(3):
        try:
            response = client.beta.chat.completions.parse(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Classify this listing:\n\n{listing_text}"},
                ],
                response_format=LLMResponse,
            )
            parsed = response.choices[0].message.parsed
            if parsed is not None:
                return ClassificationResult(listing_id=listing_id, **parsed.model_dump())
        except Exception:
            pass

    return ClassificationResult(
        listing_id=listing_id,
        category="None",
        confidence="Low",
        reasoning="Classification failed after 3 attempts.",
    )
