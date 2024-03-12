import os
import fitz  # PyMuPDF
from docx import Document


class FileProcessor:
    """
    Convert PDF/TXT/DOCX to markdown

    ### Example usage:
    ```Python
    file_paths = ['file1.pdf', 'file2.docx', 'file3.txt']
    processor = FileProcessor(file_paths)
    processor.process_files()

    ```
    """

    def __init__(self, file_paths):
        self.file_paths = file_paths

    def extract_text_from_pdf(self, pdf_path):
        text = ""
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
        return text

    def extract_text_from_docx(self, docx_path):
        doc = Document(docx_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text

    def extract_text_from_txt(self, txt_path):
        with open(txt_path, "r") as file:
            text = file.read()
        return text

    def save_text(self, text, markdown_path):
        with open(markdown_path, "w") as file:
            file.write(text)

    def process_files(self, save_path):
        for file_path in self.file_paths:
            if file_path.endswith(".pdf"):
                text = self.extract_text_from_pdf(file_path)
            elif file_path.endswith(".docx"):
                text = self.extract_text_from_docx(file_path)
            elif file_path.endswith(".txt"):
                text = self.extract_text_from_txt(file_path)
            else:
                print(f"Unsupported file type: {file_path}")
                continue

            filename = os.path.split(file_path)[-1] + ".txt"

            markdown_path = os.path.join(save_path, filename)
            self.save_text(text, markdown_path)
            print(f"Processed and saved: {markdown_path}")
