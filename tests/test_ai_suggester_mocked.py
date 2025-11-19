from unittest.mock import MagicMock
from src.ai_suggester import AISuggester

def test_ai_suggester_mocked():
    suggester = AISuggester()

    # mock completarea AI
    suggester.client.chat.completions.create = MagicMock(return_value=MagicMock(
        choices=[MagicMock(message={"content": "Mocked suggestion"})]
    ))

    result = suggester.generate_suggestions(["ERROR: Something bad happened"])
    
    assert result == "Mocked suggestion"
