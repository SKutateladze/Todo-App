from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from sqlalchemy import text, bindparam, String
from typing import Optional, Dict
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from app.dependencies import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# --- Password Utils ---
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# --- Token Utils ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> Optional[Dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# --- Authentication ---
async def authenticate_user(db_session, email: str, password: str):
    query = text("""
        SELECT * FROM users WHERE email = :email
    """).bindparams(bindparam("email", type_=String))

    result = await db_session.execute(query, {"email": email})
    user = result.mappings().first()

    if not user or not verify_password(password, user["password"]):
        return None
    
    return user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

async def get_current_user(
    db_session: AsyncSession = Depends(get_db_session),
    token: str = Depends(oauth2_scheme)
):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    query = text("SELECT * FROM users WHERE user_id = :user_id").bindparams(bindparam("user_id"))
    result = await db_session.execute(query, {"user_id": int(user_id)})
    user = result.mappings().first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user