import yaml
import json
from services.rag_chain_client_snomed import Snomed_Simple_RAG
from services.rag_loader import load_llm
from patient_model import Patient


def identify_snomed_ct(free_text_diagnostic: str, config_path: str) -> str:
    """
    Function that allows to standardize free_text_diagnostic using SNOMED-CT.
    """
    with open(config_path, "r") as file:
        # Load the dictionary from the YAML file
        config = yaml.safe_load(file)

        # First load the 'llm' that you want to use, based in the documentation
        llm = load_llm(config.get("llm"))

        # Load the rag config for the application:
        simple_rag = Snomed_Simple_RAG(
            patient_id=None,
            llm=llm,
            config=config,
            top_k_context=20,
        )

        # Get prompt template
        with open(config.get("snomed_prompts").get("path_query_llm"), "r") as f:
            prompt_template_llm = f.read()
        print("Prompt template---->", prompt_template_llm)

        # Find most likely SNOMED using LLM
        return simple_rag.invoke_rag(
            prompt_context=free_text_diagnostic,
            prompt_template_llm=prompt_template_llm,
            free_text_diagnostic=free_text_diagnostic,
        )
