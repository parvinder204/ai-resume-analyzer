# ResumeAI — Intelligent Resume Analyzer & Job Matcher

> Upload → Analyse → Match → Ace Your Interview

A production-grade AI application that analyses resumes, computes ATS scores, extracts skills using NLP, semantically matches job descriptions, and generates personalised interview questions — all in a clean, polished Streamlit UI.

---

## ✨ Features

| Feature | Description |
|---|---|
| **PDF Parsing** | Robust text extraction from any text-selectable PDF |
| **Skill Extraction** | spaCy PhraseMatcher + curated 200+ skill taxonomy |
| **ATS Scoring** | Multi-dimensional weighted score (keyword match, formatting, sections, contact info, action verbs, quantification) |
| **Skill Gap Analysis** | Matched / missing / bonus skills against job description |
| **Semantic Job Matching** | Sentence Transformers (`all-MiniLM-L6-v2`) cosine similarity |
| **Improvement Suggestions** | Personalised, dimension-aware tips |
| **Interview Coach** | Skill-tailored technical + behavioural + situational questions |
| **Multi-Resume Compare** | Rank candidates semantically against a job description |
| **Recruiter Dashboard** | Session-wide aggregate analytics & charts |

## 🚀 Quick Start

### Prerequisites

- Python **3.10+**
- pip
- (Recommended) Git

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ First run downloads the `all-MiniLM-L6-v2` model (~80 MB) and the spaCy model. This only happens once — they are cached locally.

### 4. (Optional) Download spaCy model manually

The `requirements.txt` includes the spaCy model URL. If it fails, run:

```bash
python -m spacy download en_core_web_sm
```

### 5. Run the app

```bash
streamlit run app.py
```

The app opens automatically at **http://localhost:8501**.

---

## 🧪 Running Tests

```bash
pytest tests/ -v
or 
python -m pytest
```

For coverage report:

```bash
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html
```

---

## 🧭 Usage Guide

### Resume Analyzer (Main Page)

1. Upload your resume as a **PDF** (text-selectable, not scanned image).
2. Choose a **sample job** from the dropdown, or paste a **custom job description**.
3. Click **⚡ Analyse Resume**.
4. Review:
   - **ATS Score** gauge + grade
   - **Score Breakdown** — radar & bar charts per dimension
   - **Skills** — matched ✅, missing ❌, bonus ⭐
   - **Job Matches** — top roles ranked by semantic fit
   - **Suggestions** — personalised improvement tips

### Interview Coach

1. Your skills auto-populate from the last analysis (or enter manually).
2. Set the number of questions (5–20) and target job title.
3. Click **🎯 Generate Questions**.
4. Filter by question type (Technical / Behavioural / Situational) or difficulty.
5. Each card shows the question, type badge, difficulty badge, and an answering tip.

### Multi-Resume Compare

1. Upload **2–5 PDF resumes**.
2. Paste the target **job description**.
3. Click **🏆 Rank Candidates**.
4. View ranked bar chart and per-candidate skill breakdown.

### Recruiter Dashboard

Automatically populated from session data — visit after running the Analyzer and/or Comparison.

---

## ⚙️ Configuration

### ATS Strictness

In the sidebar settings panel:

| Mode | Keyword Weight | Best for |
|---|---|---|
| **Lenient** | 30% | Junior roles, career changers |
| **Balanced** | 35% | Most use cases (default) |
| **Strict** | 40% | Senior / highly specialised roles |

### Adding Custom Jobs

Edit `data/sample_jobs/jobs.json` to add your own job listings:

```json
{
  "id": "job_011",
  "title": "Your Job Title",
  "company": "Company Name",
  "location": "Remote",
  "salary_range": "$X – $Y",
  "description": "Full job description text here.",
  "required_skills": ["Python", "Docker", "AWS"]
}
```

---

## 🛠 Technical Architecture

```
PDF Upload
    │
    ▼
pdf_parser.py          ← PyPDF2 text extraction + cleaning
    │
    ▼
skill_extractor.py     ← spaCy PhraseMatcher + 200-skill taxonomy + aliases
    │
    ├──► ats_scorer.py ← 7-dimension weighted ATS score
    │
    └──► job_matcher.py← SentenceTransformer embeddings → cosine similarity
              │
              ▼
         interview_gen.py ← Rule-based + template question generation
```

**Embedding model:** `all-MiniLM-L6-v2` — 384-dim dense vectors, 80 MB, CPU-friendly.  
**NLP model:** `en_core_web_sm` — fast tokenisation and lemmatisation.

---

## 📦 Key Libraries

| Library | Version | Purpose |
|---|---|---|
| `streamlit` | 1.36 | Web UI framework |
| `PyPDF2` | 3.0 | PDF text extraction |
| `spacy` | 3.7 | NLP tokenisation + phrase matching |
| `sentence-transformers` | 3.0 | Semantic embeddings |
| `scikit-learn` | 1.4 | ML utilities |
| `plotly` | 5.22 | Interactive charts |
| `loguru` | 0.7 | Structured logging |
| `pydantic` | 2.7 | Data validation |

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Make your changes and add tests.
4. Run tests: `pytest tests/ -v`
5. Open a pull request.

---

