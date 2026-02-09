import subprocess
from typing import Dict


class Phi3PolicyDraftingEngine:
    def __init__(
        self,
        model_name: str = "phi3:3.8b",
        temperature: float = 0.2,
        top_p: float = 0.9,
        max_tokens: int = 450,
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens

    # -------------------------------------------------
    # SINGLE MERGED PROMPT (ONE CALL PER CONTROL)
    # -------------------------------------------------
    def generate_full_improvement(self, control_gap: Dict) -> Dict:
        """
        Generates risk explanation, rewritten policy,
        and improvement roadmap in ONE LLM call.
        """

        missing = control_gap.get("missing_elements", [])
        missing_str = ", ".join(missing) if isinstance(missing, list) else missing

        prompt = f"""
You are a cybersecurity compliance expert.

Control: {control_gap.get('control_name')} ({control_gap.get('control_id')})
Severity: {control_gap.get('severity')}
Missing Elements: {missing_str}

TASKS:
1. Explain why this gap increases risk (2–3 sentences).
2. Write a formal policy section addressing ONLY the missing elements.
3. Provide 2–3 high-level improvement steps.

STRICT RULES:
- No new requirements
- No framework names
- No implementation details
- Formal, audit-ready language
- Be concise

FORMAT EXACTLY AS:

RISK:
<text>

POLICY:
<text>

ROADMAP:
- <bullet>
- <bullet>
"""

        output = self._call_model(prompt)
        return self._parse_output(output)

    # -------------------------------------------------
    # Helpers
    # -------------------------------------------------
    def _parse_output(self, text: str) -> Dict:
        sections = {
            "risk": "",
            "policy": "",
            "roadmap": "",
        }
    
        current = None
    
        for line in text.splitlines():
            clean = line.strip().lower()
    
            if clean.startswith("risk"):
                current = "risk"
                continue
            elif clean.startswith("policy"):
                current = "policy"
                continue
            elif clean.startswith("roadmap"):
                current = "roadmap"
                continue
            
            if current and line.strip():
                sections[current] += line.strip() + "\n"
    
        return {
            "risk_explanation": sections["risk"].strip(),
            "rewritten_policy": sections["policy"].strip(),
            "improvement_roadmap": sections["roadmap"].strip(),
        }


    def _call_model(self, prompt: str) -> str:
        try:
            process = subprocess.run(
                ["ollama", "run", self.model_name],
                input=prompt.encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=120,
            )
        except FileNotFoundError:
            return "[LLM unavailable] Ollama not installed."

        if process.returncode != 0:
            return process.stderr.decode("utf-8")

        return process.stdout.decode("utf-8")
