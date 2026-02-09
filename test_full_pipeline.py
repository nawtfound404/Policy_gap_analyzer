from pathlib import Path
import json

from src.compliance.gap_engine import evaluate_control
from src.compliance.scoring import compute_compliance_score
from src.llm.llm_runner import run_llm_on_gaps

# Load controls
ROOT_DIR = Path(__file__).resolve().parent
CONTROLS_PATH = ROOT_DIR / "data" / "controls" / "nist_controls.json"

with open(CONTROLS_PATH, "r", encoding="utf-8") as f:
    controls = json.load(f)

# Load policy
POLICY_PATH = ROOT_DIR / "data" / "sample_policies" / "weak_policy.txt"

with open(POLICY_PATH, "r", encoding="utf-8") as f:
    policy_text = f.read().lower()

clauses = policy_text.split(".")

print("Running compliance...\n")

results = []
for control in controls:
    results.append(evaluate_control(control, clauses))

summary = compute_compliance_score(results)
print("SUMMARY:", summary)

print("\nRunning LLM on gaps...\n")

llm_results = run_llm_on_gaps(results)

for item in llm_results:
    print("\n========================")
    print(item["control_id"], item["control_name"])
    print("\nRISK:\n", item["risk_explanation"])
    print("\nPOLICY:\n", item["rewritten_policy"])
    print("\nROADMAP:\n", item["improvement_roadmap"])
