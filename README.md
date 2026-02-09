📜 Policy Gap Analyzer

An AI-powered cybersecurity compliance tool that analyzes organizational policy documents, evaluates them against selected NIST-aligned controls, identifies compliance gaps, and generates human-readable remediation content using a local Large Language Model (Phi-3 Mini).

🚀 Overview

The Policy Gap Analyzer performs end-to-end policy analysis:

Parses policy documents (PDF / DOCX / TXT)

Evaluates policy strength against predefined security controls

Classifies controls as ADEQUATE, WEAK, or MISSING

Uses an LLM to:

Explain security risks

Rewrite missing policy sections

Generate improvement roadmaps

The system is designed to differentiate between strong, enforceable policies and weak or descriptive documents, not just detect keywords.

🛠️ A. How to Run the Project
1️⃣ Clone the Repository

git clone https://github.com/nawtfound404/Policy_gap_analyzer
cd Policy_gap_analyzer
2️⃣ Create & Activate Virtual Environment

python -m venv venv source venv/bin/activate # Linux / macOS venv\Scripts\activate # Windows
3️⃣ Install Dependencies

pip install -r requirements.txt
4️⃣ Setup Ollama (Required for LLM)

This project uses Phi-3 Mini (3.8B) locally via Ollama.


# Install Ollama (Linux/macOS) curl -fsSL https://ollama.com/install.sh | sh # Pull the model ollama pull phi3:3.8b # Start the Ollama service ollama serve

Verify installation:


ollama --version
5️⃣ Run the Full Pipeline (CLI)

python test_full_pipeline.py

This runs:

Policy parsing

Compliance evaluation

LLM-based remediation generation

6️⃣ Run the UI (Streamlit)

streamlit run ui.py

Upload a policy file and view:

Compliance score

Risk explanations

Rewritten policy sections

Improvement roadmap

📦 B. Dependencies & Installation
Core Dependencies

Python 3.10+

FastAPI

Streamlit

PyPDF2

python-docx

Ollama (external)

Phi-3 Mini model

requirements.txt (example)

fastapi uvicorn streamlit PyPDF2 python-docx
🧠 C. Logic & Workflow (Core Explanation)
🔹 High-Level Workflow

Policy File ↓ Parser (PDF / DOCX / TXT) ↓ Clause Normalization ↓ Compliance Engine ↓ Control Classification ↓ LLM Policy Improvement ↓ Final Report
🔹 Step 1: Policy Parsing

Extracts raw text from uploaded files

Normalizes text aggressively

Converts content into policy clauses (not raw paragraphs)

Why this matters:

Clause-level parsing allows accurate compliance reasoning and avoids PDF formatting bias.

🔹 Step 2: Compliance Evaluation

Each control contains:

Required elements

Severity

NIST function mapping

For each control, the engine:

Matches required elements using keywords + safe synonyms

Evaluates policy strength signals:

Mandatory language (shall, must)

Ownership & accountability

Organizational scope

Control status:

MISSING → No enforceable policy

WEAK → Partial or weak language

ADEQUATE → Explicit, enforceable coverage

Compliance score is computed as an aggregate maturity indicator.

🔹 Step 3: LLM-Based Gap Resolution

Only WEAK and MISSING controls are sent to the LLM.

For each control (one call per control):

Risk Explanation (why the gap matters)

Rewritten Policy Section (audit-ready)

Improvement Roadmap (governance-focused steps)

The LLM does not decide compliance — it only generates content based on deterministic findings.

🔹 Step 4: Output

Final output includes:

Compliance percentage

Maturity level

Per-control gap analysis

AI-generated remediation content

⚠️ D. Limitations & Future Improvements
Current Limitations

Keyword-Based Matching

No semantic embeddings yet

Synonyms must be curated manually

Performance

LLM calls are sequential

Large policies with many gaps may take several minutes

Control Coverage

Limited to selected NIST-aligned controls

Not full NIST 800-53 catalog

PDF Quality

Scanned PDFs (images) are not supported (no OCR)

Future Improvements

🔮 Semantic embeddings for smarter clause matching

⚡ Parallel LLM execution for faster analysis

📊 Control-level scoring visualization

🧠 Context-aware policy rewriting

🏛️ Support for ISO 27001 / SOC 2 mappings

📄 OCR support for scanned documents

🎯 Design Philosophy (Important)

This system prioritizes enforceable policy commitments over descriptive text.

As a result:

Templates and guides score low

Real enterprise policies score higher

Compliance scores are conservative but defensible

📂 Project Structure

. ├── data/ │ ├── controls/ # NIST-aligned controls (JSON) │ └── sample_policies/ # Test policies ├── src/ │ ├── compliance/ # Compliance logic │ ├── parser/ # Policy parsing & normalization │ ├── llm/ # Phi-3 Mini integration │ └── app.py # API backend (optional) ├── ui.py # Streamlit UI ├── test_full_pipeline.py # End-to-end test └── requirements.txt
📝 License

Internal / Academic / Hackathon Use Only.