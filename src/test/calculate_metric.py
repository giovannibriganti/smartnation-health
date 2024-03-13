from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from collections import Counter
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

embedder = SentenceTransformerEmbeddings(
        model_name="dangvantuan/sentence-camembert-large",
    )

def semantic_similarity(list1, list2, embedder):
    """
    Calculate semantic similarity between two lists of strings using embeddings.
    
    Args:
    - list1: A list of strings.
    - list2: A list of strings.
    - embedder: An instance of SentenceTransformerEmbeddings.

    Returns:
    - A float representing the semantic similarity score between the two lists.
    """
    # Generate embeddings for each string in the lists
    # Assuming embedder.embed_query supports batch processing directly for lists of strings
    embeddings1 = np.array([embedder.embed_query(text) for text in list1])   
    embeddings2 = np.array([embedder.embed_query(text) for text in list2])
    
    # Calculate cosine similarities between each pair of embeddings
    similarity_matrix = cosine_similarity(embeddings1, embeddings2)
    
    # For each item in list1, find the max similarity score with items in list2, and vice versa
    max_similarities_1 = similarity_matrix.max(axis=1)
    max_similarities_2 = similarity_matrix.max(axis=0)
    
    # Calculate the mean of the max similarities as the overall semantic similarity score
    mean_similarity = (np.mean(max_similarities_1) + np.mean(max_similarities_2)) / 2
    
    return mean_similarity


def calculate_overlap_coefficient(list1, list2):
    set1, set2 = set(list1), set(list2)
    intersection_size = len(set1.intersection(set2))
    smaller_set_size = min(len(set1), len(set2))
    return intersection_size / smaller_set_size if smaller_set_size > 0 else 0



def calculate_correctness(gt_json, mistake_json):
    score, penalties, max_score = 0, 0, 0

    for key, value in gt_json.items():
        if isinstance(value, (int, float)):
            max_score += 1
            if key in mistake_json and mistake_json[key] == value:
                score += 1
            elif key not in mistake_json or type(value) != type(mistake_json.get(key, "")) or mistake_json.get(key, 0) <= 0:
                penalties += 1
        elif isinstance(value, list) and value and isinstance(value[0], str):
            max_score += 2  # Adjusting for semantic comparison
            if key in mistake_json and isinstance(mistake_json[key], list):
                if set(value) == set(mistake_json[key]):
                    score += 1
                else:
                    # Apply semantic similarity comparison for each item in the list
                    semantic_score = semantic_similarity(value, mistake_json[key], embedder)
                    score += semantic_score
            else:
                penalties += 1

    correctness_percentage = ((score - penalties) / max_score) if max_score else 0
    return correctness_percentage


calculate_correctness(gt_json, mistake_json)

