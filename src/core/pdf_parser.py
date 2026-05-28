from __future__ import annotations

import io
from pathlib import Path
from typing import Union

import PyPDF2
from loguru import logger


class PDFExtractionError(Exception):
    """Raised when PDF text cannot be extracted."""


def extract_text_from_pdf(source: Union[bytes, str, Path]) -> str:
    try:
        if isinstance(source, (str, Path)):
            with open(source, "rb") as f:
                raw = f.read()
        else:
            raw = source

        reader = PyPDF2.PdfReader(io.BytesIO(raw))

        if reader.is_encrypted:
            raise PDFExtractionError("PDF is password-protected.")

        pages: list[str] = []
        for i, page in enumerate(reader.pages):
            try:
                text = page.extract_text() or ""
                pages.append(text)
            except Exception as exc:
                logger.warning(f"Skipping page {i}: {exc}")

        full_text = "\n".join(pages)
        cleaned   = _clean_text(full_text)

        if len(cleaned) < 50:
            raise PDFExtractionError(
                "Extracted text is too short — the PDF may be image-based. "
                "Please upload a text-selectable PDF."
            )

        logger.info(f"Extracted {len(cleaned)} characters from {len(pages)}-page PDF.")
        return cleaned

    except PDFExtractionError:
        raise
    except Exception as exc:
        raise PDFExtractionError(f"Could not parse PDF: {exc}") from exc


def _clean_text(text: str) -> str:
    import re
    text = re.sub(r"[^\x09\x0A\x0D\x20-\x7E\u00A0-\uFFFF]", " ", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def get_page_count(source: Union[bytes, str, Path]) -> int:
    raw = source if isinstance(source, bytes) else open(source, "rb").read()
    return len(PyPDF2.PdfReader(io.BytesIO(raw)).pages)
