import math
from collections import Counter

def calculate_entropy(text):
    counter = Counter(text)
    length = len(text)
    probabilities = [count / length for count in counter.values()]
    entropy = -sum(p * math.log2(p) for p in probabilities)
    return entropy


def entropy_check(url):
    entropy = calculate_entropy(url)
    if entropy > 4:
        return 15, "High entropy detected (random-looking URL)"
    return 0, None
