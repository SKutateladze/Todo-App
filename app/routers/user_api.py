from fastapi import APIRouter, Depends, HTTPException
from app.services.security import get_current_user
from app.services.user import fetch_user
from app.dependencies import get_db_session
from app.schemas.LoginSchema import LoginResponse
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/user", tags=["Users"])

@router.get(
    "/",
    response_model=LoginResponse,
    responses = {
        200: {"description": "Current user's information returned successfully."},
        400: {"description": "Invalid request data."},
        401: {"description": "User is not authenticated."},
        500: {"description": "Internal server error."}
    },
    tags=["Users"],
    response_model_by_alias=True
)
async def get_user(
    db_session: AsyncSession = Depends(get_db_session),
    current_user = Depends(get_current_user)
) -> LoginResponse:
    if not current_user:
        raise HTTPException(status_code=401, detail="User is not authenticated.")
    try:
        user = await fetch_user(db_session, current_user["user_id"])
        if not user:
            raise HTTPException(status_code=401, detail="User is not authenticated")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user information: {str(e)}")