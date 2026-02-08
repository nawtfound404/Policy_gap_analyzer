"""
Phi-3 Mini
"""

import subprocess
from typing import Dict


class Phi3PolicyDraftingEngine:

    def __init__(
        self,
        model_name: str = "gemma3:12b",
        temperature: float = 0.2,
        top_p: float = 0.9,
        max_tokens: int = 300,
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens

    # ---------------------------
    # Public API
    # ---------------------------

    def generate_gap_response(
        self,
        control_id: str,
        control_intent: str,
        gap_description: str,
    ) -> Dict[str, str]:
        """
        Generates:
        - Risk explanation
        - Revised policy clause
        - Roadmap suggestion
        """
        prompt = self._build_prompt(
            control_id, control_intent, gap_description
        )

        raw_output = self._call_model(prompt)
        parsed_output = self._parse_response(raw_output)

        return {
            "control_id": control_id,
            "risk_explanation": parsed_output["risk_explanation"],
            "policy_clause": parsed_output["policy_clause"],
            "roadmap": parsed_output["roadmap"],
        }

    # ---------------------------
    # Internal helpers
    # ---------------------------

    def _build_prompt(self, control_id, control_intent, gap_description):
        return f"""
    You are assisting in drafting cybersecurity policy documentation.

    Control:
    {control_id}

    Control Intent:
    {control_intent}

    Identified Gap:
    {gap_description}

    Tasks:
    1. Explain why this gap poses a security or operational risk.
    2. Draft a high-level formal policy clause that addresses this gap.
    3. Suggest one short-term and one long-term improvement action.

    Return your response EXACTLY in the following format:

    1. Risk Explanation:
    <text>

    2. Policy Clause:
    <text>

    3. Roadmap:
    Short-term: <text>
    Long-term: <text>

    Constraints:
    - Use formal, governance-appropriate policy language
    - Draft role-based requirements generically (e.g., "designated personnel", "assigned roles")
    - Do NOT name specific job titles, individuals, or departments
    - Do NOT define exact timelines in hours or days
    - Do not introduce requirements beyond the stated control intent
    - Do not reference NIST or external standards explicitly
    - Be concise and precise
    """

    def _call_model(self, prompt: str) -> str:
        """
        Calls Phi-3 Mini via Ollama.
        """
        process = subprocess.run(
            ["ollama", "run", self.model_name],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        if process.returncode != 0:
            raise RuntimeError(
                f"Ollama error: {process.stderr.decode('utf-8')}"
            )

        return process.stdout.decode("utf-8")

    def _parse_response(self, response_text: str) -> Dict[str, str]:
        """
        Parses the model response into structured sections.
        """
        sections = {
            "risk_explanation": "",
            "policy_clause": "",
            "roadmap": "",
        }

        current_section = None

        for line in response_text.splitlines():
            line = line.strip()

            if line.startswith("1."):
                current_section = "risk_explanation"
                continue
            elif line.startswith("2."):
                current_section = "policy_clause"
                continue
            elif line.startswith("3."):
                current_section = "roadmap"
                continue

            if current_section and line:
                sections[current_section] += line + " "

        # Final cleanup
        for key in sections:
            sections[key] = sections[key].strip()

        return sections


# ---------------------------
# Local test (manual validation)
# ---------------------------

if __name__ == "__main__":
    engine = Phi3PolicyDraftingEngine()

    result = engine.generate_gap_response(
        control_id="RS.MA",
        control_intent="Define incident response roles, escalation paths, and response timelines",
        gap_description=(
            "The policy mentions incident handling but does not define "
            "roles, escalation paths, or response timelines."
        ),
    )

    from pprint import pprint
    pprint(result)