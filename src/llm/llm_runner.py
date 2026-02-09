from src.llm.llm_engine import Phi3PolicyDraftingEngine


def run_llm_on_gaps(compliance_results):
    """
    Runs LLM on ALL non-adequate controls.
    ONE LLM call per control.
    """
    engine = Phi3PolicyDraftingEngine()
    outputs = []

    non_adequate = [
        g for g in compliance_results if g["status"] != "ADEQUATE"
    ]

    print(f"[LLM] Total gaps to process: {len(non_adequate)}")

    for idx, gap in enumerate(non_adequate, start=1):
        print(f"[LLM] ({idx}/{len(non_adequate)}) {gap['control_id']}")

        result = engine.generate_full_improvement(gap)

        outputs.append({
            "control_id": gap["control_id"],
            "control_name": gap["control_name"],
            "status": gap["status"],
            "severity": gap["severity"],
            **result,
        })

    print("[LLM] All gaps processed.")
    return outputs
