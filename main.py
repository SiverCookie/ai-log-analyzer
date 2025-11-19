import argparse
import logging
from src.analyzer import LogAnalyzer
import json

# Configure logging globally
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)

def main():
    parser = argparse.ArgumentParser(description="AI-powered log analyzer")

    parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="Path to the log file to analyze"
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Optional: Write the result to a text file"
    )

    parser.add_argument(
        "--format",
        type=str,
        choices=["text", "json"],
        default="text",
        help="Output format"
    )

    parser.add_argument(
        "--ai",
        type=str,
        choices=["on", "off", "fallback"],
        default="fallback",
        help="AI mode control"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit the number of errors sent to AI"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable detailed logging"
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress standard output"
    )

    args = parser.parse_args()

    # Verbose mode
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Verbose mode activated.")
    else:
        logging.getLogger().setLevel(logging.INFO)

    analyzer = LogAnalyzer()

    logging.info(f"Reading log file: {args.file}")

    try:
        result = analyzer.analyze_file(args.file)
        errors = result["errors"]
    except FileNotFoundError:
        logging.error(f"File not found: {args.file}")
        return

    # Apply limit
    if args.limit:
        logging.info(f"Limiting errors to first {args.limit}")
        errors = errors[:args.limit]

    # AI mode selection
    if args.ai == "off":
        logging.info("AI mode OFF — skipping suggestions.")
        suggestions = "AI disabled. No suggestions generated."
    elif args.ai == "fallback":
        logging.info("AI fallback mode enabled.")
        suggestions = analyzer.ai.generate_suggestions_fallback(errors)
    else:  # ai == "on"
        suggestions = analyzer.ai.generate_suggestions(errors)

    # JSON output mode
    if args.format == "json":
        print(json.dumps({"errors": errors, "suggestions": suggestions}, indent=4))
        return

    # Print errors
    if errors:
        logging.info(f"Found {len(errors)} errors:")
        for err in errors:
            logging.info(f"  {err}")
    else:
        logging.info("No errors found in log.")

    # Print suggestions
    logging.info("Generating suggestions...")
    if not args.quiet:
        print("\n" + suggestions + "\n")

    # Optional output to file
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write("=== ERROR REPORT ===\n\n")
            f.write("Errors:\n")
            for e in errors:
                f.write(f"- {e}\n")
            f.write("\nSuggestions:\n")
            f.write(suggestions)

        logging.info(f"Report written to: {args.output}")


if __name__ == "__main__":
    main()
