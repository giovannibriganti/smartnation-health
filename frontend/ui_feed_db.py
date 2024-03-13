import pathlib
import tempfile
import uuid
import zipfile
import logging
import sys

import streamlit as st

from utils import FileProcessor

UPLOAD_FOLDER = "uploaded"
TXT_FOLDER = "extracted"

ROOT_PATH = pathlib.Path(__file__).parent
ASSETS_PATH = ROOT_PATH / "assets"

BACKEND_PATH = ROOT_PATH.parent / "src"
sys.path.append(str(BACKEND_PATH))
import load_data  # noqa


class FeedDb:
    def __init__(self):
        self.save_path = ROOT_PATH / TXT_FOLDER

        st.set_page_config(page_icon="📄", layout="wide",
                           page_title="SmartNation")

        if not "upload_done" in st.session_state:
            st.session_state.upload_done = False

        if not "uploading" in st.session_state:
            st.session_state.uploading = False

        if not "upload_id" in st.session_state:
            st.session_state.upload_id = 0
        if not "uploaded_files" in st.session_state:
            st.session_state.uploaded_files = []

    def save_uploaded_files(self):

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = pathlib.Path(temp_dir)
            for uploaded_file in st.session_state.uploaded_files:

                subfolder = temp_dir / (str(uuid.uuid4()))
                subfolder.mkdir(exist_ok=True, parents=True)

                # extract uploaded zip file inf subfolder
                with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
                    zip_ref.extractall(subfolder)

            with st.spinner("Fichiers téléchargés, conversion en cours"):
                generated_files = self.extract_text(temp_dir)

        with st.spinner("Création de la base de données"):
            for file_name in generated_files:
                load_data.load_data(file_name)

    def create_app(self):

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

        self.make_footer(ASSETS_PATH)

    def extract_text(self, temp_dir):
        """Extract text from uploaded files and create markdown."""
        self.save_path.mkdir(exist_ok=True, parents=True)

        processor = FileProcessor(temp_dir)
        return processor.process_files(self.save_path)

    def make_footer(self, assets_path: pathlib.Path):
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
        cols = st.columns(
            5)  # Adjust the number of columns based on the number of images
        images = [
            ('logo_bosa.png', 100),
            ('logo_ai4belgium.jpeg', 200),
            ('logo_spf_fr_nl.svg', 200),
            ('logo_vivalia.svg', 200),
            ('logo_umons.svg', 200),
            ('logo_uliege_faculte_medecine.png', 200),
            ('logo_isia.svg', 200),
            ('logo_nttdata.png', 200),
        ]

        # Display each image in a column
        for index, column in enumerate(cols):
            with column:
                logo_path = str(assets_path / images[index][0])
                logo_width = images[index][1]
                st.image(logo_path, width=logo_width)

    def run(self):
        """Run the app."""
        self.create_app()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = FeedDb()
    app.run()
