
from pydantic import BaseModel
from typing import List

class Slide(BaseModel):
    heading: str
    content: str

class PPTRequest(BaseModel):
    title: str
    slides: List[Slide]
