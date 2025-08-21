from typing import List
from app.schemas.TodoSchema import TodoResponse, TodoRequest
from sqlalchemy import text, bindparam, Integer, String, Boolean
from fastapi import HTTPException

async def fetch_todos(db_session, owner_id: int) -> List[TodoResponse]:
    
    query = text("""
        SELECT
            todo_id,
            title,
            description,
            priority,
            complete
        FROM todos
        WHERE owner_id = :owner_id
    """).bindparams(bindparam("owner_id", type_=Integer))

    result = await db_session.execute(query, {"owner_id": owner_id})

    rows = result.mappings().all()  

    return [
        TodoResponse(
            todo_id=row["todo_id"],
            title=row["title"],
            description=row["description"],
            priority=row["priority"],
            complete=row["complete"]
        )
        for row in rows
    ]

async def post_todo(db_session, request: TodoRequest, owner_id: int):
    query = text("""
        INSERT INTO todos (title, description, priority, complete, owner_id)
        VALUES (:title, :description, :priority, :complete, :owner_id)
    """).bindparams(bindparam("owner_id", type_=Integer))

    params = {
        "title": request.title,
        "description": request.description,
        "priority": request.priority,
        "complete": request.complete,
        "owner_id": owner_id
    }
    await db_session.execute(
        query,
        params
    )

    await db_session.commit()


async def fetch_todo(db_session, todo_id: int, owner_id: int) -> TodoResponse:
    query = text("""
        SELECT 
            todo_id,
            title,
            description,
            priority,
            complete
        FROM todos
        WHERE todo_id = :todo_id AND owner_id = :owner_id
    """).bindparams(bindparam("todo_id", type_=Integer), bindparam("owner_id", type_=Integer))

    params = {
        "todo_id": todo_id,
        "owner_id": owner_id
    }

    result = await db_session.execute(
        query,
        params
    )
    row = result.mappings().first()
    if row is None:
        raise HTTPException(status_code=404, detail="Todo not found.")
    
    return TodoResponse(
        todo_id = row["todo_id"],
        title = row["title"],
        description = row["description"],
        priority = row["priority"],
        complete = row["complete"]
    )

async def change_todo(db_session, todo_id: int, request: TodoRequest, owner_id: int):
    query = text("""
        UPDATE todos
        SET title = :title,
            description = :description,
            priority = :priority,
            complete = :complete
        WHERE todo_id = :todo_id AND owner_id = :owner
        RETURNING todo_id, title, description, priority, complete
    """).bindparams(
            bindparam("todo_id", type_=Integer),
            bindparam("title", type_=String),
            bindparam("description", type_=String),
            bindparam("priority", type_=Integer),
            bindparam("complete", type_=Boolean),
            bindparam("owner_id", type_=Integer)
        )

    params = {
        "todo_id": todo_id,
        "title": request.title,
        "description": request.description,
        "priority": request.priority,
        "complete": request.complete,
        "owner_id": owner_id
    }

    result = await db_session.execute(query, params)
    row = result.mappings().first()

    if row is None:  
        raise HTTPException(status_code=404, detail="Todo not found.")

    await db_session.commit()

    return row

async def remove_todo(db_session, todo_id: int, owner_id: int):
    query = text("""
        DELETE FROM todos
        WHERE todo_id = :todo_id AND owner_id = :owner_id
        RETURNING todo_id
    """).bindparams(bindparam("todo_id", type_=Integer), bindparam("owner_id", type_=Integer))

    params = {
        "todo_id": todo_id, 
        "owner_id": owner_id
    }

    result = await db_session.execute(query, params)
    row = result.mappings().first()

    if row is None:
        raise HTTPException(status_code=404, detail="Todo not found.")
    
    await db_session.commit()
    return True