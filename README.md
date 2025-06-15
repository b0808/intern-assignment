# Concept Extractor

This project extracts the **top 3 key concepts** from each question in a subject-wise dataset using LLM APIs (Anthropic Claude or OpenAI GPT).

---

### 👤 Author  
**Roll No:** 22B2446

---

## 📦 Requirements

- Python 3.7 or above  
- Internet connection  
- API key for **Anthropic** or **OpenAI**

---

## 🔐 API Setup

Create a `.env` file in the root directory and add your API key like this:

For **Anthropic**:
```
ANTHROPIC_API_KEY=your_anthropic_api_key
```

For **OpenAI**:
```
OPENAI_API_KEY=your_openai_api_key
```

Use only one API key depending on which model you are using.

---

## 🧪 Conda Environment Setup

Use the following `environment.yml` to create the required conda environment:

<details>
<summary><strong>Click to view environment.yml</strong></summary>

```yaml
name: concept-extractor
channels:
  - defaults
  - conda-forge
dependencies:
  - python=3.8
  - pip
  - pip:
      - python-dotenv
      - openai
      - anthropic
      - pandas
```
</details>

To create and activate the environment:

```bash
conda env create -f environment.yml
conda activate concept-extractor
```

---

## 🚀 How to Run

### ▶️ Using Anthropic Claude API

```bash
# Ensure .env contains:
# ANTHROPIC_API_KEY=your_key_here

python main.py --subject=ancient_history
```

You can replace `ancient_history` with any other subject like `geography`, `science`, etc.

---

### ▶️ Using OpenAI GPT API

```bash
# Ensure .env contains:
# OPENAI_API_KEY=your_key_here

python main_openai_llm.py --subject=ancient_history
```

---

## 📄 Output

- A `.csv` file will be generated in the `output/` folder.
- It contains the **top 3 concepts** for each question under the selected subject.
- Example output file:  
  `output/ancient_history_concepts.csv`

CSV format:

```
Question, Concept 1, Concept 2, Concept 3
```

---

## 📌 Notes

- Use only one API key at a time in the `.env` file.
- Input question CSV should be correctly formatted and available.
- Output will be overwritten if the script is re-run for the same subject.

---

## 📬 Contact

**Roll No:** 22B2446
