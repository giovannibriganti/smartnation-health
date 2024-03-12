from ctransformers import AutoModelForCausalLM


def load(backend: str) -> str:
    match backend:
        case "gpt35turbo":
            return load_gpt35turbo()

        case "mistral":
            return load_mistral()

        case "biomistral":
            return load_biomistral()


def load_gpt35turbo():
    pass


def load_mistral():
    return AutoModelForCausalLM.from_pretrained(
        "TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
        model_file="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
        model_type="mistral",
    )


def load_biomistral():
    return AutoModelForCausalLM.from_pretrained("BioMistral/BioMistral-7B")
