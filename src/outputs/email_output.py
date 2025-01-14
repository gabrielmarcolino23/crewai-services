from pydantic import BaseModel

class EmailOutput(BaseModel):
    assunto: str
    corpo: str
