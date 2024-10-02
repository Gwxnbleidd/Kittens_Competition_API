from pydantic import BaseModel


class KittenModel(BaseModel):

    id: int | None = None
    name: str 
    color: str 
    age: int 
    breed: str 
    description: str 

class UpdateKittenModel(BaseModel):

    name: str | None = None
    color: str | None = None
    age: int | None = None
    breed: str | None = None
    description: str | None = None
