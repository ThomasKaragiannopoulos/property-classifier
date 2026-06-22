from ingest import extract_text, get_listing_id, parse_key_features


class TestParseKeyFeatures:
    def test_valid_list(self):
        raw = "['A1 Use Class', 'Former Co-op', '1,850 sq ft']"
        assert parse_key_features(raw) == ["A1 Use Class", "Former Co-op", "1,850 sq ft"]

    def test_empty_string(self):
        assert parse_key_features("") == []

    def test_whitespace_only(self):
        assert parse_key_features("   ") == []

    def test_malformed_falls_back_to_string(self):
        assert parse_key_features("[broken list") == ["[broken list"]

    def test_plain_text_falls_back_to_string(self):
        assert parse_key_features("plain text") == ["plain text"]


class TestExtractText:
    def test_pulls_summary_and_description(self):
        row = {"summary": "A nursery for sale", "detailedDescription": "Details here", "keyFeatures": ""}
        text = extract_text(row)
        assert "summary: A nursery for sale" in text
        assert "detailedDescription: Details here" in text

    def test_missing_columns_silently_skipped(self):
        row = {"summary": "Only summary"}
        text = extract_text(row)
        assert "summary: Only summary" in text

    def test_all_blank_row_returns_fallback(self):
        assert extract_text({}) == "(no usable listing text)"

    def test_key_features_parsed_and_included(self):
        row = {"keyFeatures": "['Feature A', 'Feature B']"}
        text = extract_text(row)
        assert "Feature A" in text
        assert "Feature B" in text


class TestGetListingId:
    def test_returns_id_when_present(self):
        assert get_listing_id({"id": "HK-F001"}, 0) == "HK-F001"

    def test_falls_back_to_row_index_when_empty(self):
        assert get_listing_id({"id": ""}, 4) == "row_5"

    def test_falls_back_when_id_key_missing(self):
        assert get_listing_id({}, 0) == "row_1"
