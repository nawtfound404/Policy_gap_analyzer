from typing import Dict, List


# -----------------------------
# Policy Strength Signals
# -----------------------------
MANDATORY_TERMS = ["shall", "must", "required to"]
OWNERSHIP_TERMS = ["responsible", "accountable", "owner", "ownership"]
SCOPE_TERMS = ["applies to", "all systems", "organization-wide", "entire organization"]


def evaluate_control(control: Dict, clauses: List[str]) -> Dict:
    """
    Evaluates a single control against policy clauses using:
    - keyword + synonym matching
    - policy strength signals (mandatory language, ownership, scope)

    This allows the engine to distinguish:
    MISSING vs WEAK vs ADEQUATE realistically.
    """

    required_elements = control.get("required_elements", [])
    found_elements = set()
    strength_score = 0

    # -----------------------------
    # Deterministic Synonym Map
    # -----------------------------
    SYNONYMS = {
        "asset inventory": ["asset identification", "assets identified", "asset register"],
        "asset ownership": ["asset owner", "ownership assigned"],
        "classification": ["classified", "classification scheme"],
        "risk assessment": ["risk evaluated", "risk analysis", "assess risk"],
        "least privilege": ["minimum access", "restricted access"],
        "access control": ["access restricted", "access managed"],
        "incident response": ["security incident response", "incident handling"],
        "recovery plan": ["disaster recovery", "business continuity"],
        "logging": ["log events", "audit logs"],
        "monitoring": ["continuous monitoring", "system monitoring"],
        "data classification": ["data categorized", "information classification"],
        "encryption": ["encrypted", "cryptographic protection"],
    }

    # -----------------------------
    # Clause Evaluation
    # -----------------------------
    for clause in clauses:
        clause_strength = 0

        # Strength signals
        if any(term in clause for term in MANDATORY_TERMS):
            clause_strength += 1
        if any(term in clause for term in OWNERSHIP_TERMS):
            clause_strength += 1
        if any(term in clause for term in SCOPE_TERMS):
            clause_strength += 1

        # Element matching
        for element in required_elements:
            keywords = [element]
            if element in SYNONYMS:
                keywords.extend(SYNONYMS[element])

            if any(keyword in clause for keyword in keywords):
                found_elements.add(element)
                strength_score += clause_strength

    # -----------------------------
    # Status Determination
    # -----------------------------
    if not found_elements:
        status = "MISSING"
    elif len(found_elements) < len(required_elements):
        status = "WEAK"
    else:
        # All elements found — now check strength
        status = "ADEQUATE" if strength_score >= 2 else "WEAK"

    missing_elements = list(set(required_elements) - found_elements)

    # -----------------------------
    # Reasoning
    # -----------------------------
    if status == "MISSING":
        reason = "No explicit policy statements addressing this control were found."
    elif status == "WEAK":
        reason = (
            "The control is partially addressed or lacks strong policy language "
            "(mandatory terms, ownership, or scope)."
        )
    else:
        reason = "All required elements are explicitly defined with strong policy language."

    return {
        "control_id": control["id"],
        "control_name": control["name"],
        "nist_function": control["function"],
        "status": status,
        "severity": control["severity"],
        "missing_elements": missing_elements,
        "reason": reason,
    }