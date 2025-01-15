from pydantic import BaseModel

class Inputs(BaseModel):
    objetivo_copy: str
    tom_de_voz: str
    publico_alvo: str
    segmento_loja: str
    
class ReviewInputs(BaseModel):
    mensagem: str
    feedback: str

class emailInputs(BaseModel):
    objetivo_copy: str
    tom_de_voz: str
    publico_alvo: str
    segmento_loja: str
    template: str

class linkedinInputs(BaseModel):
    topic: str