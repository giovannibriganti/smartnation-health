import pathlib
import tempfile
import uuid
import zipfile
import logging
import sys

import streamlit as st
from utils import FileProcessor, make_footer


UPLOAD_FOLDER = "uploaded"
TXT_FOLDER = "extracted"

ROOT_PATH = pathlib.Path(__file__).parent
ASSETS_PATH = ROOT_PATH / "assets"

BACKEND_PATH = ROOT_PATH.parent / "src"
sys.path.append(str(BACKEND_PATH))

import load_data  # noqa


class FeedDb:
    """
    Class to create a Streamlit app for generating a database from uploaded files.

    Attributes:
        save_path (pathlib.Path): The path where the extracted text files will be saved.
    """

    def __init__(self):
        """
        Initializes the FeedDb object.

        Sets up Streamlit page configuration and session state variables.
        """
        self.save_path = ROOT_PATH / TXT_FOLDER

        st.set_page_config(page_icon="📄", layout="wide", page_title="SmartNation")

        if "upload_done" not in st.session_state:
            st.session_state.upload_done = False

        if "uploading" not in st.session_state:
            st.session_state.uploading = False

        if "upload_id" not in st.session_state:
            st.session_state.upload_id = 0
        if "uploaded_files" not in st.session_state:
            st.session_state.uploaded_files = []

    def save_uploaded_files(self):
        """
        Saves uploaded files, extracts text from them, and creates a database.

        Uses a temporary directory to extract uploaded zip files and processes them to generate
        text files. Then, loads the data into the database.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = pathlib.Path(temp_dir)
            for uploaded_file in st.session_state.uploaded_files:

                subfolder = temp_dir / (str(uuid.uuid4()))
                subfolder.mkdir(exist_ok=True, parents=True)

                # extract uploaded zip file in subfolder
                with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
                    zip_ref.extractall(subfolder)

            with st.spinner("Fichiers téléchargés, conversion en cours"):
                generated_files = self.extract_text(temp_dir)

        with st.spinner("Création de la base de données"):
            for file_name in generated_files:
                load_data.load_data(file_name)

    def create_app(self):
        """
        Creates the Streamlit app interface.

        Handles file uploading, database generation, and displays success message.
        """
        if "upload_button" in st.session_state and st.session_state.upload_button:
            st.session_state.uploading = True
            st.session_state.upload_id += 1

        if st.session_state.upload_done:
            st.session_state.uploading = False

        logo_path = str(ASSETS_PATH / "logo_vivalia.svg")
        st.image(logo_path, width=200)
        st.title("Création de base de données")
        uploaded_files_ = st.file_uploader(
            "Fournissez votre base de données",
            type=[".zip"],
            accept_multiple_files=True,
            disabled=st.session_state.uploading,
            key=f"file_uploader_{st.session_state.upload_id}",
        )
        if uploaded_files_:
            st.session_state.uploaded_files = uploaded_files_

        if st.button(
            "Générer la base de données",
            disabled=(not uploaded_files_) or st.session_state.uploading,
            key="upload_button",
        ):
            self.save_uploaded_files()
            st.session_state.upload_done = True
            st.rerun()

        if st.session_state.upload_done:
            st.session_state.uploaded_files = []
            st.success("Base de donnée générée")
            st.session_state.upload_done = False

        make_footer(st, ASSETS_PATH)

    def extract_text(self, temp_dir):
        """
        Extracts text from uploaded files and creates markdown.

        Args:
            temp_dir (pathlib.Path): The temporary directory where uploaded files are extracted.

        Returns:
            List[str]: A list of file names of the extracted text files.
        """
        self.save_path.mkdir(exist_ok=True, parents=True)

        processor = FileProcessor(temp_dir)
        return processor.process_files(self.save_path)

    def run(self):
        """Runs the Streamlit app."""
        self.create_app()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = FeedDb()
    app.run()
