from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    email: str = Field(..., description="email of the user to successfully login")
    password: str = Field(..., description="password of the user to successfully login")

class Token(BaseModel):
    access_token: str = Field(..., description="access token for authorization")
    token_type: str = Field(..., description="type of the token")

class LoginResponse(BaseModel):
    user_id: int = Field(..., description="Unique ID of the user")
    first_name: str = Field(..., description="First name of the user")
    last_name: str = Field(..., description="Last name of the user")
    email: str = Field(..., description="Email address of the user")
    username: str = Field(..., description="Username of the user")