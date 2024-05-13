import yaml
from ctransformers import AutoModelForCausalLM
from langchain_openai import AzureChatOpenAI, OpenAI
from langchain_community.llms import Ollama
from config import *


def load_config(config_path: str) -> dict:
    """
    Loads a YAML configuration file.

    Args:
        config_path (str): The path to the configuration file.

    Returns:
        dict: The loaded configuration settings.

    """
    with open(config_path, "r") as file:
        return yaml.safe_load(file)


def load_llm(llm_params: dict):
    """
    Loads a language model based on the provided parameters.

    Args:
        llm_params (dict): The parameters for the language model.

    Returns:
        LanguageModel: The loaded language model.

    Raises:
        NotImplementedError: If the language model type is not implemented.

    """
    if llm_params.get("type") == "OpenAI":
        with open(".secrets/openapikey") as f:
            openaikey = f.read()

        return OpenAI(api_key=openaikey)

    elif llm_params.get("type") == "Mistral7B":
        return AutoModelForCausalLM.from_pretrained(
            "TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
            model_file="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
            model_type="mistral",
        )

    elif llm_params.get("type") == "llama3":
        return Ollama(
            model="llama3",
        )

    elif llm_params.get("type") == "AzureOpenAI":
        API_TYPE = "azure"
        with open(".secrets/azureopenapikey") as f:
            openaikey = f.read()
        return AzureChatOpenAI(
            openai_api_type=API_TYPE,
            deployment_name=AZURE_OPENAI_DEPLOYMENT_NAME,
            api_version=AZURE_OPENAI_API_VERSION,
            openai_api_key=openaikey,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            temperature=AZURE_OPENAI_TEMPERATURE,
        )

    else:
        raise NotImplementedError("LLM not implemented")
