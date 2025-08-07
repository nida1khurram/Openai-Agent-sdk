from pydantic import BaseModel

class UserData(BaseModel):
    name:str
    age:int
    role:str