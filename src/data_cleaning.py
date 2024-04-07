from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredHTMLLoader,
    JSONLoader,
    UnstructuredMarkdownLoader,
)
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.chroma import Chroma
from langchain.docstore.document import Document

import pandas as pd


def accept_document_return_chunks(document: str, path: str):
    """
    Accepts a document, creates chunks, embeds the chunks, and writes to a vector store.

    Parameters
    ----------
    document : str
        Path to the document to be processed.
    path : str
        Path to write the vector store.

    Returns
    -------
    List[Document]
        Chunks of text from the document.

    Raises
    ------
    ValueError
        If the file type is not supported.
    """
    if document.split(".")[-1] == "pdf":
        loader = PyPDFLoader(document)
    elif document.split(".")[-1] == "txt":
        loader = TextLoader(document)
    elif document.split(".")[-1] == "json":
        loader = JSONLoader(document,'')
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

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=250,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False,
    )

    docs = text_splitter.create_documents([unify_content])

    Chroma.from_documents(docs, embedder, persist_directory=path)

    return docs


def get_text_chunks_langchain(text_list, ids):
    """
    Creates Document objects from a list of texts.

    Parameters
    ----------
    text_list : List[str]
        List of texts.
    ids : List[str]
        List of identifiers for texts.

    Returns
    -------
    List[Document]
        List of Document objects.
    """
    docs = [
        Document(page_content=x, metadata={"ids": id}) for x, id in zip(text_list, ids)
    ]

    return docs


def snomed_embedding(
    snomed_descriptions_path: str,
    vector_db_path: str,
    nrows: int | None = None,
    demo: bool = False,
) -> None:
    """
    Embeds SNOMED descriptions and writes to a vector store.

    Parameters
    ----------
    snomed_descriptions_path : str
        Path to the SNOMED descriptions file.
    vector_db_path : str
        Path to write the vector store.
    nrows : int | None, optional
        Number of rows to read from the SNOMED descriptions file, by default None.
    demo : bool, optional
        Whether to run in demo mode, by default False.
    """
    if demo:
        all_df = pd.read_csv(snomed_descriptions_path, sep="\t")

        df = pd.concat(
            [all_df.sample(5000), all_df[all_df["term"].str.contains("myocard")]],
            axis=0,
        )
        print(df)

        del all_df

    else:
        if nrows is None:
            df = pd.read_csv(snomed_descriptions_path, sep="\t")
        else:
            df = pd.read_csv(snomed_descriptions_path, sep="\t", nrows=nrows)
            print(df)

    embedder = SentenceTransformerEmbeddings(
        model_name="dangvantuan/sentence-camembert-large",
    )

    unique_id = df["id"].tolist()
    p_id = df["conceptId"].tolist()
    term = df["term"].tolist()

    new_unique_id = [f"{x}_{y}" for x, y in zip(unique_id, p_id)]

    docs = get_text_chunks_langchain(term, new_unique_id)
    Chroma.from_documents(docs, embedder, persist_directory=vector_db_path)


if __name__ == "__main__":

    snomed_embedding(
        snomed_descriptions_path="./dataset/snomed/french/sct2_Description_Snapshot-fr_BE1000172_20231115.txt",
        vector_db_path="./snomed_fr/",
        demo=True,
    )
