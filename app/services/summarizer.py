import re


def extract_keywords(text: str, doc_type: str) -> list[str]:
    t = text or ""
    lower = t.lower()
    keywords = []

    keyword_bank = {
        "resume": [
            "fresher", "experienced", "python", "java", "sql", "react", "fastapi",
            "machine learning", "deep learning", "ai", "ml", "data science",
            "docker", "aws", "git", "2024 graduate", "2025 graduate",
            "internship", "electronics", "embedded", "vlsi", "bengaluru"
        ],
        "invoice": [
            "invoice", "payment", "receipt", "amount", "balance", "due",
            "paid", "transaction", "gst", "tax invoice", "bill"
        ],
        "legal": [
            "agreement", "contract", "notice", "termination", "renewal",
            "effective date", "legal review", "terms"
        ],
        "medical_report": [
            "patient", "diagnosis", "medical", "doctor", "hospital",
            "blood test", "treatment", "critical"
        ],
        "support_ticket": [
            "ticket", "issue", "support", "incident", "priority", "urgent"
        ],
        "report": [
            "analysis", "findings", "summary", "recommendation", "conclusion"
        ],
    }

    for kw in keyword_bank.get(doc_type, []):
        if kw in lower:
            keywords.append(kw)

    year_matches = re.findall(r"\b(20\d{2})\b", t)
    for y in year_matches:
        grad_kw = f"{y} graduate"
        if grad_kw not in keywords and "graduate" in lower:
            keywords.append(grad_kw)

    tokens = re.findall(r"[A-Za-z][A-Za-z\+\#\.\-]{2,}", lower)
    stop_words = {
        "the", "and", "for", "with", "from", "that", "this", "have", "will",
        "your", "name", "file", "document", "candidate", "uploaded", "using",
        "project", "projects", "engineering", "college", "university",
        "program", "task", "function", "grade", "calculator", "create",
        "called", "returns", "value", "take", "marks", "print"
    }

    freq = {}
    for token in tokens:
        if token not in stop_words and len(token) > 2:
            freq[token] = freq.get(token, 0) + 1

    fallback = [k for k, _ in sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:10]]

    merged = []
    for item in keywords + fallback:
        clean = item.strip().lower()
        if clean and clean not in merged:
            merged.append(clean)

    return merged[:5]


def summarize_text(text: str, doc_type: str = "other") -> str:
    text = (text or "").strip()
    if not text:
        return "No meaningful content found"

    keywords = extract_keywords(text, doc_type)

    if not keywords:
        return "general document, manual review needed"

    return ", ".join(keywords)
