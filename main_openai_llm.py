import argparse
import os
import csv
from openai import OpenAI  
from csv_reader import read_subject_csv


client = OpenAI(
    api_key="api_key",
    base_url="https://api.together.xyz/v1"
)

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def call_llama(prompt: str) -> str:
    """
    Call Together AI's LLaMA-2 model using openai>=1.0.0
    """
    response = client.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

def format_prompt(question: str, subject: str) -> str:
    return f"""Given the question: "{question}" from the subject "{subject}", identify/extract the top 3 underlying concepts being tested in question (e.g., "Indus Valley Civilization", "Gupta Period Literature", "Ashokan Edicts" etc).
           Respond with a semicolon-separated list of concepts only. example of output : "Indus Valley Civilization"; "Water harvesting and management"; "Ancient architecture" only three name no other single word """

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
            response_text = call_llama(prompt)
            concepts = [c.strip() for c in response_text.split(';') if c.strip()]
        except Exception as e:
            print(f"[ERROR] LLM failed on Question {question_num}: {e}")
            concepts = ["LLM Extraction Failed"]

        concept_str = "; ".join(concepts)
        print(f"Question {question_num}: {concept_str}")
        output_data.append([question_num, question_text, concept_str])

   
    output_file = os.path.join(OUTPUT_DIR, f"output_{args.subject}_concepts.csv")
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Question Number", "Question", "Concepts"])
        writer.writerows(output_data)

    print(f"\n✅ Output saved to: {args.subject}_{output_file}")

if __name__ == "__main__":
    main()
