from pydantic import BaseModel
from typing import Optional


class Product(BaseModel):
    id: int
    title: str
    images: list[str]
    price: Optional[float] = 0.0
