"""
Phi-3 Mini — Policy Improvement Module
"""

import subprocess
from typing import Dict


class Phi3PolicyDraftingEngine:

    def __init__(
        self,
        model_name: str = "phi3:3.8b",
        temperature: float = 0.2,
        top_p: float = 0.9,
        max_tokens: int = 300,
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens

    # -------------------------
    # MODE 1 — Explain Gap Risk
    # -------------------------
    def explain_gap(self, control_gap: Dict) -> str:
        """
        Explains why a control gap increases security or operational risk.
        Returns plain text explanation (3-4 sentences).
        """
        missing = control_gap.get('missing_elements', [])
        missing_str = ', '.join(missing) if isinstance(missing, list) else missing

        prompt = f"""You are a cybersecurity compliance expert.

Control: {control_gap.get('control_name', '')} ({control_gap.get('control_id', '')})
Status: {control_gap.get('status', '')}
Missing Elements: {missing_str}

Explain why this gap increases security or operational risk.

RESPONSE RULES
- Limit to 3–4 sentences
- Use clear, professional language
- Do NOT add new requirements
- Do NOT restate the input verbatim
- Do NOT include recommendations
- Plain English only

Return ONLY the explanation text."""

        return self._call_model(prompt).strip()

    # -------------------------
    # MODE 2 — Rewrite Policy
    # -------------------------
    def rewrite_policy(self, control_gap: Dict) -> str:
        """
        Writes formal policy text addressing only the missing elements.
        Returns formal policy text (1-2 paragraphs).
        """
        missing = control_gap.get('missing_elements', [])
        missing_str = ', '.join(missing) if isinstance(missing, list) else missing

        prompt = f"""You are a cybersecurity policy writer.

Control: {control_gap.get('control_name', '')} ({control_gap.get('control_id', '')})
Missing Elements: {missing_str}

Write a formal policy section that addresses ONLY the missing elements.

POLICY WRITING RULES
- Use "shall" or "must" language
- Clearly define responsibilities in role-based terms
- Cover all listed missing elements
- Stay strictly within this control's scope
- Suitable for direct inclusion in an enterprise policy document

STYLE REQUIREMENTS
- Formal
- Audit-ready
- 1–2 concise paragraphs
- No framework names
- No implementation details

Return ONLY the policy text."""

        return self._call_model(prompt).strip()

    # -------------------------
    # MODE 3 — Generate Roadmap
    # -------------------------
    def generate_roadmap(self, control_gap: Dict) -> str:
        """
        Provides actionable improvement steps for a control gap.
        Returns bullet list of 2-3 improvement actions.
        """
        prompt = f"""You are a cybersecurity advisor.

Control: {control_gap.get('control_name', '')} ({control_gap.get('control_id', '')})
Severity: {control_gap.get('severity', '')}

Provide 2–3 actionable improvement steps that address this control.

ROADMAP RULES
- Use concise bullet points
- Focus on governance and process
- No technical overload
- No timelines
- No new controls

Return ONLY a bullet list of actions."""

        return self._call_model(prompt).strip()

    # -------------------------
    # Internal Model Call
    # -------------------------
    def _call_model(self, prompt: str) -> str:
        """Calls Phi-3 Mini via Ollama."""
        process = subprocess.run(
            ["ollama", "run", self.model_name],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        if process.returncode != 0:
            raise RuntimeError(f"Ollama error: {process.stderr.decode('utf-8')}")

        return process.stdout.decode("utf-8")