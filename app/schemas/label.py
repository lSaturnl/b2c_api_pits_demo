from pydantic import BaseModel
from typing import List, Literal

class LabelRequest(BaseModel):
    tracking_numbers: List[str]
    format: Literal["html", "pdf"]