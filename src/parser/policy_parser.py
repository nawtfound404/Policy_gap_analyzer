import io
import re
from fastapi import UploadFile
import PyPDF2

async def parse_policy(file: UploadFile) -> str:
    """
    Extracts text from an uploaded file (PDF, TXT, or DOCX).
    Returns a cleaned string of the content.
    """
    content = await file.read()
    filename = file.filename.lower()
    text = ""

    try:
        if filename.endswith(".txt"):
            text = content.decode("utf-8")
        
        elif filename.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        elif filename.endswith(".docx"):
            # Import here to avoid hard dependency if not used
            try:
                from docx import Document
                doc = Document(io.BytesIO(content))
                for para in doc.paragraphs:
                    text += para.text + "\n"
            except ImportError:
                return "Error: python-docx not installed. Cannot parse .docx files."
                
        else:
            return "Unsupported file format. Please upload PDF, TXT, or DOCX."

    except Exception as e:
        print(f"Error parsing file {filename}: {e}")
        return f"Error extracting text: {str(e)}"

    # Basic cleaning
    return _clean_text(text)

def _clean_text(text: str) -> str:
    """
    Cleans extracted text:
    - Removes excessive whitespace
    - Normalizes line breaks
    - Removes non-printable characters
    """
    # Replace multiple newlines with a single newline
    text = re.sub(r'\n+', '\n', text)
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()
