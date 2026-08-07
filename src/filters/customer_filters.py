from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class CustomerFilter(BaseModel):
    name : Optional[str] = Field(None, min_length=1)
    email : Optional[EmailStr] = None
    phone : Optional[str] = None
    account_no : Optional[str] = None

    