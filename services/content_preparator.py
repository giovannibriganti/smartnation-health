from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings


def simple_text_split(content):
    text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
    )

    texts = text_splitter.create_documents([content])
    return texts



def recursive_splitter(chunk_size, overlap):
    text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=500,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
    )
    # texts = text_splitter.create_documents([content])

    return text_splitter



def semantic_chunker(embedder,breakpoint = "percentile"):
    text_splitter = SemanticChunker(embedder)
    # docs = text_splitter.create_documents([content])
    return text_splitter
