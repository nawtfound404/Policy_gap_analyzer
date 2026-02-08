# Policy Gap Analyzer

An intelligent cybersecurity compliance tool that automatically analyzes policy documents against NIST 800-53 controls, identifies gaps, and uses LLMs (Phi-3 Mini) to draft remediation plans.

## 🚀 Features

-   **Policy Parsing**: Extracts text from PDF, DOCX, and TXT files.
-   **Gap Analysis**: Compares policy content against NIST 800-53 controls using keyword matching and semantic analysis.
-   **AI Remediation**: Uses **Microsoft Phi-3 Mini** (via Ollama) to:
    -   Explain security risks of identified gaps.
    -   Draft formal, audit-ready policy clauses.
    -   Generate actionable improvement roadmaps.
-   **Orchestration**: Seamless pipeline from file upload to remediation report.

---

## 🏗️ Architecture

The system follows a modular "Member" architecture:

1.  **Compliance Engine (Member 1)**:
    -   Loads controls from `data/controls/nist_controls.json`.
    -   Parses user policy via `src/app.py` or `main.py`.
    -   Detects *Missing*, *Weak*, or *Adequate* controls.

2.  **Policy Improvement Module (Member 2)**:
    -   Powered by `src/llm/llm_engine.py`.
    -   Uses local LLM to generate governance artifacts.
    -   **Strict Constraints**: No decision making, only text generation based on Member 1's findings.

---

## 🛠️ Setup & Installation

### Prerequisites
-   Python 3.10+
-   [Ollama](https://ollama.com/) installed and running.

### 1. Clone & Environment
```bash
git clone <repository-url>
cd Policy_gap_analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Ollama (Required for LLM)
This project uses **Phi-3 Mini** (3.8B parameters) for local inference.
```bash
ollama pull phi3:3.8b
ollama serve
```

---

## 🏃 Usage

### CLI Mode (Recommended for testing)
Run the main orchestration script to analyze the sample policy (`data/sample_policies/weak_policy.txt`).

```bash
python main.py
```

**Output:**
-   Console log showing parsing status.
-   List of identified gaps.
-   For each gap: Risk Explanation, Proposed Policy Clause, and Roadmap.

### API Mode
Start the FastAPI server for the backend API.

```bash
uvicorn src.app:app --reload
```

---

## 📂 Project Structure

```
.
├── data/
│   ├── controls/           # NIST control definitions (JSON)
│   └── sample_policies/    # Test documents
├── src/
│   ├── compliance/         # Gap detection & control loading logic
│   ├── llm/                # LLM engine (Phi-3 interface)
│   ├── parser/             # File parsing (PDF/DOCX/TXT)
│   └── app.py              # FastAPI backend application
├── main.py                 # CLI entry point (glue code)
└── requirements.txt        # Python dependencies
```

## 📝 License
Proprietary / Internal Use Only.
