import streamlit as st

import pathlib
import sys

from utils import make_footer

ROOT_PATH = pathlib.Path(__file__).parent
ASSETS_PATH = ROOT_PATH / "assets"

BACKEND_PATH = ROOT_PATH.parent / "src"
sys.path.append(str(BACKEND_PATH))
import answer_questions  # noqa


class Chatbot:
    def __init__(self):
        st.set_page_config(page_icon="💬", page_title="SmartNation")

        if "patient_id" not in st.session_state:
            st.session_state.patient_id = ""

        if "chat_ready" not in st.session_state:
            st.session_state["chat_ready"] = False

        if "disable_validate" not in st.session_state:
            st.session_state["disable_validate"] = False

        if "disable_new" not in st.session_state:
            st.session_state["disable_new"] = False

        if "start" not in st.session_state:
            st.session_state["start"] = True

        if "patient_id" not in st.session_state:
            st.session_state.text_input_value = ""

        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"role": "assistant", "content": "Comment puis-je vous aider?"}
            ]

    def default_chatbot(self):
        st.title("Assistant virtuel de Vivalia")
        st.markdown(
            "Veuillez saisir l'ID patient et commencez à poser vos questions")
        # st.image(str(ASSETS_PATH / "default_view.png"))

    def create_chatbot(self):
        st.markdown(f"## Dossier patient:`{st.session_state.patient_id}`")
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input():
            st.session_state.messages.append(
                {"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)

            with st.spinner("Writing..."):
                if st.session_state.patient_id:
                    response = {
                        "answer": answer_questions.answer_question(
                            st.session_state.patient_id, prompt
                        )
                    }
                else:
                    response = {
                        "answer": "Veuillez saisir l'ID du patient d'abord"}

            msg = {"content": response["answer"], "role": "assistant"}
            st.session_state.messages.append(msg)

            st.chat_message("assistant").write(response["answer"])

    def send_question(self, question):
        with st.spinner("Writing..."):
            if st.session_state.patient_id:
                response = {
                    "answer": answer_questions.answer_question(
                        st.session_state.patient_id, question
                    )
                }

            else:
                response = {
                    "answer": "Veuillez saisir l'ID du patient d'abord"}

        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.messages.append(
            {"role": "assistant", "content": response["answer"]}
        )

    def create_sidebar(self):
        st.sidebar.image(str(ASSETS_PATH / "logo_vivalia.svg"), width=200)
        st.sidebar.title("Discutez avec la base de données")
        st.sidebar.markdown(
            "Veuillez saisir l'ID patient et commencez à poser vos questions"
        )

        st.sidebar.divider()

        if (
            "bt_validate" in st.session_state
            and st.session_state["bt_validate"]
            and st.session_state.patient_id
        ):
            st.session_state.disable_validate = True
            st.session_state.disable_new = False

        if "bt_new" in st.session_state and st.session_state["bt_new"]:
            st.session_state.messages = [
                {"role": "assistant", "content": "Comment puis-je vous aider?"}
            ]
            st.session_state.disable_new = True
            st.session_state.disable_validate = False
            st.session_state.chat_ready = False
        elif "bt_new" not in st.session_state:
            st.session_state.disable_new = True

        st.sidebar.header("Patient ID")

        self.patient_id_placeholder = st.sidebar.empty()
        st.session_state.patient_id = self.patient_id_placeholder.text_input(
            "Patient ID",
            label_visibility="hidden",
            disabled=st.session_state.disable_validate,
        )

        placeholder = st.sidebar.empty()

        col1, col2 = placeholder.columns(2)
        with col1:
            validate_id = st.sidebar.button(
                "Valider l'ID",
                disabled=st.session_state.disable_validate,
                key="bt_validate",
            )
        with col2:
            new_id = st.sidebar.button(
                "Changer de patient",
                disabled=st.session_state.disable_new,
                key="bt_new",
            )

        if validate_id or st.session_state.disable_validate:
            if st.session_state.patient_id:
                st.session_state.disable_validate = True
                st.session_state.disable_new = False
                st.session_state.chat_ready = True

                st.sidebar.divider()

                suggested_questions = [
                    "Quels sont les antécédents médicaux du patient?",
                    "Ce patient est-il diabétique?",
                    "Fournir des informations sur l'IMC et voir si le patient est en bonne santé",
                ]

                st.sidebar.subheader("Questions suggérées")
                for question in suggested_questions:
                    if st.sidebar.button(question):
                        self.send_question(question)

        if new_id or st.session_state.disable_new:
            st.session_state.messages = [
                {"role": "assistant", "content": "En quoi puis-je vous aider?"}
            ]
            st.session_state.disable_new = True
            st.session_state.disable_validate = False
            st.session_state.chat_ready = False

    def update_session(self):
        pass

    def run(self):
        self.create_sidebar()

        if st.session_state.chat_ready:
            self.create_chatbot()
        else:
            self.default_chatbot()
            make_footer(st, ASSETS_PATH, n_lines=2)


if __name__ == "__main__":
    app = Chatbot()
    app.run()
