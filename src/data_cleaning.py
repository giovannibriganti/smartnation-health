from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredHTMLLoader,
    JSONLoader,
    UnstructuredMarkdownLoader,
)
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

# from langchain_experimental.text_splitter import SemanticChunker
# from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
# import numpy as np
import pandas as pd


def accept_document_return_chunks(document: str, path: str):
    """
    _description_
    This function accepts a document, creates chunks, embed the chunks and write to a vector store

    Parameters
    ----------
    document : str
        _description_
        takes the directory of the document to be processed

    Returns
    -------
    _type_
        _description_
        Chunks of text from the document

    Raises
    ------
    ValueError
        _description_
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

    # embedder = SentenceTransformerEmbeddings(
    #     model_name="Dr-BERT/DrBERT-7GB",
    # )

    embedder = SentenceTransformerEmbeddings(
        model_name="dangvantuan/sentence-camembert-large",
    )

    # semantic_splitter = SemanticChunker(embedder)

    # docs = semantic_splitter.create_documents([unify_content])

    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=250,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False,
    )

    docs = text_splitter.create_documents([unify_content])

    # patient_id = document.split("/")[-1].split(".")[0]

    # docs = docs + ["patient_id": patient_id]

    # print(patient_id, docs)

    Chroma.from_documents(docs, embedder, persist_directory=path)

    return docs


def get_text_chunks_langchain(text_list, ids):

    docs = [
        Document(page_content=x, metadata={"ids": id}) for x, id in zip(text_list, ids)
    ]

    return docs


def snomed_embedding(
    snomed_descriptions_path: str,
    vector_db_path: str,
    nrows: str | None = None,
    demo: bool = False,
) -> None:
    """
    _description_
    This function accepts a document, creates chunks, embed the chunks and write to a vector store

    Parameters
    ----------
    document : str
        _description_
        takes the directory of the document to be processed

    Returns
    -------
    _type_
        _description_
        Chunks of text from the document

    Raises
    ------
    ValueError
        _description_
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

    # full snomed
    # snomed_embedding(
    #     snomed_descriptions_path="./dataset/snomed/french/sct2_Description_Snapshot-fr_BE1000172_20231115.txt",
    #     vector_db_path="../../embeddings/snomed_fr/",
    # )

    # subset snomed for testing
    # snomed_embedding(
    #     snomed_descriptions_path="./dataset/snomed/french/sct2_Description_Snapshot-fr_BE1000172_20231115.txt",
    #     vector_db_path="../../embeddings/snomed_testing_fr/",
    #     nrows=2000,
    # )

    snomed_embedding(
        snomed_descriptions_path="./dataset/snomed/french/sct2_Description_Snapshot-fr_BE1000172_20231115.txt",
        vector_db_path="./snomed_fr/",
        demo=True,
    )
