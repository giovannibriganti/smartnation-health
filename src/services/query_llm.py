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
    try:
        response = llm.invoke(prompt)
    except AttributeError:
        response = llm(prompt)
    print(response)
    return response
