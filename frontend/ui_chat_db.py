import streamlit as st

class Chatbot:
    def __init__(self):
        pass

    def create_chatbot(self):   
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
        
        if prompt := st.chat_input():
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            request = {"question": prompt, 
                        "chat_history": "",
                        "patient_id": self.patient_id}

            with st.spinner('Writing...'):
                response = self.dummy_response(request)
            
            msg = {
                "content": response["answer"],
                "role": "assistant"
            }
            st.session_state.messages.append(msg)
            
            st.chat_message("assistant").write(response["answer"])
    
    def dummy_response(self, prompt):
        try:
            if self.patient_id:
                response = {"answer": f'Patient with ID: {self.patient_id} is in process'}
            else:
                response = {"answer": "Please enter the patient ID first"}
        
        except Exception as e:
            print(e)
            response = {"answer": "Please enter the patient ID first"}

        return response 
    
    def send_question(self, question):
        with st.spinner('Writing...'):
            response = self.dummy_response({"question": question, "chat_history": ""})
        
        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.messages.append({"role": "assistant", "content": response["answer"]})

    def create_sidebar(self):
        st.set_page_config(page_icon="💬", page_title="SmartNation")
        st.sidebar.image("assets/logo.png", width=200)
        st.sidebar.title('Chat with Database')
        st.sidebar.markdown('Please enter the patient ID and start asking your questions')

        st.sidebar.divider()

        st.sidebar.header('Patient ID')
        self.patient_id = st.sidebar.text_input('Patient ID', label_visibility='hidden')

        st.sidebar.divider()

        suggested_questions = [
            "What is the patient name?",
            "When was the latest visit of this patient?",
            "What is the latest treatment?"
        ]

        st.sidebar.subheader("Suggested Questions")
        for question in suggested_questions:
            if st.sidebar.button(question):
                self.send_question(question)

    def run(self):
        self.create_sidebar()
        self.create_chatbot()


if __name__ == "__main__":
    app = Chatbot()
    app.run()