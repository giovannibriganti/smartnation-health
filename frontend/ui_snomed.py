import pathlib
import sys
import streamlit as st

ROOT_PATH = pathlib.Path(__file__).parent
ASSETS_PATH = ROOT_PATH / "assets"

BACKEND_PATH = ROOT_PATH.parent / "src"
sys.path.append(str(BACKEND_PATH))

class SnomedApp:
    """
    Class to create a Streamlit app for interacting with SNOMED CT.

    Attributes:
        prompt (str): The prompt for the patient description.
    """

    def __init__(self):
        """Initializes the SnomedApp object."""
        self.prompt = None

    def dummy_call(self):
        """Dummy method to demonstrate a Streamlit text call."""
        st.text('This is a text call')

    def create_app(self):
        """Creates the Streamlit app interface."""
        st.set_page_config(page_icon="📄", page_title="SmartNation")
        st.image(str(ASSETS_PATH / "logo_vivalia.svg"), width=200)
        st.title("Veuillez saisir la description de votre patient")
        self.prompt = st.text_input('input', label_visibility='hidden', key='prompt')
        
        if 'prompt' in st.session_state and self.prompt:
            self.dummy_call()

if __name__ == "__main__":
    app = SnomedApp()
    app.create_app()
