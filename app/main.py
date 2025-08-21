from fastapi import FastAPI
from app.models import TodoModel, UserModel
from app.dependencies import engine
from app.routers import todo_api, auth_api, user_api

app = FastAPI()

@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        # Run create_all for each Base
        await conn.run_sync(TodoModel.Base.metadata.create_all)
        await conn.run_sync(UserModel.Base.metadata.create_all)

# Include your router
app.include_router(todo_api.router)
app.include_router(auth_api.router)
app.include_router(user_api.router)