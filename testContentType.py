from app.core.pdf_extract import extract_best_text
from app.core.pdf_contentType import group_content_under_headings

if __name__ == "__main__":
    pdf_path = "storage/uploadFiles/sample_resume2.pdf"

    text, source = extract_best_text(pdf_path)

    structured_doc = group_content_under_headings(text)

    print("TITLE:", structured_doc["title"])

    for heading, content in structured_doc["sections"].items():
        print("\n", heading)
        for line in content:
            print("-", line)
