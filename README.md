# 🚀 DocuSphere AI  
### Smart Document Intelligence & Workflow Automation Platform

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![AI](https://img.shields.io/badge/AI-NLP-orange)
![License](https://img.shields.io/badge/License-MIT-purple)

---

## 🌟 What is DocuSphere AI?

DocuSphere AI is an intelligent document processing platform that allows users to upload any type of document while enabling employers to instantly understand, prioritize, and act on them.

Instead of manually reviewing files, the system automatically extracts content, identifies document type, generates key highlights, assigns priority, and suggests actions — making workflows faster and smarter.

---
## 🏗️ Architecture Diagram

```mermaid
flowchart TD

A[👤 User / Candidate] --> B[📄 Upload Portal]

subgraph Frontend
    B --> F1[Enter Name]
    B --> F2[Upload Document]
end

B -->|HTTP Request| C[⚙️ FastAPI Backend]

subgraph Backend
    C --> R1[Upload API]
    C --> R2[Processing Engine]
end

subgraph AI Processing
    R2 --> P1[📑 Text Extraction]
    P1 --> P1A[PDF Parser]
    P1 --> P1B[DOCX Parser]
    P1 --> P1C[OCR - Tesseract]

    P1 --> P2[🧠 Document Classification]
    P2 --> P3[🔍 Field Extraction]
    P3 --> P4[✨ Keyword Summary (Top 5)]
    P4 --> P5[🚨 Priority Detection]
    P5 --> P6[⚡ Action Triggering]
end

P6 --> D[(🗄 Database - SQLite)]

subgraph Storage
    D --> S1[Documents Table]
end

D --> E[🧑‍💼 Employer Dashboard]

subgraph Employer View
    E --> V1[View Documents]
    E --> V2[See Type]
    E --> V3[See Keywords]
    E --> V4[See Priority]
    E --> V5[Download File]
end

E --> Q[❓ QA System]
Q -->|Ask Questions| R2
```
---

## ⚙️ How It Works

1. User uploads a document  
2. Text is extracted (OCR used for images)  
3. AI identifies document type  
4. Important fields are extracted  
5. Top 5 keywords are generated  
6. Priority is assigned  
7. Suggested actions are created  
8. Employer views everything in dashboard  

---

## ✨ Key Features

### 📄 Candidate Submission Portal
- Simple form (name + upload)
- Supports PDF, DOCX, TXT, JPG, PNG
- Clean and professional UI

### 🤖 AI Processing Engine
- Document classification (resume, invoice, legal, etc.)
- Smart keyword-based summarization
- OCR using Tesseract for images
- Field extraction (email, phone, skills)

### 🧑‍💼 Employer Dashboard
- Secure login system
- View all uploaded documents
- Displays:
  - Candidate Name
  - Document Type
  - Keywords Summary
  - Priority Level
- Download documents instantly

---

## 📊 Supported Document Types

- Resume / CV  
- Invoice / Receipt / Bill  
- Legal Documents / Contracts  
- Medical Reports  
- General Files  

---

## 🚨 Priority Logic

- 💰 Money / Payment / Invoice → **HIGH**
- ⚖️ Legal / Contract → **HIGH**
- 📄 Resume → **MEDIUM**
- 📁 Others → **LOW**

---

## 🧠 Example Output

**Resume**  
Type: Resume  
Summary: fresher, python, ai ml, 2024 graduate, projects  
Priority: Medium  

**Invoice**  
Type: Invoice  
Summary: amount, total, payment due, invoice number, date  
Priority: High  

---

## 💼 Use Cases

- Resume screening  
- Invoice processing  
- Legal document analysis  
- Medical report summarization  
- Customer support document intake  
- Workflow automation systems  

---

## 🏗 Architecture Overview

User → Upload Portal → FastAPI Backend → AI Processing  
→ Database Storage → Employer Dashboard  

---

## 🛠 Tools & Technologies

- FastAPI (Backend)
- SQLite + SQLAlchemy (Database)
- HTML + CSS + Jinja2 (Frontend)
- HuggingFace Transformers (AI/NLP)
- pytesseract (OCR)
- PyMuPDF (PDF extraction)
- python-docx (DOCX parsing)
- Pillow (Image processing)

---

## ▶️ How to Run

```bash
# Activate environment
source venv/bin/activate

# Run server
python -m uvicorn app.main:app --reload

# Open browser
http://127.0.0.1:8000

🔐 Employer Login

Username: employer1
Password: 1234

🚀 Future Improvements

Multi-user authentication
Cloud deployment (AWS/GCP)
Email notifications
Advanced AI summaries
Analytics dashboard
Role-based access

💡 Why This Project?

Combines AI + Full Stack
Real-world document workflow automation
Handles multiple document formats
Clean UI with intelligent backend
Portfolio + placement ready project

👨‍💻 Made by Rohan Ramgopal
