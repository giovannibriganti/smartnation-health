import yaml
from services.rag_loader import load_llm


def query_llm(
    prompt_template: str,
    context: dict,
    question: str,
    config_path: str,
) -> str:

    # Load the dictionary from the YAML file
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    # Load LLM
    llm = load_llm(config.get("llm"))

    # Create prompt from template, question and context
    prompt = prompt_template.format(context=str(context), question=question)

    # LLM Text Generation
    llm_type = config.get("llm").get("type")

    if llm_type == "OpenAI":
        response = llm.invoke(prompt)
    elif llm_type == "AzureOpenAI":
        response = llm.invoke(prompt).content
    elif llm_type == "Mistral7B":
        response = llm(prompt)
    else:
        raise NotImplementedError(f"LLM type not implemented. {llm_type=}")

    return response
