def classify_document(text: str, filename: str = "") -> str:
    t = (text or "").lower()
    f = (filename or "").lower()

    resume_keywords = [
        "education", "skills", "experience", "projects", "internship",
        "objective", "certifications", "bachelor", "curriculum vitae",
        "resume", "cgpa", "graduate"
    ]
    finance_keywords = [
        "invoice", "bill", "receipt", "amount", "payment", "balance",
        "transaction", "paid", "total", "gst", "tax invoice", "due"
    ]
    legal_keywords = [
        "agreement", "contract", "legal", "notice", "party", "parties",
        "termination", "renewal", "terms and conditions", "effective date"
    ]
    medical_keywords = [
        "patient", "diagnosis", "medical", "prescription", "blood test",
        "haemoglobin", "doctor", "hospital", "report values", "treatment"
    ]
    support_keywords = [
        "ticket", "issue", "incident", "support", "priority", "server down"
    ]
    report_keywords = [
        "report", "analysis", "findings", "conclusion", "executive summary"
    ]

    def score(keywords):
        return sum(1 for k in keywords if k in t)

    scores = {
        "resume": score(resume_keywords),
        "invoice": score(finance_keywords),
        "legal": score(legal_keywords),
        "medical_report": score(medical_keywords),
        "support_ticket": score(support_keywords),
        "report": score(report_keywords),
    }

    best_type = max(scores, key=scores.get)

    if scores[best_type] > 0:
        return best_type

    if f.endswith((".jpg", ".jpeg", ".png")) and any(k in t for k in ["education", "skills", "experience"]):
        return "resume"

    return "other"
