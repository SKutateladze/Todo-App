from fastapi import APIRouter, Depends, Body, Path, HTTPException
from app.schemas.TodoSchema import TodoResponse, TodoRequest
from app.dependencies import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.services.todo import fetch_todos, post_todo, fetch_todo, change_todo, remove_todo
from app.services.security import get_current_user

router = APIRouter(
    prefix="/todo",
    tags=["Todos"]
)

@router.get(
    "/",
    response_model=List[TodoResponse],
    responses={
        200: {"description": "Todos returned successfully."},
        400: {"description": "Invalid request data."},
        401: {"description": "User is not authorized."},
        500: {"description": "Internal server error."}
    },
    response_model_by_alias=True,
)
async def get_todos(
    db_session: AsyncSession = Depends(get_db_session),
    current_user = Depends(get_current_user)
) -> List[TodoResponse]:

    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")
    try:
        todos = await fetch_todos(db_session, current_user["user_id"])
        return todos or []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch todos: {str(e)}")


@router.post(
    "/",
    status_code=201,
    responses={
        201: {"description": "Todo created successfully."},
        400: {"description": "Invalid request data."},
        401: {"description": "User is not authorized."},
        500: {"description": "Internal server error."}
    },
    response_model_by_alias=True,
)
async def create_todo(
    db_session: AsyncSession = Depends(get_db_session),
    current_user = Depends(get_current_user),
    request: TodoRequest = Body(..., description="Create todo.")
):
    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")
    try:
        await post_todo(db_session, request, current_user["user_id"])
        return {"message": "Todo was created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create Todo: {str(e)}")


@router.get(
    "/{todo_id}",
    response_model=TodoResponse,
    responses={
        200: {"description": "Todo returned successfully."},
        404: {"description": "Todo not found."},
        401: {"description": "User is not authorized."},
        500: {"description": "Internal server error."}
    },
    response_model_by_alias=True,
)
async def get_todo(
    db_session: AsyncSession = Depends(get_db_session),
    current_user = Depends(get_current_user),
    todo_id: int = Path(..., description="Unique ID of the todo to be returned")
) -> TodoResponse:
    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")
    try:
        todo = await fetch_todo(db_session, todo_id, current_user["user_id"])
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found.")
        return todo
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch todo: {str(e)}")


@router.put(
    "/{todo_id}",
    responses={
        200: {"description": "Todo updated successfully."},
        404: {"description": "Todo not found."},
        400: {"description": "Invalid request data."},
        401: {"description": "User is not authorized."},
        500: {"description": "Internal server error."}
    },
    response_model_by_alias=True,
)
async def update_todo(
    db_session: AsyncSession = Depends(get_db_session),
    current_user = Depends(get_current_user),
    todo_id: int = Path(..., description="Unique ID of the todo to be updated"),
    request: TodoRequest = Body(..., description="Update todo.")
):
    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")
    try:
        updated_todo = await change_todo(db_session, todo_id, request, current_user["user_id"])
        if not updated_todo:
            raise HTTPException(status_code=404, detail="Todo not found.")
        return {"message": "Todo updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update todo: {str(e)}")


@router.delete(
    "/{todo_id}",
    responses={
        200: {"description": "Todo deleted successfully."},
        400: {"description": "Invalid request data."},
        404: {"description": "Todo not found."},
        401: {"description": "User is not authorized."},
        500: {"description": "Internal server error."}
    },
    response_model_by_alias=True,
)
async def delete_todo(
    db_session: AsyncSession = Depends(get_db_session),
    current_user = Depends(get_current_user),
    todo_id: int = Path(..., description="Unique ID of the todo to be deleted"),
):
    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")
    try:
        deleted = await remove_todo(db_session, todo_id, current_user["user_id"])
        if not deleted:
            raise HTTPException(status_code=404, detail="Todo not found.")
        return {"message": "Todo deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete todo: {str(e)}")
