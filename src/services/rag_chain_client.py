from langchain_community.vectorstores import Chroma
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings


class Simple_RAG:

    def __init__(self, patient_id: str, llm, config):
        self.llm = llm
        self.patient_id = patient_id
        self.config = config

        if config.get("rag_setup").get("db"):
            self.set_database(type=config.get("rag_setup").get("db").get("type"))
            self.set_retriever()

    def set_database(self, type):

        if self.patient_id is not None:
            path = f'{self.config.get("rag_setup").get("db").get("path")}/{self.patient_id}'
        else:
            path = f'{self.config.get("rag_setup").get("db").get("path")}'

        if type == "chroma":
            embedding_function = SentenceTransformerEmbeddings(
                model_name="dangvantuan/sentence-camembert-large"
            )
            self.db = Chroma(
                persist_directory=path, embedding_function=embedding_function
            )
        else:
            raise NotImplementedError

    def set_retriever(self, k=3):
        self.retriever = self.db.as_retriever(search_kwargs={"k": k})

    def invoke_rag(self, prompt_context: str, prompt_template_llm: str) -> str | None:
        def parse_docs(docs):
            texts = ""
            for doc in docs:
                texts += doc.page_content
            return texts

        retrieved_contexts = self.retriever.get_relevant_documents(
            prompt_context,
            top_k=3,
        )

        context_text = parse_docs(retrieved_contexts)
        prompt = prompt_template_llm.format(context=context_text)
        if not context_text:
            return None

        llm_type = self.config.get("llm").get("type")

        if llm_type == "OpenAI":
            response = self.llm.invoke(prompt)
        elif llm_type == "AzureOpenAI":
            response = self.llm.invoke(prompt).content
        elif llm_type == "Mistral7B":
            response = self.llm(prompt)
        else:
            raise NotImplementedError(f"LLM type not implemented. {llm_type=}")

        return response
