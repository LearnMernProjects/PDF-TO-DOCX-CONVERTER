from app.core.pdf_extract import (
    extract_best_text,
    pages_to_text,
    word_count
)

if __name__ == "__main__":
    pdf_path = "storage/uploadFiles/sample_resume2.pdf"

    text, source = extract_best_text(pdf_path)

    print("Selected extractor:", source)
    print("Word count:", word_count(text))
    print("\nFinal Extracted Text:\n")
    print(text)