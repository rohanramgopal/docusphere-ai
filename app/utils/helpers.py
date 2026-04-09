import os
import re
import json
import fitz
from docx import Document as DocxDocument
from PIL import Image
import pytesseract

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx", ".png", ".jpg", ".jpeg"}


def allowed_file(filename: str) -> bool:
    _, ext = os.path.splitext(filename.lower())
    return ext in ALLOWED_EXTENSIONS


def save_json(data) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def load_json(data: str):
    if not data:
        return {}
    return json.loads(data)


def clean_text(text: str) -> str:
    text = text or ""
    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_text_from_pdf(file_path: str) -> str:
    text_parts = []
    with fitz.open(file_path) as doc:
        for page in doc:
            text_parts.append(page.get_text())
    return clean_text("\n".join(text_parts))


def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return clean_text(f.read())


def extract_text_from_docx(file_path: str) -> str:
    doc = DocxDocument(file_path)
    parts = [p.text for p in doc.paragraphs]
    return clean_text("\n".join(parts))


def extract_text_from_image(file_path: str) -> str:
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return clean_text(text)
    except Exception:
        return "OCR unavailable. Install Tesseract to extract text from images."


def extract_text(file_path: str) -> str:
    _, ext = os.path.splitext(file_path.lower())

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    if ext == ".txt":
        return extract_text_from_txt(file_path)
    if ext == ".docx":
        return extract_text_from_docx(file_path)
    if ext in {".png", ".jpg", ".jpeg"}:
        return extract_text_from_image(file_path)

    return ""


def determine_priority(text: str, doc_type: str) -> str:
    t = (text or "").lower()

    money_keywords = [
        "rs", "₹", "$", "usd", "inr", "amount", "total", "balance",
        "payment", "paid", "invoice", "bill", "receipt", "due",
        "transaction", "salary", "price", "cost", "gst", "tax"
    ]

    urgent_keywords = ["urgent", "asap", "immediate", "deadline", "notice", "critical", "overdue"]

    if doc_type == "legal":
        return "high"

    if any(word in t for word in money_keywords):
        return "high"

    if any(word in t for word in urgent_keywords):
        return "high"

    if doc_type in {"resume", "medical_report", "report", "support_ticket"}:
        return "medium"

    return "low"


def build_actions(text: str, doc_type: str, extracted_fields: dict) -> list:
    t = (text or "").lower()
    actions = []

    if doc_type == "invoice":
        actions.append("send_to_finance")
        actions.append("review_payment_details")
        if determine_priority(text, doc_type) == "high":
            actions.append("mark_urgent")

    elif doc_type == "resume":
        actions.append("send_to_hr_review")
        skills = extracted_fields.get("skills", [])
        if any(skill in skills for skill in ["python", "machine learning", "fastapi", "aws", "ai", "ml"]):
            actions.append("shortlist_candidate")
        if extracted_fields.get("emails") or extracted_fields.get("phones"):
            actions.append("contact_candidate")

    elif doc_type == "legal":
        actions.append("send_for_legal_review")
        if "renewal" in t:
            actions.append("review_renewal_terms")
        if "termination" in t or "notice" in t:
            actions.append("review_legal_risk")

    elif doc_type == "medical_report":
        actions.append("send_for_medical_review")
        if determine_priority(text, doc_type) == "high":
            actions.append("mark_urgent")

    elif doc_type == "support_ticket":
        actions.append("assign_support_agent")
        if determine_priority(text, doc_type) == "high":
            actions.append("mark_urgent")

    elif doc_type == "report":
        actions.append("send_for_management_review")

    else:
        actions.append("store_for_manual_review")

    return actions


def simple_field_extractor(text: str, doc_type: str) -> dict:
    result = {"document_type": doc_type}

    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    phones = re.findall(r'(?:\+91[-\s]?)?\b\d{10}\b', text)
    amounts = re.findall(r'(?:₹|Rs\.?|INR|\$)\s?[\d,]+(?:\.\d{1,2})?', text)
    dates = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', text)

    if emails:
        result["emails"] = list(set(emails[:5]))
    if phones:
        result["phones"] = list(set(phones[:5]))
    if amounts:
        result["amounts"] = list(set(amounts[:5]))
    if dates:
        result["dates"] = list(set(dates[:5]))

    t = text.lower()

    if doc_type == "resume":
        skills = []
        known_skills = [
            "python", "java", "sql", "react", "fastapi",
            "flask", "machine learning", "docker", "aws", "git",
            "deep learning", "javascript", "html", "css", "ai", "ml",
            "vlsi", "embedded"
        ]
        for skill in known_skills:
            if skill in t:
                skills.append(skill)
        result["skills"] = skills

    if doc_type == "invoice":
        if "invoice" in t:
            result["has_invoice_keyword"] = True
        if "bill to" in t:
            result["has_bill_to"] = True

    if doc_type == "legal":
        if "termination" in t:
            result["has_termination_clause"] = True
        if "renewal" in t:
            result["has_renewal_clause"] = True
        if "notice" in t:
            result["has_legal_notice"] = True

    if doc_type == "support_ticket":
        if "urgent" in t or "high priority" in t:
            result["priority_flag"] = "high"

    result["priority"] = determine_priority(text, doc_type)
    result["actions"] = build_actions(text, doc_type, result)

    return result
