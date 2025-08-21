from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.SignupSchema import SignUpRequest
from app.dependencies import get_db_session
from app.services.signup import sign_up_user
from app.schemas.LoginSchema import Token
from app.services.security import authenticate_user, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post(
    "/create-account",
    responses={
        200: {"description": "User account created successfully."},
        400: {"description": "Invalid request data."},
        500: {"description": "Internal server error."}
    },
    tags=["Authentication"],
    response_model_by_alias=True
)
async def create_user(
    db_session: AsyncSession = Depends(get_db_session),
    request: SignUpRequest = Body(..., description="Create user account")
):
    
    try:
        await sign_up_user(request, db_session)
        return {"message": "User was created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create User: {str(e)}")

@router.post("/login", response_model=Token)
async def login_account(
    db_session: AsyncSession = Depends(get_db_session),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    user = await authenticate_user(db_session, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": str(user["user_id"]), "email": user["email"]}
    )

    return Token(access_token=access_token, token_type="bearer")