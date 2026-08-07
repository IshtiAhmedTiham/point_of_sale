from typing import Optional

from pydantic import BaseModel, Field


class UserFilters(BaseModel):
    name : Optional[str] = Field(None, min_length=1)
    phone : Optional[str] = None
     