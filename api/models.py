from pydantic import BaseModel

class GS1Input(BaseModel):
    gs1_string: str
