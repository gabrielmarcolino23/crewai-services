from pydantic import BaseModel
from datetime import datetime

class InputSegment(BaseModel):
    prompt: str  