from pathlib import Path
import json

from src.compliance.gap_engine import evaluate_control
from src.compliance.scoring import compute_compliance_score

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

print("Running compliance engine...\n")

results = []
for control in controls:
    result = evaluate_control(control, clauses)
    results.append(result)
    print(result)

summary = compute_compliance_score(results)

print("\n=== SUMMARY ===")
print(summary)
