from app.core.pdf_extract import extract_best_text
from app.core.pdf_contentType import group_content_under_headings
from app.core.pdf_toWord import build_word_document
from app.core.pdf_extract import extract_lines_with_alignment

if __name__ == "__main__":
    pdf_path = "storage/uploadFiles/sample_resume2.pdf"
    output_docx = "storage/outputFiles/output.docx"
    text, source = extract_best_text(pdf_path)
    structured = group_content_under_headings(text)
    aligned_lines = extract_lines_with_alignment(pdf_path)
    build_word_document(structured, output_docx, aligned_lines)


    print("Word document generated at:", output_docx)
