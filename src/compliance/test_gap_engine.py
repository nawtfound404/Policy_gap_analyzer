import json
from pathlib import Path

from src.parser.policy_parser import parse_policy
from src.compliance.gap_engine import evaluate_control
from src.compliance.scoring import compute_compliance_score
from src.compliance.grouping import group_by_function


# Resolve project root safely
ROOT_DIR = Path(__file__).resolve().parents[2]

POLICY_PATH = ROOT_DIR / "data" / "sample_policies" / "weak_policy.txt"
CONTROLS_PATH = ROOT_DIR / "data" / "controls" / "nist_controls.json"


def main():
    with open(CONTROLS_PATH, "r", encoding="utf-8") as f:
        controls = json.load(f)

    clauses = parse_policy(POLICY_PATH)

    results = []

    # ---- Run evaluation ONCE ----
    for control in controls:
        result = evaluate_control(control, clauses)
        results.append(result)

    # ---- Group by NIST function ----
    grouped_results = group_by_function(results)

    print("\n=== COMPLIANCE GAP ANALYSIS (GROUPED BY NIST FUNCTION) ===\n")

    for function, items in grouped_results.items():
        print(f"\n[{function}]")
        for item in items:
            print(
                f"  - {item['control_id']} ({item['control_name']}): "
                f"{item['status']} | Severity: {item['severity']}"
            )

    # ---- Overall compliance summary ----
    summary = compute_compliance_score(results)

    print("\n=== OVERALL COMPLIANCE SUMMARY ===")
    print(summary)


if __name__ == "__main__":
    main()
