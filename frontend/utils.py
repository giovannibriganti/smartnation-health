import os
import pathlib
import fitz  # PyMuPDF
from docx import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader


class FileProcessor:
    """
    Convert PDF/TXT/DOCX to txt

    ### Example usage:
    ```Python
    file_paths = ['file1.pdf', 'file2.docx', 'file3.txt']
    processor = FileProcessor(file_paths)
    processor.process_files()

    ```
    """

    def __init__(self, root_dir: pathlib.Path):
        self.root_dir = root_dir

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

    def save_text(self, text, save_path: pathlib.Path, file_name: str):
        with save_path.open("a") as file:
            file.write(f"<FILE>{file_name}</FILE>\n")
            file.write(text)

    def process_files(self, save_path: pathlib.Path):

        glob = self.root_dir.glob("**/*")

        patient_dict = {}

        for file in glob:
            if not file.is_file():
                continue

            file_id = file.parent.name
            if not file_id in patient_dict:
                patient_dict[file_id] = []

            patient_dict[file_id].append(file)

        for patient_id, file_list in patient_dict.items():
            patient_file = save_path / f"{patient_id}.txt"

            for file_path in file_list:
                if file_path.suffix == ".pdf":
                    text = self.extract_text_from_pdf(file_path)
                elif file_path.suffix == ".docx":
                    text = self.extract_text_from_docx(file_path)
                elif file_path.suffix == ".txt":
                    text = self.extract_text_from_txt(file_path)
                else:
                    print(f"Unsupported file type: {file_path}")
                    continue

                self.save_text(text, patient_file, file_path.name)
            print(f"Processed and saved patient: {patient_id}")
