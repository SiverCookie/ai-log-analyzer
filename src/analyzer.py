from src.log_reader import LogReader
from src.ai_suggester import AISuggester

class LogAnalyzer:
    """
    Coordinates the log reading and AI suggestion generation.
    """

    def __init__(self):
        self.reader = LogReader()
        self.ai = AISuggester()

    def analyze_file(self, file_path):
        """
        Reads a log file, extracts errors, and asks the AI for suggestions.
        Returns a dictionary with both raw errors and AI-generated advice.
        """
        errors = self.reader.read_errors(file_path)
        suggestions = self.ai.generate_suggestions(errors)

        return {
            "errors": errors,
            "suggestions": suggestions
        }
