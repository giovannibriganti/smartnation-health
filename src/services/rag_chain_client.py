from langchain_community.vectorstores.chroma import Chroma
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings


class Simple_RAG:
    """
    Represents a Simple Retriever-Augmented Generation (RAG) model.

    Attributes:
        patient_id (str): The ID of the patient.
        llm: The language model used for generation.
        config: The configuration settings.
        top_k_context (int): The number of top contexts to consider.

    """

    def __init__(self, patient_id: str, llm, config, top_k_context: int = 3):
        """
        Initializes the Simple_RAG instance.

        Args:
            patient_id (str): The ID of the patient.
            llm: The language model used for generation.
            config: The configuration settings.
            top_k_context (int, optional): The number of top contexts to consider. Defaults to 3.

        """
        self.llm = llm
        self.patient_id = patient_id
        self.config = config
        self.top_k_context = top_k_context

        if config.get("rag_setup").get("db"):
            self.set_database(type=config.get("rag_setup").get("db").get("type"))
            self.set_retriever()

    def set_database(self, type):
        """
        Sets the database for retrieval.

        Args:
            type (str): The type of database.

        Raises:
            NotImplementedError: If the database type is not implemented.

        """
        if self.patient_id is not None:
            path = f'{self.config.get("rag_setup").get("db").get("path")}/{self.patient_id}'
        else:
            path = f'{self.config.get("rag_setup").get("db").get("path")}'

        if type == "chroma":
            embedding_function = SentenceTransformerEmbeddings(model_name="BAAI/bge-m3")
            self.db = Chroma(
                persist_directory=path, embedding_function=embedding_function
            )
        else:
            raise NotImplementedError

    def set_retriever(self):
        """Sets the retriever."""
        self.retriever = self.db.as_retriever(search_kwargs={"k": self.top_k_context})

    def invoke_rag(
        self,
        prompt_context: str,
        prompt_template_llm: str,
        free_text_diagnostic: str | None = None,
    ) -> str | None:
        """
        Invokes the RAG model for generation.

        Args:
            prompt_context (str): The context for the prompt.
            prompt_template_llm (str): The template for the prompt for the language model.
            free_text_diagnostic (str, optional): Free text diagnostic information. Defaults to None.

        Returns:
            str | None: The generated response from the language model.

        Raises:
            NotImplementedError: If the language model type is not implemented.

        """

        def parse_docs(docs):
            texts = ""
            for doc in docs:
                texts += doc.page_content
            return texts

        retrieved_contexts = self.retriever.get_relevant_documents(
            prompt_context,
            top_k=self.top_k_context,
        )

        context_text = parse_docs(retrieved_contexts)

        if free_text_diagnostic is None:
            prompt = prompt_template_llm.format(context=context_text)
        else:
            prompt = prompt_template_llm.format(
                context=context_text,
                free_text_diagnostic=free_text_diagnostic,
            )

        if not context_text:
            return None

        llm_type = self.config.get("llm").get("type")

        if llm_type == "OpenAI":
            response = self.llm.invoke(prompt)
        elif llm_type == "AzureOpenAI":
            response = self.llm.invoke(prompt).content
        elif llm_type == "Mistral7B":
            response = self.llm(prompt)
        elif llm_type == "llama3":
            response = self.llm.invoke(prompt)
        else:
            raise NotImplementedError(f"LLM type not implemented. {llm_type=}")

        return response
