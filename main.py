import argparse
import os
import csv
from csv_reader import read_subject_csv
from llm_api import call_anthropic

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def format_prompt(question: str, subject: str) -> str:
    """
    Format the prompt for Claude to extract academic concepts.
    """
    return f"""Given the question: "{question}" from the subject "{subject}", identify the core academic or historical concept(s) it is testing.
Respond with a semicolon-separated list of concepts."""

def main():
    parser = argparse.ArgumentParser(description="Intern Task: Question to Concept Mapping")
    parser.add_argument('--subject', required=True, choices=['ancient_history', 'math', 'physics', 'economics'], help='Subject to process')
    args = parser.parse_args()

    data = read_subject_csv(args.subject)
    print(f"Loaded {len(data)} questions for subject: {args.subject}")

    output_data = []

    for row in data:
        question_num = row.get("Question Number", "").strip()
        question_text = row.get("Question", "").strip()

        prompt = format_prompt(question_text, args.subject)
        try:
            response_text = call_anthropic(prompt)
            concepts = [c.strip() for c in response_text.split(';') if c.strip()]
        except Exception as e:
            print(f"[ERROR] LLM failed on Question {question_num}: {e}")
            concepts = ["LLM Extraction Failed"]

        concept_str = "; ".join(concepts)
        print(f"Question {question_num}: {concept_str}")
        output_data.append([question_num, question_text, concept_str])

    # Save output CSV
    output_file = os.path.join(OUTPUT_DIR, "output_concepts.csv")
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Question Number", "Question", "Concepts"])
        writer.writerows(output_data)

    print(f"\n✅ Output saved to: {output_file}")

if __name__ == "__main__":
    main()
