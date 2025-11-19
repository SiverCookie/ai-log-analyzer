import argparse
from src.analyzer import LogAnalyzer

def main():
    parser = argparse.ArgumentParser(description="AI-powered log analyzer")
    parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="Path to the log file to analyze"
    )

    args = parser.parse_args()
    analyzer = LogAnalyzer()

    print("\n🔍 Reading log file:", args.file)
    result = analyzer.analyze_file(args.file)

    print("\n📌 Extracted errors:")
    if result["errors"]:
        for err in result["errors"]:
            print("  -", err)
    else:
        print("  No errors found.")

    print("\n🤖 AI Suggestions:")
    print(result["suggestions"])
    print("\nDone.\n")

if __name__ == "__main__":
    main()
