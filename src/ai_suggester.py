import os
from openai import OpenAI, RateLimitError, APIError
from dotenv import load_dotenv

load_dotenv()

class AISuggester:
    """
    Uses an AI model to generate suggestions for fixing log errors.
    Automatically falls back to offline analysis if API fails.
    """

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("MODEL", "gpt-4o-mini")

        # Create client only if key exists
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def _fallback_suggestion(self, errors):
        """
        Basic heuristic fallback if AI isn't available.
        """
        if not errors:
            return "No errors found. System is running normally."

        suggestions = [
            "⚠️ AI unavailable — using fallback engine.",
            "Possible causes:",
        ]

        for err in errors:
            if "database" in err.lower():
                suggestions.append("- Database connection issue. Check credentials or server availability.")
            elif "timeout" in err.lower():
                suggestions.append("- Operation timed out. Increase timeout or check network stability.")
            elif "critical" in err.lower():
                suggestions.append("- Critical error detected. Inspect system resources or hardware.")
            else:
                suggestions.append(f"- Review module associated with: {err[:50]}...")

        suggestions.append("\nGeneral steps:")
        suggestions.append("- Check recent config changes.")
        suggestions.append("- Inspect logs around the error timestamp.")
        suggestions.append("- Reproduce issue in a controlled environment.")

        return "\n".join(suggestions)

    def generate_suggestions(self, errors):
        """
        Sends error list to AI, or falls back if quota is exceeded or no key exists.
        """
        # nothing to analyze
        if not errors:
            return "No errors found. System is running normally."

        # no API key → use fallback
        if not self.api_key:
            return self._fallback_suggestion(errors)

        # call real AI with full safety
        prompt = (
            "You are an expert software engineer specialized in debugging.\n"
            "Below is a list of log errors. Provide clear, concise suggestions "
            "on what may have caused them and what steps could fix the problem.\n\n"
            "Errors:\n"
            + "\n".join(errors)
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )

            return response.choices[0].message["content"]

        except (RateLimitError, APIError, Exception):
            # fallback in case of quota exceeded, invalid model, or any other API error
            return self._fallback_suggestion(errors)
