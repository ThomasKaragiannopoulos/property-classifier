from unittest.mock import MagicMock

import pytest
from pydantic import ValidationError

from classify import classify
from schema import ClassificationResult, LLMResponse


def make_client(parsed=None, raises=None):
    """Build a mock OpenAI client. Mocks client.beta.chat.completions.parse."""
    client = MagicMock()
    if raises:
        client.beta.chat.completions.parse.side_effect = raises
    else:
        mock_response = MagicMock()
        mock_response.choices[0].message.parsed = parsed
        client.beta.chat.completions.parse.return_value = mock_response
    return client


class TestClassify:
    def test_valid_response_returns_result(self):
        parsed = LLMResponse(category="Nursery", confidence="High", reasoning="Currently operating.")
        result = classify(make_client(parsed=parsed), "HK-001", "some listing text")
        assert result.listing_id == "HK-001"
        assert result.category == "Nursery"
        assert result.confidence == "High"

    def test_api_error_retries_three_times_then_falls_back(self):
        client = make_client(raises=Exception("API error"))
        result = classify(client, "HK-999", "some text")
        assert result.category == "None"
        assert result.confidence == "Low"
        assert client.beta.chat.completions.parse.call_count == 3

    def test_parsed_none_retries_three_times_then_falls_back(self):
        client = make_client(parsed=None)
        result = classify(client, "HK-999", "some text")
        assert result.category == "None"
        assert result.confidence == "Low"
        assert client.beta.chat.completions.parse.call_count == 3


class TestSchema:
    def test_valid_construction(self):
        r = ClassificationResult(
            listing_id="x", category="Food Store", confidence="High", reasoning="OK"
        )
        assert r.category == "Food Store"

    def test_invalid_category_raises(self):
        with pytest.raises(ValidationError):
            ClassificationResult(
                listing_id="x", category="Hospital", confidence="High", reasoning="OK"
            )

    def test_invalid_confidence_raises(self):
        with pytest.raises(ValidationError):
            ClassificationResult(
                listing_id="x", category="None", confidence="Very High", reasoning="OK"
            )
