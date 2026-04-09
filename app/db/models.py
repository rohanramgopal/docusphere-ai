from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.db.database import Base


class Employer(Base):
    __tablename__ = "employers"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    role = Column(String, default="employer")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    candidate_name = Column(String, nullable=True)
    filename = Column(String, nullable=False)
    stored_path = Column(String, nullable=False)
    content_type = Column(String, nullable=True)

    extracted_text = Column(Text, nullable=True)
    document_type = Column(String, nullable=True)
    summary = Column(Text, nullable=True)
    extracted_fields = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
