import logging
import pathlib
import traceback

import streamlit as st

from docx import Document
from langchain_community.document_loaders import UnstructuredFileLoader


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

    def extract_text_from_docx(self, docx_path: pathlib.Path) -> str:
        """Extract text from a docx file

        Args:
            docx_path (pathlib.Path): Path to the docx file

        Returns:
            str: Extracted text
        """
        doc = Document(docx_path)
        text = ""

        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"

        return text

    def extract_text_from_unstructured(self, file_path: pathlib.Path) -> str:
        """Extract text from an unstructured file

        Args:
            file_path (pathlib.Path): Path to the unstructured file

        Returns:
            str: Extracted text
        """
        loader = UnstructuredFileLoader(file_path)
        text = loader.load()
        return text

    def save_text(self, text: str, file: pathlib.Path, file_name: str) -> None:
        """Save text to a file

        Args:
            text (str): Text to save
            file (pathlib.Path): File to save to
            file_name (str): Name of the file
        """
        file.write(f"<FILE>{file_name}</FILE>\n")
        file.write(text)

    def process_files(self, save_path: pathlib.Path) -> None:
        """Process files and save to a directory

        Args:
            save_path (pathlib.Path): Path to save the files
        """

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

            with patient_file.open("w", encoding="utf-8") as patient_fp:

                for file_path in file_list:
                    print("file_path", file_path)
                    try:
                        if file_path.suffix.lower() == ".docx":
                            text = self.extract_text_from_docx(file_path)

                        else:
                            text = self.extract_text_from_unstructured(
                                file_path)

                        print("save file", file_path.name,
                              patient_fp, file_path.name)
                        self.save_text(text, patient_fp, file_path.name)

                    except Exception:
                        exec_info = traceback.format_exc()
                        logging.error(
                            "Error processing file: %s, %s", file_path.name, exec_info
                        )
                        st.error(
                            f"Error processing file: {file_path.name}, {exec_info}")

            logging.info("Processed and saved patient: %s", patient_id)
