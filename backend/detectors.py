import re
from Levenshtein import distance

SUSPICIOUS_WORDS = ["urgent", "verify", "suspended", "click", "bank", "otp"]

PROMPT_INJECTION_PATTERNS = [
    "ignore previous instructions",
    "override system",
    "developer mode",
    "disable security"
]

def detect_phishing_text(text: str):
    score = 0
    for word in SUSPICIOUS_WORDS:
        if word in text:
            score += 15

    if "http" in text:
        score += 20

    return score


def detect_prompt_injection(text: str):
    score = 0
    for pattern in PROMPT_INJECTION_PATTERNS:
        if pattern in text:
            score += 30
    return score


def detect_suspicious_url(url: str):
    score = 0

    if len(url) > 75:
        score += 15

    if re.search(r"\d+\.\d+\.\d+\.\d+", url):
        score += 25

    if "-" in url:
        score += 10

    # Basic domain similarity check
    if distance(url, "paypal.com") < 3:
        score += 25

    return score
