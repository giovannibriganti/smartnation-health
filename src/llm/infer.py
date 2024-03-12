from openai import OpenAI


def infer(model, backend: str, prompt: str) -> str:
    match backend:
        case "gpt35turbo":
            return infer_gpt35turbo(model=model, prompt=prompt)

        case "mistral":
            return infer_mistral(model=model, prompt=prompt)

        case "biomistral":
            return infer_mistral(model=model, prompt=prompt)


def infer_gpt35turbo(model, prompt: str) -> str:
    return model.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            # {"role": "user", "content": "Hello!"},
        ],
    )


def infer_mistral(model, prompt: str) -> str:
    return model(prompt)


def infer_biomistral(model, prompt: str) -> str:
    return model(prompt)
