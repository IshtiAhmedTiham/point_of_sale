from pydantic import BaseModel, Field
from typing import Optional

class SubCategoryFilter(BaseModel):
    name : Optional[str] = Field(None, min_length=1)
    code : Optional[str] = Field(None, min_length=1)