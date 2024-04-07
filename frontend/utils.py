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

    def extract_text_from_csv(self, csv_path: pathlib.Path) -> str:
        """Extract text from a csv file

        Args:
            csv_path (pathlib.Path): Path to the docx file

        Returns:
            str: Extracted text
        """
        with csv_path.open("r") as fp:
            text = fp.read()

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
        return text[0].page_content

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

        generated_files = []

        for patient_id, file_list in patient_dict.items():
            patient_file = save_path / f"{patient_id}.txt"
            generated_files.append(str(patient_file))
            if patient_file.exists():
                logging.warning(
                    "Patient file exists: %s, overwriting", patient_file.name
                )

            with patient_file.open("w", encoding="utf-8") as patient_fp:

                for file_path in file_list:
                    try:
                        if file_path.suffix.lower() == ".docx":
                            text = self.extract_text_from_docx(file_path)
                        elif file_path.suffix.lower() == ".csv":
                            text = self.extract_text_from_csv(file_path)
                        else:
                            text = self.extract_text_from_unstructured(str(file_path))

                        self.save_text(text, patient_fp, file_path.name)

                    except Exception:
                        exec_info = traceback.format_exc()
                        logging.error(
                            "Error processing file: %s, %s", file_path.name, exec_info
                        )
                        st.error(
                            f"Le format du fichier '{file_path.name}' n'est pas supporté. \
                            La génération va continuer sans ce fichier."
                        )

            logging.info("Processed and saved patient: %s", patient_id)

        return generated_files


def make_footer(st, assets_path: pathlib.Path, n_lines: int = 1):
    """Create the footer."""
    st.markdown(
        """
        ---
        <div style="text-align: center;">
            <p> Vivalia's Hackathon </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    images = (
        "logo_bosa.png",
        "logo_ai4belgium.svg",
        "logo_spf_fr_nl.svg",
        "logo_vivalia.svg",
        "logo_umons.svg",
        "logo_uliege_faculte_medecine.png",
        "logo_isia.svg",
        "logo_nttdata.png",
    )
    n_columns = len(images) // n_lines

    for line in range(n_lines):
        # Adjust the number of columns based on the number of images
        cols = st.columns(n_columns, gap="medium")

        # Display each image in a column
        for index, column in enumerate(cols):
            with column:
                try:
                    logo_path = str(assets_path / images[line * n_columns + index])
                    st.image(logo_path, use_column_width=True)
                finally:
                    pass

    st.markdown(
        """
        <div style="text-align: center;">
            <p> Powered by 
                <a href="https://vivalia.be">Vivalia</a>, 
                <a href="https://bosa.belgium.be/fr/AIhackathon">BOSA</a>, 
                <a href="https://ai4belgium.be/en/">AI4Belgium</a>, 
                <a href="https://www.health.belgium.be/en">FPS Health</a>, 
                <a href="https://web.umons.ac.be/">UMONS</a>, 
                <a href="https://www.facmed.uliege.be/cms/c_3211623/fr/faculte-de-medecine">ULIÈGE</a>, 
                <a href="https://nttdata.com">NTT DATA</a>, 
                and <a href="https://web.umons.ac.be/isia/en/">ISIA Lab</a> 
           </p>
        </div>
        
        ---
        
        """,
        unsafe_allow_html=True,
    )
