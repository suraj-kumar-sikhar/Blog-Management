from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class BlogBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    author: str = Field(..., min_length=3)
    email: EmailStr
    category: str
    content: str = Field(..., min_length=100)
    imageuri:Optional[str]=None
    published: Optional[datetime] = Field(default_factory=datetime.utcnow)
    approved: bool = False

class BlogResponse(BlogBase):
    id: str
    created_at: Optional[datetime]=None
