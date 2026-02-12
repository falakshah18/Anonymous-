def calculate_risk(score_list):
    total_score = sum(score_list)

    # Cap max score
    if total_score > 100:
        total_score = 100

    if total_score >= 80:
        risk_level = "HIGH RISK"
    elif total_score >= 40:
        risk_level = "MEDIUM RISK"
    else:
        risk_level = "LOW RISK"

    return total_score, risk_level
