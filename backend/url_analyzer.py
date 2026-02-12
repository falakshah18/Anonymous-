import re
from config import SUSPICIOUS_TLDS, SHORTENERS, RISK_KEYWORDS

def check_ip_url(url):
    pattern = r"http[s]?://\d+\.\d+\.\d+\.\d+"
    if re.search(pattern, url):
        return 20, "IP-based URL detected"
    return 0, None


def check_suspicious_tld(url):
    for tld in SUSPICIOUS_TLDS:
        if url.endswith(tld):
            return 15, f"Suspicious TLD detected ({tld})"
    return 0, None


def check_shortener(url):
    for short in SHORTENERS:
        if short in url:
            return 10, "URL Shortener detected"
    return 0, None


def check_keywords(url):
    for word in RISK_KEYWORDS:
        if word in url.lower():
            return 10, f"Suspicious keyword detected ({word})"
    return 0, None
