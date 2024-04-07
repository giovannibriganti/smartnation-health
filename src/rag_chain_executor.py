import json
import yaml

from services.rag_chain_client import Simple_RAG
from services.rag_loader import load_llm
from patient_model import Patient


def execute_rag_for_doc(patient_id: str, config_path: str) -> Patient:
    """
    Executes RAG for a patient document based on the provided configuration.

    Args:
        patient_id (str): The ID of the patient.
        config_path (str): The path to the YAML configuration file.

    Returns:
        Patient: The patient object containing the extracted data.
    """
    with open(config_path, "r") as file:
        # Load the dictionary from the YAML file
        config = yaml.safe_load(file)

        # First load the 'llm' that you want to use, based on the documentation
        llm = load_llm(config.get("llm"))

        # Load the rag config for the application:
        simple_rag = Simple_RAG(
            patient_id=patient_id,
            llm=llm,
            config=config,
        )

        # Applications steps:
        execution_config = config.get("ner_prompts")

        # Iterate through the queries
        patient_data_dict = {}
        for key, value in execution_config.items():
            with open(value.get("path_retrieve_context"), "r") as f:
                prompt_context = f.read()
            with open(value.get("path_query_llm"), "r") as f:
                prompt_template_llm = f.read()
            response = simple_rag.invoke_rag(prompt_context, prompt_template_llm)
            formatted_response = format_llm_response(key, response)
            patient_data_dict[key] = formatted_response

        return Patient(patient_id=patient_id, **patient_data_dict)


def format_llm_response(field: str, response: str):
    """
    Parses and formats the LLM response based on the field.

    Args:
        field (str): The field for which the response is being formatted.
        response (str): The response string from LLM.

    Returns:
        Union[list, str, None]: The formatted response.
    """
    if response is None:
        return None

    response = response.strip()
    if field in ["allergies", "diagnoses"]:
        try:
            formatted_response = json.loads(response)
            if not isinstance(formatted_response, list):
                formatted_response = list(formatted_response)
            return formatted_response
        except Exception:
            return list()

    elif response == "None":
        return None

    return response
    
