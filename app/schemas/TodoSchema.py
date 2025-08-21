from pydantic import BaseModel, Field

class TodoResponse(BaseModel):
    todo_id: int = Field(..., description="Unique identifier of todo")
    title: str = Field(..., description="Title of the todo")
    description: str = Field(..., description="Description of the todo")
    priority: int = Field(..., description="Priority of the todo (scale 1-5)")
    complete: bool = Field(default=False, description="Whether todo is complete or not(True/False)") 

class TodoRequest(BaseModel):
    title: str = Field(..., description="Set the title for todo")
    description: str = Field(..., description="Describe the todo")
    priority: int = Field(..., description="Set the priority of the todo scale(1-5)")
    complete: bool = Field(default=False, description="Set if the todo is complete or not")
