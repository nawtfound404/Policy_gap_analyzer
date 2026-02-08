# Phi-3 Mini — Policy Improvement Module (Member 2)

This module (`src/llm/llm_engine.py`) serves as the **Policy Improvement Engine** (Member 2) of the Policy Gap Analyzer. It uses the **Phi-3 Mini** model via **Ollama** to generate explanatory and policy text based on identified control gaps.

## Overview

The `Phi3PolicyDraftingEngine` does **NOT** make compliance decisions. Its sole purpose is to transform structured gap data from the Compliance Engine (Member 1) into human-readable policy documentation and roadmaps.

### Core Capabilities
1.  **Explain Risks**: Why a gap matters.
2.  **Rewrite Policy**: Formal text to close the gap.
3.  **Generate Roadmaps**: Governance-focused improvement steps.

---

## Architecture

-   **Model**: Microsoft Phi-3 Mini (3.8B parameters)
-   **Interface**: Local subprocess calls to `ollama run phi3:3.8b`
-   **Design Principle**: Single Responsibility — one method per task mode. No decision-making logic.

---

## Usage Guide

### 1. Initialization
```python
from src.llm.llm_engine import Phi3PolicyDraftingEngine

# Initialize the engine
# Constraints: temperature=0.2 (low creativity), max_tokens=300
engine = Phi3PolicyDraftingEngine()
```

### 2. Modes

#### Mode 1: Explain Gap Risk
Explains why a specific gap poses a security or operational risk.
-   **Input**: `control_id`, `control_name`, `status`, `missing_elements`
-   **Output**: 3-4 sentences, plain English.

```python
gap_data = {
    "control_id": "PR.AC-1",
    "control_name": "Access Control Policy",
    "status": "Partial",
    "missing_elements": ["periodic review", "role-based access definitions"]
}

explanation = engine.explain_gap(gap_data)
print(explanation)
```

#### Mode 2: Rewrite Policy
Drafts formal policy text to address *only* the missing elements.
-   **Input**: `control_id`, `control_name`, `missing_elements`
-   **Output**: Formal, audit-ready text (shall/must language).

```python
policy_text = engine.rewrite_policy(gap_data)
print(policy_text)
```

#### Mode 3: Generate Roadmap
Suggests actionable steps to improve the control.
-   **Input**: `control_id`, `control_name`, `severity`
-   **Output**: Bullet list of governance actions (no timelines/tech details).

```python
roadmap_data = {
    "control_id": "PR.AC-1",
    "control_name": "Access Control Policy",
    "severity": "High"
}

roadmap = engine.generate_roadmap(roadmap_data)
print(roadmap)
```

---

## Requirements

### Prerequisite: Ollama
This module requires [Ollama](https://ollama.com/) to be installed and running locally with the Phi-3 model pulled.

```bash
# Install Ollama
# ...

# Pull the model
ollama pull phi3:3.8b
```

### Error Handling
The engine raises a `RuntimeError` if the Ollama subprocess fails (return code != 0). Ensure Ollama is running before initializing the engine.

---

## File Structure
`src/llm/llm_engine.py` contains the `Phi3PolicyDraftingEngine` class. It has been refactored to remove all legacy logic and now strictly follows the 3-mode architecture.
