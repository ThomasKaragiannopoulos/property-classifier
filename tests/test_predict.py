from predict import CATEGORY_FILL, CONFIDENCE_FILL


class TestColorMaps:
    def test_all_categories_have_fill_entry(self):
        for cat in ("Nursery", "SEN School", "Food Store", "None"):
            assert cat in CATEGORY_FILL

    def test_none_category_has_no_fill(self):
        assert CATEGORY_FILL["None"].fill_type is None

    def test_all_confidence_levels_have_fill_entry(self):
        for conf in ("High", "Medium", "Low"):
            assert conf in CONFIDENCE_FILL

    def test_high_and_low_have_different_fills(self):
        assert CONFIDENCE_FILL["High"].fgColor != CONFIDENCE_FILL["Low"].fgColor
