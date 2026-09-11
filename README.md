# Personal AI Application Assistant

An evidence-grounded personal application assistant for scholarships, jobs, internships, fellowships, and university programs.

> **One profile → many opportunities → personalized applications.**

## What it solves

Students repeatedly provide the same education, projects, achievements, leadership, volunteering, skills, and experience to application tools. This MVP lets a student upload their profile documents once per session, builds a RAG knowledge base, analyzes a new opportunity, matches requirements to profile evidence, identifies gaps, and generates grounded application responses.

The assistant is deliberately **not** a generic “chat with PDF” app. Its main product is **Personal Profile + Opportunity Intelligence + Matching + Evidence-Grounded Application Assistance**.

## Features

- Multi-document personal profile upload: PDF, DOCX, TXT.
- PyMuPDF / python-docx / standard text extraction.
- Text cleaning and chunking with source metadata.
- Sentence Transformers embeddings.
- FAISS vector search over profile evidence only.
- Opportunity analysis into structured fields.
- Requirement ↔ profile evidence matching.
- Matches, gaps, and unclear states.
- Transparent AI-generated readiness estimate.
- Evidence/source display for generated answers.
- Application assistant with refine actions.
- Tailored Markdown resume generation.
- Session-only profile storage; no database required for the hackathon MVP.
- Friendly handling of invalid files, empty indexes, missing keys, API failures, and malformed structured output.

## Architecture

```text
Profile documents
    ↓
Extraction → cleaning → chunking
    ↓
Sentence Transformer embeddings
    ↓
FAISS (profile evidence only)
    ↓
Retriever
    ↓
Relevant evidence + opportunity context
    ↓
Groq LLM
    ↓
Grounded answer / match / tailored resume
```

Opportunity documents are analyzed separately and are **not inserted into the personal profile index**.

## Technology stack

- Python 3.12
- Streamlit
- FAISS CPU
- Sentence Transformers
- Groq Python SDK
- Groq `openai/gpt-oss-120b` by default
- PyMuPDF
- python-docx

The default Groq model is `openai/gpt-oss-120b`, which is currently listed by Groq as a production model with a 131,072-token context window and JSON support. Groq's current deprecation page lists older Llama 3.3 70B as deprecated for free/developer usage, so this project avoids hardcoding that retired model. You can override the model with `GROQ_MODEL`. 

## Project structure

```text
app.py
config.py
requirements.txt
README.md
.env.example
.gitignore
.streamlit/config.toml
utils/
    __init__.py
    file_parser.py
    text_processor.py
    validators.py
rag/
    __init__.py
    embeddings.py
    vector_store.py
    retriever.py
llm/
    __init__.py
    groq_client.py
    prompts.py
    generator.py
profile/
    __init__.py
    profile_manager.py
opportunity/
    __init__.py
    analyzer.py
    matcher.py
features/
    __init__.py
    application_assistant.py
    resume_generator.py
    readiness_score.py
    evidence.py
ui/
    __init__.py
    dashboard.py
    profile_page.py
    opportunity_page.py
    match_page.py
    assistant_page.py
    resume_page.py
tests/
    test_file_parser.py
    test_text_processor.py
    test_vector_store.py
    test_validators.py
data/
    .gitkeep
```

## Local setup

Use Python 3.12 for a predictable deployment environment.

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### macOS/Linux

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a local `.env` from `.env.example`, or export `GROQ_API_KEY` in your shell. The app reads Streamlit secrets first and then environment variables. Do not commit `.env`.

Then:

```bash
streamlit run app.py
```

The first launch downloads the Sentence Transformers model. Subsequent launches use Streamlit's resource cache.

## Environment variables

```text
GROQ_API_KEY=your_real_key
GROQ_MODEL=openai/gpt-oss-120b
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

Only `GROQ_API_KEY` is required.

## Streamlit Community Cloud

1. Push this project to a GitHub repository.
2. Open Streamlit Community Cloud and choose **Create app**.
3. Select the repository, branch, and `app.py` entrypoint.
4. In **Advanced settings**, choose Python 3.12.
5. Add this secret:

```toml
GROQ_API_KEY = "your_real_key"
```

6. Deploy.

Streamlit Community Cloud currently defaults to Python 3.12 and supports selecting a supported Python version during deployment. Dependencies belong in `requirements.txt`; secrets should be configured in the app's Secrets settings rather than committed to Git.

## RAG and grounding

1. Personal files are extracted into text.
2. Text is cleaned and split into overlapping chunks.
3. Chunks receive source metadata.
4. Sentence Transformers creates normalized embeddings.
5. FAISS stores the embeddings and metadata is kept alongside the index.
6. A user question or opportunity requirement is embedded and the closest profile chunks are retrieved.
7. Only those relevant chunks are sent to Groq, together with the question/opportunity context.
8. Prompts explicitly prohibit unsupported personal claims.
9. Generated outputs show the evidence sources used.

This makes the system evidence-grounded rather than relying on the model's general knowledge about the student.

## Readiness score

The readiness estimate is an equal-weight average of five transparent categories:

- Eligibility
- Skills
- Experience
- Documents
- Other

Each category is scored 0–100 by the matching model from the retrieved evidence. The resulting number is explicitly labeled as an **AI-generated profile match/readiness estimate**, not a scientifically validated probability.

## Privacy and security

- No API keys are hardcoded.
- `.env`, secrets, private documents, and local vector databases are ignored by Git.
- The MVP keeps the profile index in Streamlit session memory.
- The app does not intentionally log document contents.
- Do not upload passwords, payment information, credentials, or other highly sensitive data.

## Tests

Run:

```bash
pytest -q
```

The tests cover extraction, empty documents, chunking, retrieval, and basic validation. They avoid making network/API calls.

## Troubleshooting

### “GROQ_API_KEY is not configured”

Set the key in `.env` locally or Streamlit Cloud Secrets.

### PDF says no text was extracted

The MVP extracts text from PDFs but does not perform OCR. Scanned/image-only PDFs need OCR before upload.

### FAISS installation fails locally

Use Python 3.12 and the pinned `faiss-cpu` version in `requirements.txt`. On a fresh virtual environment, upgrade pip before installing:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Groq model access error

Set `GROQ_MODEL` to a model enabled for your Groq project. The default is the current production `openai/gpt-oss-120b`.

### Streamlit Cloud dependency failure

Make sure the deployment is using Python 3.12 and only this project's `requirements.txt`. Community Cloud uses the dependency file it finds for the app environment.

## Hackathon demo

1. Upload a fictional student's CV, project document, and certificate.
2. Build the profile.
3. Upload a fictional scholarship/job opportunity.
4. Analyze it.
5. Run Match Analysis.
6. Show matches, gaps, uncertainty, and readiness.
7. Ask “Why should I be selected?”
8. Show the answer plus evidence.
9. Generate the tailored resume.

## Scope

This is intentionally a stable hackathon MVP. Authentication, persistent multi-user databases, payment systems, mobile apps, admin dashboards, and complex analytics are intentionally outside the scope.
