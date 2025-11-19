from unittest.mock import MagicMock
from src.analyzer import LogAnalyzer

def test_analyzer_flow():
    analyzer = LogAnalyzer()

    # mock log reader output
    analyzer.reader.read_errors = MagicMock(return_value=["ERROR: Something happened"])

    # mock ai suggester output
    analyzer.ai.generate_suggestions = MagicMock(return_value="Mocked suggestion")

    result = analyzer.analyze_file("logs/sample.log")

    assert result["errors"] == ["ERROR: Something happened"]
    assert result["suggestions"] == "Mocked suggestion"
