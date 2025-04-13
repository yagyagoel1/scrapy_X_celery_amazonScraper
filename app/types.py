from pydantic  import BaseModel




class dataBody(BaseModel):
    item: str = "pendrive"
    noOfPages: int =  1