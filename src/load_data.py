from rag_chain_executor import execute_rag_for_doc
from data_cleaning_executor import accept_document_return_chunks
from mondodb import load_to_mongodb


def load_data(file_path: str) -> None:
    """
    Endpoint for loading patient data.
    """
    # Create enbeddings and load to vector database
    # patient_id = "patient1"
    patient_id = accept_document_return_chunks(document=file_path)

    # NER
    response = execute_rag_for_doc(
        patient_id=patient_id,
        config_path="./pipeline_meta/prompt_meta.yaml",
    )
    print(response)

    # Load to MongoDB
    load_to_mongodb(response)


if __name__ == "__main__":
    load_data(file_path="./dataset/patient6.txt")
