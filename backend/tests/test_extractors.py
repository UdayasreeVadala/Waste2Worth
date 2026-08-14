import os

from waste2worth_ai import llm
from waste2worth_ai.nl_extractor import extract_waste_from_text
from waste2worth_ai.vision import build_data_uri, classify_waste_image


def test_nl_extraction_rule_based_quantity_tonnes():
    result = extract_waste_from_text("I have 2 tonnes of spoiled onion waste from Nashik")
    assert result["waste_type"] == "onion"
    assert result["quantity_kg"] == 2000
    assert result["condition"] == "spoiled"
    assert result["source"] == "nl_rules"


def test_nl_extraction_rule_based_kg():
    result = extract_waste_from_text("around 700 kg of rotten tomatoes at my farm")
    assert result["waste_type"] == "tomato"
    assert result["quantity_kg"] == 700
    assert result["condition"] == "spoiled"


def test_nl_extraction_rule_based_quintal():
    result = extract_waste_from_text("10 quintal of mango waste")
    assert result["quantity_kg"] == 1000


def test_nl_extraction_crop_residue_beats_grain():
    result = extract_waste_from_text("around 1200 kg of paddy stubble from my farm in Nashik")
    assert result["waste_type"] == "crop"
    assert result["location"] == "Nashik"


def test_nl_extraction_city_after_in():
    result = extract_waste_from_text("2 tonnes of spoiled onion waste from my farm in Nashik, India")
    assert result["location"] == "Nashik, India"


def test_nl_extraction_returns_none_on_empty():
    assert extract_waste_from_text("") is None
    assert extract_waste_from_text(None) is None


def test_nl_extraction_disabled_ai_still_extracts():
    result = extract_waste_from_text("500kg of fresh banana peels")
    assert result["quantity_kg"] == 500
    assert result["condition"] == "fresh"


def test_data_uri_encoding():
    uri = build_data_uri(b"\xff\xd8\xff\xe0", mime_type="image/jpeg")
    assert uri.startswith("data:image/jpeg;base64,")


def test_vision_returns_none_without_key():
    os.environ.pop("OPENAI_API_KEY", None)
    assert classify_waste_image(None) is None
    assert classify_waste_image(build_data_uri(b"\x00" * 32)) is None


def test_vision_returns_none_when_disabled():
    previous_key = os.environ.get("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = "sk-test-does-not-exist"
    os.environ["WASTE2WORTH_USE_AI"] = "0"
    try:
        assert classify_waste_image("data:image/jpeg;base64,AAAA") is None
        assert llm.ai_enabled() is False
    finally:
        os.environ.pop("WASTE2WORTH_USE_AI", None)
        if previous_key is None:
            os.environ.pop("OPENAI_API_KEY", None)
        else:
            os.environ["OPENAI_API_KEY"] = previous_key
