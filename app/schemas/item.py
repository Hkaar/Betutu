from pydantic import BaseModel

class ItemSchema(BaseModel):
    name: str
    price: float

class ItemOrderSchema(BaseModel):
    name: str
    amount: int