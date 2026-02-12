from difflib import SequenceMatcher
from config import TRUSTED_DOMAINS

def similarity_ratio(a, b):
    return SequenceMatcher(None, a, b).ratio()

def check_domain_similarity(url):
    for domain in TRUSTED_DOMAINS:
        ratio = similarity_ratio(url, domain)
        if ratio > 0.8 and ratio < 1:
            return 25, f"Possible spoofing detected (similar to {domain})"
    return 0, None
