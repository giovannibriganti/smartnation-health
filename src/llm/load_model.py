from ctransformers import AutoModelForCausalLM
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import AzureChatOpenAI
import json


def load(backend: str) -> str:
    match backend:
        case "gpt35turbo":
            return load_gpt35turbo()

        case "mistral":
            return load_mistral()

        case "biomistral":
            return load_biomistral()


def load_gpt35turbo():
    with open(".secrets/azure.json") as f:
        secrets = json.loads(f.read())
    return AzureChatOpenAI(
        # openai_api_type=API_TYPE,
        # deployment_name=azure_openai_deployment_name,
        api_version=secrets["version"],
        openai_api_key=secrets["key"],
        azure_endpoint=secrets["endpoint"],
        # temperature=azure_openai_temperature
    )


def load_mistral():
    return AutoModelForCausalLM.from_pretrained(
        "TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
        model_file="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
        model_type="mistral",
    )


def load_biomistral():
    return AutoModelForCausalLM.from_pretrained("BioMistral/BioMistral-7B")
