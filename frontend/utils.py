import os
import fitz  # PyMuPDF
from docx import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader


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
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        text = ""

        for page in pages:
            text += page.page_content + "\n"
        return text

    def extract_text_from_docx(self, docx_path):
        doc = Document(docx_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text

    def extract_text_from_txt(self, txt_path):
        loader = TextLoader(txt_path)
        text = loader.load()[0].page_content
        return text

    def save_text(self, text, save_path):
        with open(save_path, "w") as file:
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

            filename = os.path.splitext(os.path.basename(file_path))[0] + ".txt"

            markdown_path = os.path.join(save_path, filename)
            self.save_text(text, markdown_path)
            print(f"Processed and saved: {markdown_path}")
