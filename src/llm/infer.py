from langchain_core.messages import HumanMessage, SystemMessage


def infer(model, backend: str, prompt: str) -> str:
    match backend:
        case "gpt35turbo":
            return infer_gpt35turbo(model=model, prompt=prompt)

        case "mistral":
            return infer_mistral(model=model, prompt=prompt)

        case "biomistral":
            return infer_mistral(model=model, prompt=prompt)


def infer_gpt35turbo(model, prompt: str) -> str:
    prompt = HumanMessage(content=prompt)
    return model([prompt])


def infer_mistral(model, prompt: str) -> str:
    return model(prompt)


def infer_biomistral(model, prompt: str) -> str:
    return model(prompt)
