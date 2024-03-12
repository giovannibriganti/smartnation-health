from infer import infer
from load_model import load

BACKEND = "gpt35turbo"
CONTEXT = "Le patient est monsieur Dupoint"
QUESTION = "Qui est le patient?"

#################################################
# Template
#################################################

# Load prompt template
with open("prompt_template/question_fr.txt", "r") as f:
    prompt_template = f.read()

# Create prompt
prompt = prompt_template.format(context=CONTEXT, question=QUESTION)
# print(prompt)


#################################################
# Load Model
#################################################

# OpenAI
model = load(backend=BACKEND)

#################################################
# Inference
#################################################

answer = infer(model=model, backend=BACKEND, prompt=prompt)

print(answer)
