import io
import re
from fastapi import UploadFile
import PyPDF2


async def parse_policy(file: UploadFile) -> list[str]:
    """
    Extracts and normalizes text from a policy file (PDF, TXT, DOCX)
    and returns a list of meaningful policy clauses.
    """
    content = await file.read()
    filename = file.filename.lower()
    raw_text = ""

    try:
        if filename.endswith(".txt"):
            raw_text = content.decode("utf-8", errors="ignore")

        elif filename.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    raw_text += page_text + "\n"

        elif filename.endswith(".docx"):
            try:
                from docx import Document
                doc = Document(io.BytesIO(content))
                for para in doc.paragraphs:
                    raw_text += para.text + "\n"
            except ImportError:
                raise RuntimeError("python-docx not installed")

        else:
            raise ValueError("Unsupported file format")

    except Exception as e:
        raise RuntimeError(f"Failed to parse policy file: {str(e)}")

    # Normalize and extract clauses
    cleaned_text = _clean_text(raw_text)
    clauses = _extract_clauses(cleaned_text)

    return clauses


# -------------------------------------------------------------------
# Text Normalization
# -------------------------------------------------------------------
def _clean_text(text: str) -> str:
    """
    Aggressive normalization for policy documents.
    Ensures consistent input across PDF, DOCX, TXT.
    """

    # Lowercase
    text = text.lower()

    # Fix hyphenated line breaks (e.g., "man-\nagement")
    text = re.sub(r'-\s*\n\s*', '', text)

    # Normalize newlines to spaces
    text = re.sub(r'\n+', ' ', text)

    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text)

    # Remove non-policy noise (keep punctuation useful for clauses)
    text = re.sub(r'[^a-z0-9.,;:() ]', '', text)

    return text.strip()


# -------------------------------------------------------------------
# Clause Extraction (KEY UPGRADE)
# -------------------------------------------------------------------
def _extract_clauses(text: str) -> list[str]:
    """
    Converts normalized policy text into meaningful policy clauses.

    This makes PDF, DOCX, and TXT behave at the same logical level
    for compliance evaluation.
    """

    # Split on common policy boundaries
    raw_clauses = re.split(
        r'\.\s+|;\s+|\n\d+\.\s+|\n-\s+|\n•\s+',
        text
    )

    # Filter out noise and short fragments
    clauses = [
        clause.strip()
        for clause in raw_clauses
        if len(clause.strip()) >= 40
    ]

    return clauses
