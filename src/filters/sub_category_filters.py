from typing import Optional

from pydantic import (
    BaseModel, 
    Field
)


class SubCategoryFilter(BaseModel):
    name : Optional[str] = Field(None, min_length=1)
    code : Optional[str] = Field(None, min_length=1)