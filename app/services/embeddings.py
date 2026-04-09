import math


def embed_text(text: str):
    text = (text or "").lower()
    words = text.split()

    return [
        len(text),
        len(words),
        text.count("invoice"),
        text.count("resume"),
        text.count("contract"),
        text.count("python"),
        text.count("amount"),
        text.count("date"),
    ]


def cosine_similarity(a, b) -> float:
    if not a or not b:
        return 0.0

    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)