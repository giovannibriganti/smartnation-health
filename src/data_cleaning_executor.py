from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredHTMLLoader,
    JSONLoader,
    UnstructuredMarkdownLoader,
)
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.vectorstores.chroma import Chroma


def accept_document_return_chunks(document: str):
    """
    This function accepts a document, creates chunks, embed the chunks and write to a vector store
    """

    if document.split(".")[-1] == "pdf":
        loader = PyPDFLoader(document)
    elif document.split(".")[-1] == "txt":
        loader = TextLoader(document)
    elif document.split(".")[-1] == "json":
        loader = JSONLoader(document)
    elif document.split(".")[-1] == "html":
        loader = UnstructuredHTMLLoader(document)
    elif document.split(".")[-1] == "md":
        loader = UnstructuredMarkdownLoader(document)
    else:
        raise ValueError("File type not supported")

    pages = loader.load_and_split()

    unify_content = ""
    for page in pages:
        unify_content += "\n" + page.page_content

    embedder = SentenceTransformerEmbeddings(
        model_name="dangvantuan/sentence-camembert-large",
    )

    semantic_splitter = SemanticChunker(embedder)
    docs = semantic_splitter.create_documents([unify_content])
    patient_id = document.split("/")[-1].split(".")[0]

    # Define a directory for each ID:
    persist_dir = "./inputs/documents/" + patient_id

    # Load it to Vector DB
    Chroma.from_documents(docs, embedder, persist_directory=persist_dir)

    return patient_id
