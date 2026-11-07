from typing import Optional

from pydantic import (
    BaseModel, 
    Field
)


class SubCategoryFilter(BaseModel):
    id : Optional[int] = None
    name : Optional[str] = Field(None, min_length=1)
    code : Optional[str] = Field(None, min_length=1)