from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Transaction(BaseModel):
    name: str
    datetime: Optional[str]
    description: str
    price: float