from sqlalchemy import bindparam, Integer, text
from app.schemas.LoginSchema import LoginResponse
from fastapi import HTTPException
async def fetch_user(db_session, user_id: int) -> LoginResponse:
    query = text("""
        SELECT 
            user_id,
            first_name,
            last_name,
            email,
            username
        FROM users
        WHERE user_id = :user_id
    """).bindparams(bindparam("user_id", type_=Integer))

    params = {"user_id": user_id}

    result = await db_session.execute(query, params)
    row = result.mappings().first()

    if row is None:
        raise HTTPException(status=404, detail="No user is not logged in")
    
    return LoginResponse(
        user_id=user_id,
        first_name=row["first_name"],
        last_name=row["last_name"],
        email=row["email"],
        username=row["username"]
    )