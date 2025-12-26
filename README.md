# PDF to Word Converter

## Overview
This project is a backend driven PDF to Word document conversion system built using Python and FastAPI. The goal of the project is to convert PDF files into Microsoft Word documents while preserving document structure, readability, and alignment as closely as possible.
Instead of attempting pixel perfect replication, which is not feasible due to fundamental differences between PDF and Word formats, the project focuses on reconstructing the logical structure and visual intent of the original document in a reliable and readable Word format.
The application provides a simple web interface where users can upload a PDF file and download the generated Word document.

---

## Problem Understanding
PDF documents store content using absolute positioning, graphical elements, and drawing instructions. Word documents, on the other hand, are flow based and rely on semantic structures such as paragraphs, headings, and tables.
Because of this difference, directly mapping PDF coordinates to Word layout leads to unstable and inconsistent results. The challenge is not only extracting text but also understanding how that text should behave once placed inside a Word document.
This project addresses the problem by focusing on structure, alignment intent, and readability rather than raw positioning.

---

## PDF Text Extraction Strategy
The project uses multiple PDF extraction libraries to handle different types of PDFs and edge cases.
Pdfplumber is used to extract structured text and layout related information. PyMuPDF is used to access lower level text positioning data which helps in understanding alignment intent. Pdfminer is used as a fallback when additional text completeness is required.
The extracted outputs are compared and the most reliable result is selected automatically. This approach improves robustness across different PDF formats.

---

## Text Normalization and Structuring

Once text is extracted, it is normalized to remove unnecessary whitespace, encoding artifacts, and layout noise.
The cleaned text is then structured into logical components such as document title, section headings, and section content. This structured representation forms the foundation for rebuilding the document in Word format.

---

## Semantic Alignment Handling
Absolute positioning from PDFs cannot be applied directly to Word documents. Instead, the project infers semantic alignment based on visual intent.
Text is categorized as left aligned, center aligned, or right aligned depending on its role in the document. Alignment is then applied using Word paragraph formatting rather than absolute coordinates. This ensures consistent behavior across different environments.

---

## Table Reconstruction Approach
Table creation is one of the most challenging aspects of PDF to Word conversion. In PDFs, tables are typically drawn using lines and shapes rather than being stored as structured table objects.
Because of this, automatically detecting rows, columns, borders, and merged cells is unreliable for generic documents. To handle this limitation, the project reconstructs form style tables using predefined Word table templates.
These templates include visible borders, fixed column widths, and controlled alignment to accurately replicate the structure of form based and legal documents.

---
## Word Document Generation
Word document generation is implemented using the python docx library. Paragraph formatting, font sizes, spacing, alignment, and table borders are applied programmatically to rebuild the document structure.
The focus is on producing a clean, readable, and professional Word document that closely matches the original PDF content.

---
## Backend API and Frontend Interface

The backend is implemented using FastAPI. It handles PDF uploads, runs the conversion pipeline, and returns the generated Word file as a downloadable response.
A minimal HTML frontend is served directly by the backend. This interface allows users to upload PDF files and download converted Word documents without requiring any additional frontend framework.

---
## Tech Stack
Python 3  
FastAPI  
python docx  
pdfplumber  
PyMuPDF  
pdfminer six  
HTML CSS and JavaScript

---
## How to Run Locally

Install dependencies using the requirements file.
Start the server using uvicorn.
Open the application in a browser and upload a PDF file to generate a Word document.

---
## Limitations

Pixel perfect layout replication is not possible due to differences between PDF and Word formats.
Generic automatic table detection is limited for complex or highly customized PDF layouts.
Template based table reconstruction is used to ensure reliability and consistency.

---
## Conclusion
This project demonstrates a practical and production oriented approach to PDF to Word conversion. By combining structured text extraction, semantic alignment, and template based table reconstruction, the solution achieves reliable and readable results suitable for real world document processing scenarios.
