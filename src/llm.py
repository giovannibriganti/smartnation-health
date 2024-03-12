from openai import OpenAI

ORGANIZATION = ""
CONTEXT = ""
QUESTION = ""

# Create Open-AI object
client = OpenAI(
    organization="YOUR_ORG_ID",
)

# Load prompt template
with open("question_fr.txt", "r") as f:
    prompt_template = f.read()

# Create prompt

prompt = prompt_template.format(context=CONTEXT, question=QUESTION)
print(prompt)

# Inference
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
    ],
)

print(completion.choices[0].message)
