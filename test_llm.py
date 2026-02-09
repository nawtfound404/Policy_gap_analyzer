from src.llm.llm_engine import Phi3PolicyDraftingEngine

engine = Phi3PolicyDraftingEngine()

test_gap = {
    "control_id": "PR.DS",
    "control_name": "Data Security",
    "status": "WEAK",
    "severity": "Critical",
    "missing_elements": ["data classification", "key management"]
}

print("\n--- EXPLAIN GAP ---")
print(engine.explain_gap(test_gap))

print("\n--- REWRITE POLICY ---")
print(engine.rewrite_policy(test_gap))

print("\n--- ROADMAP ---")
print(engine.generate_roadmap(test_gap))
