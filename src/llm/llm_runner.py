from src.llm.llm_engine import Phi3PolicyDraftingEngine

def run_llm_on_gaps(compliance_results):
    """
    Runs Phi-3 on all non-ADEQUATE controls with progress logging.
    """
    engine = Phi3PolicyDraftingEngine()
    outputs = []

    non_adequate = [g for g in compliance_results if g["status"] != "ADEQUATE"]
    total = len(non_adequate)

    print(f"[LLM] Total gaps to process: {total}")

    for idx, gap in enumerate(non_adequate, start=1):
        print(f"\n[LLM] ({idx}/{total}) Processing {gap['control_id']}")

        # 1️⃣ Risk explanation
        print("[LLM] → explain_gap")
        explanation = engine.explain_gap(gap)
        print("[LLM] ✓ explain_gap done")

        # 2️⃣ Policy rewrite (most important)
        print("[LLM] → rewrite_policy")
        rewritten = engine.rewrite_policy(gap)
        print("[LLM] ✓ rewrite_policy done")

        # 3️⃣ Roadmap
        print("[LLM] → generate_roadmap")
        roadmap = engine.generate_roadmap(gap)
        print("[LLM] ✓ generate_roadmap done")

        outputs.append({
            "control_id": gap["control_id"],
            "control_name": gap["control_name"],
            "status": gap["status"],
            "severity": gap["severity"],
            "risk_explanation": explanation,
            "rewritten_policy": rewritten,
            "improvement_roadmap": roadmap
        })

    print("\n[LLM] All gaps processed.")
    return outputs
