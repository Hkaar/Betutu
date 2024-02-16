from string import punctuation

from pydantic import BaseModel, validator

class UserSchema(BaseModel):
    id: int
    name: str
    password: str

class RegisterSchema(BaseModel):
    name: str
    password: str

    @validator("password")
    @classmethod
    def check_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be 8 characters or longer!")
        
        if not any(c.isupper() for c in value):
            raise ValueError("Password must contain a uppercase character!")
        
        if not any(c.islower() for c in value):
            raise ValueError("Password must contain a lowercase character!")
        
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain a digit!")
        
        if not any(c in punctuation for c in value):
            raise ValueError("Password must contain a special character!")
        
        return value
    