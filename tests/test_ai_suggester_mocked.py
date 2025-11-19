from unittest.mock import MagicMock
from src.ai_suggester import AISuggester

def test_ai_suggester_mocked():
    suggester = AISuggester()

    # mock AI complet
    suggester.generate_suggestions = MagicMock(return_value="Mocked suggestion")

    result = suggester.generate_suggestions(["ERROR: Something bad happened"])

    assert result == "Mocked suggestion"