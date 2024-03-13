import yaml
from services.rag_chain_client import Simple_RAG
from services.rag_loader import load_llm
from patient_model import Patient
import json


def execute_rag_for_doc(patient_id: str, config_path: str) -> Patient:
    with open(config_path, "r") as file:
        # Load the dictionary from the YAML file
        config = yaml.safe_load(file)

        # First load the 'llm' that you want to use, based in the documentation
        llm = load_llm(config.get("llm"))

        # Load the rag config for the application:
        simple_rag = Simple_RAG(
            patient_id=patient_id,
            llm=llm,
            config=config,
        )

        ## Applications steps:
        execution_config = config.get("ner_prompts")

        # Iterate through the queries
        patient_data_dict = {}
        for key, value in execution_config.items():
            with open(value.get("path_retrieve_context"), "r") as f:
                prompt_context = f.read()
            with open(value.get("path_query_llm"), "r") as f:
                prompt_template_llm = f.read()
            response = simple_rag.invoke_rag(prompt_context, prompt_template_llm)
            formated_response = format_llm_response(key, response)
            patient_data_dict[key] = formated_response

        return Patient(patient_id=patient_id, **patient_data_dict)


def format_llm_response(field: str, response: str):
    """Parses and formats LLM response."""

    if response is None:
        return None

    response = response.strip()
    if field in ["allergies", "diagnoses"]:
        try:
            return json.loads(response)
        except Exception:
            return list()

    elif response == "None":
        return None

    return response
