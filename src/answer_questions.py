from mondodb import get_from_mongodb
from services.query_llm import query_llm


def answer_question(patient_id: str, question: str) -> str:
    """
    Endpoint for answering doctor's question.
    """
    # Retrieve data from MongoDB
    context = get_from_mongodb(patient_id=patient_id)
    if context is None:
        raise IndexError(f"Patient not found {patient_id=}.")

    # Retrieve prompt template
    with open("./prompt_template/doctor_question_fr.txt", "r") as f:
        prompt_template = f.read()

    # Query LLM with question
    response = query_llm(
        prompt_template=prompt_template,
        context=context,
        question=question,
        config_path="./pipeline_meta/prompt_meta.yaml",
    )
    print(response)
    return response


if __name__ == "__main__":
    answer_question(
        patient_id="patient1",
        question="Quel est sont les allegies du patient?",
    )
