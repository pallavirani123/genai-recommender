from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    level: str  # beginner / intermediate / advanced
    preferred_topics: List[str]
    learning_style: Optional[str] = "visual"  # visual / text / audio
