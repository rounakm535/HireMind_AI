import io
import logging

logger = logging.getLogger(__name__)

try:
    import PyPDF2
except Exception:  # pragma: no cover - optional dependency
    PyPDF2 = None

try:
    import docx
except Exception:  # pragma: no cover - optional dependency
    docx = None

try:
    import pdfplumber
except Exception:
    pdfplumber = None

try:
    from pdfminer.high_level import extract_text as pdfminer_extract_text
except Exception:
    pdfminer_extract_text = None

def extract_text_from_pdf(content: bytes) -> str:
    """Extract raw text from PDF file bytes."""
    if PyPDF2 is None:
        logger.warning("PyPDF2 is not installed; attempting alternative PDF extractors")
        # Try pdfplumber first
        try:
            if pdfplumber is not None:
                pdf_file = io.BytesIO(content)
                with pdfplumber.open(pdf_file) as pdf:
                    pages = [p.extract_text() or "" for p in pdf.pages]
                text = "\n".join(pages).strip()
                if text:
                    return text
        except Exception as e:
            logger.debug(f"pdfplumber extraction failed: {e}")

        # Try pdfminer.six
        try:
            if pdfminer_extract_text is not None:
                pdf_file = io.BytesIO(content)
                text = pdfminer_extract_text(pdf_file)
                if text:
                    return text.strip()
        except Exception as e:
            logger.debug(f"pdfminer extraction failed: {e}")

        logger.warning("No PDF extraction libraries available or extraction failed; falling back to plaintext heuristics")
        return ""

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
    if docx is None:
        logger.warning("python-docx is not installed; skipping DOCX text extraction")
        return ""

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
    def _plaintext_fallback(b: bytes) -> str:
        # Try utf-8 then latin-1 decoding
        try:
            text = b.decode("utf-8")
        except Exception:
            try:
                text = b.decode("latin-1")
            except Exception:
                return ""

        # Heuristic: return if contains reasonable amount of whitespace/newlines
        if len(text.strip()) > 40:
            return text

        # Otherwise extract long printable substrings as a last resort
        import re

        chunks = re.findall(r"[\w\s\-\.,;:\(\)\[\]/]{20,}", text)
        return "\n\n".join(chunks).strip()

    if ext == "pdf":
        txt = extract_text_from_pdf(content)
        if not txt:
            # attempt plaintext fallback for PDFs when PyPDF2 is not available
            return _plaintext_fallback(content)
        return txt
    elif ext == "docx":
        txt = extract_text_from_docx(content)
        if not txt:
            return _plaintext_fallback(content)
        return txt
    else:
        return _plaintext_fallback(content)
