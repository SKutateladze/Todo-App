from pydantic import BaseModel, Field

class SignUpRequest(BaseModel):
    first_name: str = Field(..., description="Provide your first name")
    last_name: str = Field(..., description="Provide your last name")
    email: str = Field(..., description="Provide your email")
    password: str = Field(..., description="Create your password")
    username: str = Field(..., description="Create your username")
