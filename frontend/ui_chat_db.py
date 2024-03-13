import streamlit as st

class Chatbot:
    def __init__(self):
        st.set_page_config(page_icon="💬", page_title="SmartNation")

        if "chat_ready" not in st.session_state:
                st.session_state["chat_ready"] = False
        
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    def default_chatbot(self):
        st.title("Chatbot assistant de Vivalia")
        st.markdown("Veuillez saisir l'ID patient et commencez à poser vos questions")
        st.image("assets/default_view.png")

    def create_chatbot(self):   
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
        
        if prompt := st.chat_input():
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            request = {"question": prompt, 
                        "chat_history": "",
                        "patient_id": self.patient_id}

            with st.spinner('Writing...'):
                if self.patient_id:
                    response = self.dummy_response(request)
                else:
                    response = {"answer": "Please enter the patient ID first"}
            
            msg = {
                "content": response["answer"],
                "role": "assistant"
            }
            st.session_state.messages.append(msg)
            
            st.chat_message("assistant").write(response["answer"])
    
    def dummy_response(self, prompt):
        response = {"answer": "Ceci est la réponse de l'API"}
        
        return response 
    
    def send_question(self, question):
        with st.spinner('Writing...'):
            request = {"question": question, 
                        "chat_history": "",
                        "patient_id": self.patient_id}
            
            if self.patient_id:
                response = self.dummy_response(request)
            
            else:
                response = {"answer": "Veuillez saisir l'ID du patient d'abord"}
        
        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.messages.append({"role": "assistant", "content": response["answer"]})

    def create_sidebar(self):
        st.sidebar.image("assets/logo.png", width=200)
        st.sidebar.title('Chat with Database')
        st.sidebar.markdown('Veuillez saisir l\'ID patient et commencez à poser vos questions')
        
        st.sidebar.divider()

        st.sidebar.header('Patient ID')
        self.patient_id = st.sidebar.text_input('Patient ID', label_visibility='hidden')

        if self.patient_id:
            st.sidebar.divider()

            suggested_questions = [
                "Montre-moi les antécédents médicaux?",
                "Ce patient est-il diabétique?",
                "Fournir des informations sur l'IMC et voir si le patient est en bonne santé?"
            ]

            st.sidebar.subheader("Questions suggérées")
            for question in suggested_questions:
                if st.sidebar.button(question):
                    self.send_question(question)
            
            st.session_state.chat_ready = True
            
        else:
            st.session_state.chat_ready = False

    def run(self):
        self.create_sidebar()

        if st.session_state.chat_ready:
            self.create_chatbot()
        else:
            self.default_chatbot()


if __name__ == "__main__":
    app = Chatbot()
    app.run()