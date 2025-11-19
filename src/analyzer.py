from typing import Dict, List
from src.log_reader import LogReader
from src.ai_suggester import AISuggester
import logging


class LogAnalyzer:
    """
    High-level orchestration class that ties together log parsing
    and AI suggestion generation.

    Methods
    -------
    analyze_file(path: str) -> dict
        Returns a dictionary containing detected errors and AI suggestions.
    """

    def __init__(self) -> None:
        logging.info("Reading errors from file...")
        self.reader = LogReader()
        self.ai = AISuggester()

    def analyze_file(self, file_path: str) -> Dict[str, List[str] | str]:
        """
        High-level orchestration method.

        Returns a report dictionary containing:
        - "errors": list of extracted log lines
        - "suggestions": AI-generated or fallback-generated advice
        """

        errors: List[str] = self.reader.read_errors(file_path)
        suggestions: str = self.ai.generate_suggestions(errors)

        logging.info("Generating AI suggestions...")
        return {
            "errors": errors,
            "suggestions": suggestions
        }
