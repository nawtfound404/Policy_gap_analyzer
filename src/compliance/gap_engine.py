from typing import Dict, List

def evaluate_control(control: Dict, clauses: List[str]) -> Dict:
    text = " ".join(clauses)

    required = control.get("required_elements", [])

    found_elements = [el for el in required if el in text]
    missing_elements = [el for el in required if el not in text]

    if len(found_elements) == 0:
        status = "MISSING"
        reason = "No evidence of this control found in the policy."
    elif len(found_elements) < len(required):
        status = "WEAK"
        reason = f"Partially covered. Missing elements: {', '.join(missing_elements)}"
    else:
        status = "ADEQUATE"
        reason = "All required elements are present."

    return {
        "control_id": control["id"],
        "control_name": control["name"],
        "nist_function": control["function"],
        "status": status,
        "severity": control.get("severity", "Medium"),
        "missing_elements": missing_elements,
        "reason": reason
    }
