from src.llm.llm_engine import Phi3PolicyDraftingEngine
from typing import List, Dict


def run_llm_on_gaps(compliance_results: List[Dict]) -> List[Dict]:
    """
    Runs Phi-3 Mini on all non-adequate controls.
    Uses ONE merged prompt per control to generate:
    - Risk explanation
    - Rewritten policy
    - Improvement roadmap
    """

    engine = Phi3PolicyDraftingEngine()
    outputs = []

    # Only process meaningful gaps
    gaps = [
        g for g in compliance_results
        if g["status"] in ("WEAK", "MISSING")
    ]

    print(f"[LLM] Total gaps to process: {len(gaps)}")

    for idx, gap in enumerate(gaps, start=1):
        control_id = gap.get("control_id", "UNKNOWN")
        control_name = gap.get("control_name", "UNKNOWN")

        print(f"[LLM] ({idx}/{len(gaps)}) Processing {control_id} — {control_name}")

        try:
            llm_result = engine.generate_full_improvement(gap)

            # Safety fallback in case model returns empty sections
            outputs.append({
                "control_id": control_id,
                "control_name": control_name,
                "status": gap["status"],
                "severity": gap["severity"],
                "risk_explanation": llm_result.get("risk_explanation", "").strip() or
                    "Risk explanation could not be generated.",
                "rewritten_policy": llm_result.get("rewritten_policy", "").strip() or
                    "No policy rewrite generated.",
                "improvement_roadmap": llm_result.get("improvement_roadmap", "").strip() or
                    "No improvement roadmap generated."
            })

        except Exception as e:
            print(f"[LLM] ⚠️ Failed for {control_id}: {str(e)}")

            # Fail gracefully — do NOT break pipeline
            outputs.append({
                "control_id": control_id,
                "control_name": control_name,
                "status": gap["status"],
                "severity": gap["severity"],
                "risk_explanation": "LLM generation failed.",
                "rewritten_policy": "LLM generation failed.",
                "improvement_roadmap": "LLM generation failed."
            })

    print("[LLM] All gaps processed.")
    return outputs