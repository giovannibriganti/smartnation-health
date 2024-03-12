import os
import pathlib
import tempfile
import uuid
import zipfile

import streamlit as st

from utils import FileProcessor

UPLOAD_FOLDER = "uploaded"
TXT_FOLDER = "extracted"

ROOT_PATH = pathlib.Path(__file__).parent


class FeedDb:
    def __init__(self):
        # if "folder_name" not in st.session_state:
        #     st.session_state["folder_name"] = str(uuid.uuid4())

        # self.folder_name = st.session_state["folder_name"]
        self.save_path = ROOT_PATH / UPLOAD_FOLDER
        self.extract_path = ROOT_PATH / TXT_FOLDER
        # self.uploaded_local_paths = []

    def save_uploaded_files(self):
        # self.save_path.mkdir(exist_ok=True, parents=True)

        with tempfile.TemporaryDirectory() as temp_dir:
            for uploaded_file in self.uploaded_files:
                
                subfolder = temp_dir / (str(uuid.uuid4()))
                subfolder.mkdir(exist_ok=True, parents=True)
                

                # ext = os.path.splitext(uploaded_file.name)[-1]
                # file_name = self.save_path / (str(uuid.uuid4()) + ext)

                # with file_name.open("wb") as f:
                #     f.write(uploaded_file.getbuffer())
                #     self.uploaded_local_paths.append(file_name)

        st.success(
            f"Successfully saved {len(self.uploaded_files)} files to {self.save_path}"
        )

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
                # self.extract_text()

        """Extract text from uploaded files and create markdown."""

    def extract_text(self):
        self.extract_path.mkdir(exist_ok=True, parents=True)

        if self.uploaded_local_paths:
            processor = FileProcessor(self.uploaded_local_paths)
            processor.process_files(self.extract_path)
            st.info("Markdown created successfully")

        """Run the app."""

    def run(self):
        self.create_app()


if __name__ == "__main__":
    app = FeedDb()
    app.run()
