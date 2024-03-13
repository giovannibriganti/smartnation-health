import streamlit as st
import pathlib
import sys

ROOT_PATH = pathlib.Path(__file__).parent
ASSETS_PATH = ROOT_PATH / "assets"

BACKEND_PATH = ROOT_PATH.parent / "src"
sys.path.append(str(BACKEND_PATH))

class SnomedApp:
    def __init__(self):
        pass

    def dummy_call(self):
        st.text('This is a text call')

    def create_app(self):
        st.set_page_config(page_icon="📄", page_title="SmartNation")
        st.image(str(ASSETS_PATH / "logo_vivalia.svg"), width=200)
        st.title("Veuillez saisir la description de votre patient")
        self.prompt = st.text_input('input', label_visibility='hidden', key='prompt')
        
        if 'prompt' in st.session_state and self.prompt:
            self.dummy_call()

    
if __name__ == "__main__":
    app = SnomedApp()
    app.create_app()