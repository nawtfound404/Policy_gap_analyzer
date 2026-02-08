def compute_compliance_score(results: list[dict]) -> dict:
    total_controls = len(results)
    score = 0

    for r in results:
        if r["status"] == "ADEQUATE":
            score += 100
        elif r["status"] == "WEAK":
            score += 50
        else:
            score += 0

    percentage = score / (total_controls * 100) * 100

    if percentage >= 80:
        maturity = "Strong"
    elif percentage >= 50:
        maturity = "Moderate"
    else:
        maturity = "Weak"

    return {
        "compliance_percentage": round(percentage, 2),
        "maturity_level": maturity
    }
