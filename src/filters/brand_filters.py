from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class BrandFilters(BaseModel):
    name : Optional[str] = Field(None, min_length=1)
    email : Optional[EmailStr] = None
     