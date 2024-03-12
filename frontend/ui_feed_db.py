import os
import streamlit as st
import uuid
from utils import FileProcessor

class FeedDb:
    def __init__(self):
        if 'folder_name' not in st.session_state:
            st.session_state['folder_name'] = str(uuid.uuid4())

        self.folder_name = st.session_state['folder_name']
        self.save_path = os.path.join('data_in', self.folder_name)
        self.uploaded_local_paths= []

    def save_uploaded_files(self, uploaded_files):
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

        for uploaded_file in uploaded_files:
            with open(os.path.join(self.save_path, uploaded_file.name), 'wb') as f:
                f.write(uploaded_file.getbuffer())
                self.uploaded_local_paths.append(os.path.join(self.save_path, uploaded_file.name))
                
        st.success(f"Successfully saved {len(uploaded_files)} files to {self.save_path}")

    def create_app(self):
        st.set_page_config(page_icon="📄", layout="wide", page_title='SmartNation')
        st.image('assets/logo.png', width=200)
        st.title('Feed Database')
        self.uploaded_files = st.file_uploader('Upload your files', type=['pdf', 'txt', 'docx', 'doc'], accept_multiple_files=True)

        if self.uploaded_files:
            if st.button('Create Database'):
                self.save_uploaded_files(self.uploaded_files)
                self.create_markdown()
    
    def create_markdown(self):
        if self.uploaded_local_paths:
            processor = FileProcessor(self.uploaded_local_paths)
            path_markdown = processor.process_files()
            print(path_markdown)
            st.info('Markdown created successfully')

    
    def run(self):
        self.create_app()


if __name__ == '__main__':
    app = FeedDb()
    app.run()
