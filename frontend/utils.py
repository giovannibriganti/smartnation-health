import pathlib
import logging
import fitz  # PyMuPDF
from docx import Document
import streamlit as st


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

    def save_text(self, text, file, file_name: str):
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
            if patient_file.exists():
                logging.warning(
                    "Patient file exists: %s, overwriting", patient_file.name
                )

            with patient_file.open("w") as patient_fp:

                for file_path in file_list:
                    if file_path.suffix == ".pdf":
                        text = self.extract_text_from_pdf(file_path)
                    elif file_path.suffix == ".docx":
                        text = self.extract_text_from_docx(file_path)
                    elif file_path.suffix == ".txt":
                        text = self.extract_text_from_txt(file_path)
                    else:
                        logging.error("Unsupported file type: %s", file_path.name)
                        st.error(f"Unsupported file type: {file_path.name}")
                        continue

                    self.save_text(text, patient_fp, file_path.name)

            logging.info("Processed and saved patient: %s", patient_id)
