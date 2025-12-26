import pdfplumber
from typing import List, Dict
import fitz
import re
from pdfminer.high_level import extract_text as pdfminer_extract_text


# Alignment of text based on x-coordinate of pdf
def infer_alignment(x: float, page_width: float) -> str:
    center_left = page_width * 0.4
    center_right = page_width * 0.6
    right_threshold = page_width * 0.75

    if center_left <= x <= center_right:
        return "center"
    if x >= right_threshold:
        return "right"
    return "left"


def extract_text_from_pdf(pdf_path: str) -> List[Dict]:
    extracted_pages = []

    with pdfplumber.open(pdf_path) as pdf:
        for index, page in enumerate(pdf.pages):
            text = page.extract_text()
            lines = [line.strip() for line in text.split("\n") if line.strip()] if text else []

            extracted_pages.append({
                "page_number": index + 1,
                "lines": lines
            })

    return extracted_pages


def extract_text_pymupdf(pdf_path: str):
    doc = fitz.open(pdf_path)
    extracted_pages = []

    for page_index, page in enumerate(doc):
        page_width = page.rect.width
        blocks = page.get_text("dict")["blocks"]
        lines = []

        for block in blocks:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                text = ""
                x_positions = []

                for span in line["spans"]:
                    text += span["text"]
                    x_positions.append(span["bbox"][0])

                cleaned = text.strip()
                if not cleaned:
                    continue

                avg_x = sum(x_positions) / len(x_positions)

                lines.append({
                    "text": cleaned,
                    "alignment": infer_alignment(avg_x, page_width),
                    "x": avg_x,
                    "page_width": page_width
                })

        extracted_pages.append({
            "page_number": page_index + 1,
            "lines": lines
        })

    return extracted_pages

def extract_tables_pdfplumber(pdf_path: str):
    """
    Extracts table structures from PDF using pdfplumber.
    Returns raw table data per page.
    """
    import pdfplumber

    tables = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_index, page in enumerate(pdf.pages):
            page_tables = page.extract_tables()

            for table in page_tables:
                tables.append({
                    "page_number": page_index + 1,
                    "table": table  # list of rows, each row is list of cells
                })

    return tables

def pages_to_text(pages):
    all_lines = []

    for page in pages:
        for line in page["lines"]:
            if isinstance(line, str):
                all_lines.append(line)
            elif isinstance(line, dict):
                all_lines.append(line.get("text", ""))

    return "\n".join(all_lines)


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text)) if text else 0


def extract_best_text(pdf_path: str):
    text_pymupdf_pages = extract_text_pymupdf(pdf_path)
    text_pdfplumber_pages = extract_text_from_pdf(pdf_path)

    text_pymupdf = pages_to_text(text_pymupdf_pages)
    text_pdfplumber = pages_to_text(text_pdfplumber_pages)

    if word_count(text_pymupdf) > word_count(text_pdfplumber):
        final_text = text_pymupdf
        source = "pymupdf"
    else:
        final_text = text_pdfplumber
        source = "pdfplumber"

    final_text = normalize_cid(final_text)

    if "(cid:" in final_text:
        final_text = extract_text_pdfminer(pdf_path)
        source += " + pdfminer"

    return final_text, source


def extract_text_pdfminer(pdf_path: str) -> str:
    try:
        return pdfminer_extract_text(pdf_path) or ""
    except Exception:
        return ""


CID_MAP = {
    "127": "•",
    "120": "–",
    "121": "—",
    "133": "…",
}


def normalize_cid(text: str) -> str:
    def replace(match):
        return CID_MAP.get(match.group(1), "")
    return re.sub(r"\(cid:(\d+)\)", replace, text)

def extract_lines_with_alignment(pdf_path: str):
    """
    Returns alignment-aware lines for Word rendering.
    Uses PyMuPDF output (because it has coordinates).
    """
    pages = extract_text_pymupdf(pdf_path)

    aligned_lines = []

    for page in pages:
        for line in page["lines"]:
            aligned_lines.append({
                "text": line["text"],
                "alignment": line["alignment"]
            })

    return aligned_lines
