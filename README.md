# Policy Gap Analyzer

**Policy Gap Analyzer** is an intelligent cybersecurity compliance system that evaluates organizational policy documents against structured security controls. It generates explainable remediation guidance using a locally hosted Large Language Model (Phi-3 Mini).

The system enforces a **strict separation** between deterministic compliance logic and AI-based text generation, ensuring accuracy, explainability, and audit readiness.

---

## 🔍 Overview

Organizations often struggle to understand where their policies fall short, why gaps matter, and how to remediate them in a formal, audit-ready manner.

**Policy Gap Analyzer addresses this by:**
* Performing **deterministic, non-AI** compliance gap analysis.
* Using AI **only** for controlled explanation and drafting.
* Operating **fully offline** using a locally hosted LLM.

---

## 🚀 Features

### 📄 Policy Parsing
* Supports **TXT**, **PDF**, and **DOCX** files.
* Cleans, normalizes, and tokenizes policy content automatically.

### ✅ Deterministic Gap Analysis (No AI)
* Evaluates policies against predefined security controls.
* **Identifies control status:**
    * 🟢 ADEQUATE
    * 🟡 WEAK
    * 🔴 MISSING
* Assigns severity and computes **Overall Compliance Percentage** & **Organizational Maturity Level**.
* *Note: All compliance decisions are fully deterministic and auditable.*

### 🧠 AI-Powered Policy Improvement (Phi-3 Mini)
* Uses **Microsoft Phi-3 Mini (3.8B)** via Ollama.
* For each identified gap, generates:
    1.  **Risk Explanation:** Why the gap matters.
    2.  **Remediation:** Formal, audit-ready policy language.
    3.  **Roadmap:** High-level steps for improvement.
* Uses one consolidated LLM call per control gap for consistency.

### 🔗 End-to-End Orchestration
* Full pipeline from `Policy Upload` → `Gap Detection` → `Remediation Guidance`.
* Designed for offline and asynchronous governance workflows.

---

## 🏗️ System Architecture

The system follows a two-member modular architecture with strict responsibility boundaries.

### 1️⃣ Compliance Engine (Member 1)
**Type:** Deterministic | Non-AI | Authoritative

* **Responsibilities:**
    * Loads control definitions from `data/controls/nist_controls.json`.
    * Parses policy content and evaluates required control elements.
    * Assigns Status (ADEQUATE, WEAK, MISSING) and Severity.
    * Computes Compliance Percentage and Maturity Level.
* **Role:** This engine is the **single source of truth** for compliance decisions.

### 2️⃣ Policy Improvement Engine (Member 2)
**Type:** Generative | Non-Decisional

* **Implementation:** `src/llm/llm_engine.py`
* **Responsibilities:**
    * Consumes structured gap data from the Compliance Engine.
    * Uses Phi-3 Mini to generate explanations and rewrites.
* **Strict Constraints:**
    * ❌ No compliance decisions.
    * ❌ No severity assignment.
    * ❌ No new controls or requirements.
    * ❌ No technical implementation steps.
* **Role:** Used **only** for explanation and drafting—never for judgment.

---

## 🧠 Key Design Decisions

### 🔹 Single Merged Prompt per Control
Each control gap triggers exactly one LLM call that generates the Risk Explanation, Policy Rewrite, and Roadmap simultaneously.
* **Benefits:** Improved performance, output consistency, and stronger explainability guarantees.

### 🔹 Offline Governance Model
Compliance remediation is treated as a governance task, not a real-time workload.
* **Priorities:** Accuracy, Explainability, Audit Readiness.

---

## 🛠️ Setup & Installation

### Prerequisites
* **Python 3.10+**
* **Ollama** (Installed and running locally)

### Installation Steps

**1. Clone Repository & Create Virtual Environment**
```bash
git clone <repository-url>
cd Policy_gap_analyzer

# Linux/Mac
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

**2. Install Python Dependencies**


```bash
pip install -r requirements.txt

**3. Install and Configure Ollama (Required)**

```bash
# Install Ollama (Linux/Mac)
curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh

# Pull the Phi-3 Mini model
ollama pull phi3:3.8b

Ensure the Ollama service is running before executing the pipeline.

🏃 Usage
CLI Pipeline (Recommended for Testing)
Run the full compliance analysis and LLM generation pipeline:

```Bash
python test_full_pipeline.py

Outputs:

Compliance summary (percentage + maturity).

List of control gaps.

For each gap: Risk explanation, Rewritten policy text, and Improvement roadmap.

```API Mode (Optional)
Run the FastAPI backend:

```Bash
uvicorn src.app:app --reload

Provides endpoints for policy upload, compliance analysis, and remediation generation.

📂 Project Structure
Plaintext
.
├── data/
│   ├── controls/               # Control definitions (JSON)
│   └── sample_policies/        # Test policy documents
├── src/
│   ├── compliance/             # Deterministic gap analysis logic
│   ├── llm/                    # Phi-3 Policy Improvement Engine
│   ├── parser/                 # Policy file parsing (PDF/DOCX/TXT)
│   └── app.py                  # FastAPI backend
├── test_full_pipeline.py       # End-to-end pipeline test
├── ui.py                       # Streamlit UI (optional)
└── requirements.txt
⚠️ Important Notes
AI output is never authoritative.

Compliance decisions are fully deterministic.

Generated policy text is assistive and not a replacement for human review.

The system is designed for auditability, traceability, and governance.

📝 License
Proprietary — Internal Use Only