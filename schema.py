from typing import Literal
from pydantic import BaseModel

Category = Literal["Nursery", "SEN School", "Food Store", "None"]
Confidence = Literal["High", "Medium", "Low"]


class LLMResponse(BaseModel):
    """Schema passed to the LLM via structured outputs — no listing_id."""
    category: Category
    confidence: Confidence
    reasoning: str


class ClassificationResult(BaseModel):
    listing_id: str
    category: Category
    confidence: Confidence
    reasoning: str
