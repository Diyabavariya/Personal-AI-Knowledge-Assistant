import os
from pypdf import PdfReader
from docx import Document


def load_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def load_docx(file_path):
    doc = Document(file_path)
    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


def load_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".txt":
        return load_txt(file_path)

    if ext == ".pdf":
        return load_pdf(file_path)

    if ext == ".docx":
        return load_docx(file_path)

    raise ValueError(f"Unsupported file format: {ext}")
