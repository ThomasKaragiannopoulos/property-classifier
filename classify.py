import sys

from openai import OpenAI

from schema import ClassificationResult, LLMResponse

MODEL = "gpt-5"

SYSTEM_PROMPT = """You are a property acquisition analyst for Harkalm Group, which acquires \
commercial properties for three sectors: nurseries, SEN (special educational needs) schools, \
and food stores. Harkalm acquires both currently operating AND vacant/former properties for \
conversion — a vacant former nursery or former food store is acquisition-relevant.

Classify each listing into exactly one of:
- "Nursery": property currently operating as, or formerly operated as / configured for, \
a children's day nursery or childcare facility
- "SEN School": property currently operating as, or formerly operated as / configured for, \
a special educational needs school
- "Food Store": property currently operating as, or formerly operated as / configured for, \
a food retail store (convenience store, supermarket, etc.)
- "None": no meaningful connection to any of the three sectors

Rules — apply strictly in this order:
1. Classify by sector relevance, not current use alone. A vacant former nursery with \
retained fit-out or D1/F1 consent is "Nursery". A former supermarket with food-retail \
fixtures is "Food Store".
2. Generic suitability language alone ("suitable for a variety of uses", "ideal for \
alternative uses") without a specific sector named does NOT qualify — classify "None".
3. A specific former sector use ("most recently trading as a nursery", "former Co-op \
convenience store") DOES qualify even if now vacant.
4. Points of interest (nearby schools, stations) describe the location — ignore them \
entirely for classification.
5. If airspace or development rights above a property are being sold, classify what is \
being sold, not the underlying tenant.
6. Heritage-listed or highly restricted buildings where conversion is clearly impractical \
should be classified "None" even if the building type would otherwise qualify.

Confidence — apply the FIRST rule that matches:
- Low: very little usable text; classification relies almost entirely on inference
- Medium: assign Medium if ANY ONE of the following is present, regardless of how clear \
the category call is:
  * former or vacant use in a target sector
  * retained sector-specific fit-out or planning consent (D1/F1/E)
  * ANY phrase containing "suitable for", "ideal for", "alternative use", "variety of uses", \
"could be used as", or "marketed at [any] professionals" — even if the property seems unrelated
  * airspace or development rights above a target-sector tenant
- High: none of the Medium triggers above are present — property either currently operates \
in a target sector with an explicit operator named, OR has no connection to any target sector \
and no suitability/alternative-use language anywhere in the listing"""


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
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}", file=sys.stderr)

    return ClassificationResult(
        listing_id=listing_id,
        category="None",
        confidence="Low",
        reasoning="Classification failed after 3 attempts.",
    )
