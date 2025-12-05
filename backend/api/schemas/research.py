
from pydantic import BaseModel

class ResearchRequest(BaseModel):
    title: str
    text: str
