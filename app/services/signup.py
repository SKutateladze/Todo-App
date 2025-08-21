from app.schemas.SignupSchema import SignUpRequest
from sqlalchemy import text, bindparam, String
from app.services.security import hash_password


async def sign_up_user(request: SignUpRequest, db_session):
    query = text("""
        INSERT INTO users (first_name, last_name, email, password, username) 
        VALUES(:first_name, :last_name, :email, :password, :username)
    """).bindparams(
        bindparam("first_name", type_=String),
        bindparam("last_name", type_=String),
        bindparam("email", type_=String),
        bindparam("password", type_=String),
        bindparam("username", type_=String),
    )
    hashed_password = hash_password(request.password)
    params = {
        "first_name": request.first_name,
        "last_name": request.last_name,
        "email": request.email,
        "password": hashed_password,
        "username": request.username
    }

    await db_session.execute(query, params)
    await db_session.commit()

    