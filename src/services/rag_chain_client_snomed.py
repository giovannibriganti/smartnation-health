from langchain_community.vectorstores import Chroma
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings


class Snomed_Simple_RAG:

    def __init__(self, patient_id: str, llm, config, top_k_context: int = 3):
        self.llm = llm
        self.patient_id = patient_id
        self.config = config
        self.top_k_context = top_k_context

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

    def set_retriever(self):
        self.retriever = self.db.as_retriever(search_kwargs={"k": self.top_k_context})

    def invoke_rag(
        self,
        prompt_context: str,
        prompt_template_llm: str,
        free_text_diagnostic: str | None = None,
    ) -> str | None:

        def parse_docs(docs):
            texts = ""
            for doc in docs:
                merged_snomed_ct_id = doc.metadata.get("ids")
                snomed_ct_id = merged_snomed_ct_id.split("_")[1].capitalize()
                texts += f"\n{doc.page_content} ({snomed_ct_id})"
            return texts

        print("VectorDB context--->", prompt_context)
        retrieved_contexts = self.retriever.get_relevant_documents(
            prompt_context,
            top_k=self.top_k_context,
        )
        print("Retrieved termns snomed--->", retrieved_contexts)

        context_text = parse_docs(retrieved_contexts)

        if free_text_diagnostic is None:
            prompt = prompt_template_llm.format(context=context_text)
        else:
            prompt = prompt_template_llm.format(
                context=context_text,
                free_text_diagnostic=free_text_diagnostic,
            )

        print("Final prompt ----->", prompt)

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
