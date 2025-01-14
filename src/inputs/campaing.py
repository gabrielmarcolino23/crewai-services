from pydantic import BaseModel
from .copy_input import Inputs
from .segment_input import InputSegment

class CampaingInputs(BaseModel):
    tipo_campanha: str
    inputs: Inputs
