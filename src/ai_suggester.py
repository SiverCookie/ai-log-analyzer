import os
from typing import List, Optional
from openai import OpenAI, RateLimitError, APIError
from dotenv import load_dotenv
import logging

load_dotenv()


class AISuggester:
    """
    Handles AI-based error analysis.

    Attributes
    ----------
    model : str
        The name of the AI model to call.
    client : OpenAI
        The underlying OpenAI client instance.

    Methods
    -------
    generate_suggestions(errors: list[str]) -> str
        Sends errors to the AI model and returns a suggestion text.

    generate_suggestions_fallback(errors: list[str]) -> str
        Generates simple rule-based recommendations when AI is disabled or unavailable.
    """

    def __init__(self) -> None:
        self.api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
        self.model: str = os.getenv("MODEL", "gpt-4o-mini")

        # Create client only if we have a key
        self.client: Optional[OpenAI] = (
            OpenAI(api_key=self.api_key) if self.api_key else None
        )

    def _fallback_suggestion(self, errors: List[str]) -> str:
        """
        Local offline fallback model.
        Uses simple heuristics to produce meaningful suggestions.
        """

        if not errors:
            return "No errors found. System is running normally."

        suggestions = [
            "⚠️ AI unavailable — using fallback engine.",
            "Possible causes:",
        ]

        for err in errors:
            lower = err.lower()

            if "database" in lower:
                suggestions.append("- Database connection issue. Check credentials or server availability.")

            elif "timeout" in lower:
                suggestions.append("- Operation timed out. Check network stability or increase timeout limits.")

            elif "critical" in lower:
                suggestions.append("- Critical error detected. Inspect CPU, RAM, temperature, or hardware.")

            else:
                # generic fallback
                suggestions.append(f"- Investigate subsystem associated with: '{err[:60]}...'")

        suggestions.extend([
            "",
            "General steps:",
            "- Check recent config changes.",
            "- Inspect logs around the error timestamp.",
            "- Reproduce the issue in a controlled environment."
        ])
        logging.warning("AI unavailable — using fallback mode.")
        return "\n".join(suggestions)
        
    def generate_suggestions_fallback(self, errors):
        return (
            "AI unavailable — fallback activated.\n\n"
            + "\n".join(f"- Possible issue: {e}" for e in errors)
        )

    def generate_suggestions(self, errors: List[str]) -> str:
        """
        Generates suggestions for fixing the provided log errors.
        Automatically falls back to heuristic mode if AI fails.

        Parameters
        ----------
        errors : List[str]
            The list of extracted log errors.

        Returns
        -------
        str
            A formatted suggestion message.
        """

        if not errors:
            return "No errors found. System is running normally."

        # No API key → fallback mode
        if not self.client:
            return self._fallback_suggestion(errors)

        # Build prompt
        prompt = (
            "You are an expert software engineer specialized in debugging.\n"
            "Analyze the following log errors and provide concise, actionable steps.\n\n"
            "Errors:\n" + "\n".join(errors)
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )
            logging.info("Sending error list to AI model...")
            return response.choices[0].message["content"]

        except (RateLimitError, APIError, Exception):
            # fallback on any OpenAI failure
            logging.error("AI request failed — entering fallback mode.")
            return self._fallback_suggestion(errors)
