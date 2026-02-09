import io
import re
from fastapi import UploadFile
import PyPDF2


async def parse_policy(file: UploadFile) -> str:
    """
    Extracts text from an uploaded policy file (PDF, TXT, DOCX).
    Returns cleaned policy text as a single string.
    """
    content = await file.read()
    filename = file.filename.lower()
    text = ""

    try:
        if filename.endswith(".txt"):
            text = content.decode("utf-8", errors="ignore")

        elif filename.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        elif filename.endswith(".docx"):
            try:
                from docx import Document
                doc = Document(io.BytesIO(content))
                for para in doc.paragraphs:
                    text += para.text + "\n"
            except ImportError:
                raise RuntimeError("python-docx not installed")

        else:
            raise ValueError("Unsupported file format")

    except Exception as e:
        raise RuntimeError(f"Failed to parse policy file: {str(e)}")

    return _clean_text(text)


def _clean_text(text: str) -> str:
    """
    Normalizes extracted text.
    """
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
