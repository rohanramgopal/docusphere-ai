from app.utils.helpers import simple_field_extractor


def extract_fields(text: str, doc_type: str) -> dict:
    return simple_field_extractor(text, doc_type)