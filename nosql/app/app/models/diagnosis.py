from pydantic import BaseModel

class Diagnosis(BaseModel):
    """
    Represents a diagnosis.

    Attributes:
        term (str): The term describing the diagnosis.
        id (str): The ID associated with the diagnosis.

    """

    term: str
    id: str
