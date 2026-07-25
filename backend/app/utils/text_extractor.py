import io
import logging
import PyPDF2
import docx

logger = logging.getLogger(__name__)

def extract_text_from_pdf(content: bytes) -> str:
    """Extract raw text from PDF file bytes."""
    try:
        pdf_file = io.BytesIO(content)
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        return ""

def extract_text_from_docx(content: bytes) -> str:
    """Extract raw text from DOCX file bytes."""
    try:
        docx_file = io.BytesIO(content)
        doc = docx.Document(docx_file)
        text = ""
        for paragraph in doc.paragraphs:
            if paragraph.text:
                text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from DOCX: {e}")
        return ""

def extract_text(file_name: str, content: bytes) -> str:
    """Extract text from file based on file extension, with fallback."""
    ext = file_name.split(".")[-1].lower()
    if ext == "pdf":
        return extract_text_from_pdf(content)
    elif ext == "docx":
        return extract_text_from_docx(content)
    else:
        # Fallback to reading bytes as text if it's plain text
        try:
            return content.decode("utf-8")
        except Exception:
            return ""
