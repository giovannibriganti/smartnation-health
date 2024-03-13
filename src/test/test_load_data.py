from rag_chain_executor import execute_rag_for_doc
from data_cleaning_executor import accept_document_return_chunks
from mondodb import load_to_mongodb
from calculate_metric import calculate_correctness
import json


def test_load_data(file_path: str,  gt_path: str) -> None:
    """
    Endpoint for loading patient data.
    """
    # Create enbeddings and load to vector database
    patient_id = accept_document_return_chunks(document=file_path)
    # patient_id = "patient1"

    # NER
    response = execute_rag_for_doc(
        patient_id=patient_id,
        config_path="./pipeline_meta/prompt_meta_testing.yaml",
    )

    # Load ground truth data from JSON
    with open(gt_path, 'r') as gt_file:
        ground_truth_data = json.load(gt_file)
    
    calculate_correctness(response, ground_truth_data)
    
    


if __name__ == "__main__":
    file_path = "./dataset/patient2.txt"
    gt_path = "./dataset/patient1_gt.json"  # Path to the ground truth JSON file
    load_data(file_path, gt_path)
