from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def get_chuncker_configs():
    configs = []

    config_simple = {
        "name" : "Simple",
        "params" : {
            "chunck_size" : 1000,
            "overlap" : 200,
            "separator": "\n\n",
            "length_function" : len,
            "is_separator_regex" : False
        }
    }

    config_recursive = {
        "name" : "Recursive",
        "params" : {
            "chunck_size" : 500,
            "overlap" : 20,
            "length_function" : len,
            "is_separator_regex" : False
        }
    }

    config_semantic = {
        "name" : "Semantic",
        "params" : {
            "breakpoint_threshold" : 90,
            "breakpoint_type" : "percentile",
            "number_of_chunks" : None
        }
    }

    configs.append(config_simple)
    configs.append(config_recursive)
    configs.append(config_semantic)

    return configs

def load_chunker(config, embedder=None):
    chunking_type = config.get("name")
    params = config.get("params")

    chunk_size = params.get("chunk_size")
    chunk_overlap =params.get("overlap")
    length_function = params.get("length_function") 
    regex_sep = params.get("is_separator_regex")

    if chunking_type == "Recursive":
        chunker = recursive_splitter(
            chunk_size=chunk_size,
            overlap = chunk_overlap,
            length_fn=length_function,
            regex_sep=regex_sep
            )
    
    elif chunking_type == "Simple":
        separator = params.get("separator")
        chunker = simple_text_split(
            separator=separator, 
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=length_function,
            is_separator_regex=regex_sep
            )
    
    else:
        breakpt_thres = params.get("breakpoint_threshold")
        chunk_nb = params.get("number_of_chunks")
        breakpt_type = params.get("breakpoint_type")

        if(embedder is None):
            raise Exception("Embeddings required for semantic chunker")

        chunker = semantic_chunker(
            embedder = embedder,
            breakpoint_threshold = breakpt_thres,
            number_of_chunks = chunk_nb, 
            breakpoint_type = breakpt_type
            )
    
    return chunker


def simple_text_split(separator, chunk_size, chunk_overlap, length_fn, regex_sep):
    
    text_splitter = CharacterTextSplitter(
        separator = separator,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=length_fn,
        is_separator_regex=regex_sep
    )
    #texts = text_splitter.create_documents([content])
    return text_splitter



def recursive_splitter(chunk_size, overlap, length_fn, regex_sep):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        length_function=length_fn,
        is_separator_regex=regex_sep
    )

    return text_splitter



def semantic_chunker(embedder, breakpoint_threshold, number_of_chunks, breakpoint_type):
    text_splitter = SemanticChunker(
        embedder,
        breakpoint_threshold_type = breakpoint_type,
        breakpoint_threshold_amount = breakpoint_threshold,
        number_of_chunks = number_of_chunks
    )
    return text_splitter




def topic_asigment(embedder, topics, chunk_text):
    """
    Determine the topic most related to a given chunk of text based on embeddings.

    Parameters:
        embedder: A function that takes a text input and returns its embedding.
        topics (list of str): List of topics in plain text.
        chunk (str): The chunk of text for which the related topic needs to be determined.

    Returns:
        str: The topic most related to the chunk.
    """
    # Generate embeddings for the chunk
    chunk_embedding = embedder(chunk_text)

    # Initialize variables to store maximum similarity score and related topic
    max_similarity = -1
    related_topic = None

    # Calculate similarity scores between chunk embedding and embeddings of topics
    for topic in topics:
        # Generate embedding for the topic
        topic_embedding = embedder(topic)

        # Calculate cosine similarity between chunk embedding and topic embedding
        similarity = cosine_similarity(chunk_embedding, topic_embedding)

        # Update maximum similarity score and related topic if current similarity is higher
        if similarity > max_similarity:
            max_similarity = similarity
            related_topic = topic

    return related_topic