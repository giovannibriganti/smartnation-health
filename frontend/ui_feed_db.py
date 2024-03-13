import pathlib
import tempfile
import uuid
import zipfile
import logging

import streamlit as st

from utils import FileProcessor

UPLOAD_FOLDER = "uploaded"
TXT_FOLDER = "extracted"

ROOT_PATH = pathlib.Path(__file__).parent


class FeedDb:
    def __init__(self):
        self.save_path = ROOT_PATH / TXT_FOLDER

    def save_uploaded_files(self):

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = pathlib.Path(temp_dir)
            for uploaded_file in self.uploaded_files:

                subfolder = temp_dir / (str(uuid.uuid4()))
                subfolder.mkdir(exist_ok=True, parents=True)

                # extract uploaded zip file inf subfolder
                with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
                    zip_ref.extractall(subfolder)

            st.success(
                f"Successfully saved {len(self.uploaded_files)} files to {str(temp_dir)}"
            )

            self.extract_text(temp_dir)

    def create_app(self):
        st.set_page_config(page_icon="📄", layout="wide", page_title="SmartNation")
        st.image("assets/logo.png", width=200)
        st.title("Feed Database")
        self.uploaded_files = st.file_uploader(
            "Upload your files",
            type=[".zip"],
            accept_multiple_files=True,
        )

        if self.uploaded_files:
            if st.button("Create Database"):
                self.save_uploaded_files()

    def extract_text(self, temp_dir):
        """Extract text from uploaded files and create markdown."""
        self.save_path.mkdir(exist_ok=True, parents=True)

        processor = FileProcessor(temp_dir)
        processor.process_files(self.save_path)
        st.info("Text files created successfully")

    def run(self):
        """Run the app."""
        self.create_app()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = FeedDb()
    app.run()
