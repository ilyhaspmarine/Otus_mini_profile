from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from typing import List
from prometheus_fastapi_instrumentator import Instrumentator
from user_db import get_db, AsyncSessionLocal
from user_models import Base, User as UserModel
from user_schema import User as UserSchema, UserCreate, UserUpdate
import random

app = FastAPI(title="Users API", version="1.0.0")

@app.get('/health', summary='HealthCheck EndPoint', tags=['Health Check'])
def healthcheck():
    return {'status': 'OK'}

@app.post("/users", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db=Depends(get_db)):
    db_user = UserModel(
        username = user.username, 
        firstName = user.firstName,
        lastName = user.lastName,  
        email = user.email,
        phone = user.phone )
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")
    return db_user

@app.get("/users/{username}", response_model=UserSchema)
async def read_user(username: str, db=Depends(get_db)):
    result = await db.execute(select(UserModel).filter(UserModel.username == username))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{username}", response_model=UserSchema)
async def update_user(username: str, user_update: UserUpdate, db=Depends(get_db)):
    result = await db.execute(select(UserModel).filter(UserModel.username == username))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.firstName = user_update.firstName
    user.lastName = user_update.lastName
    user.email = user_update.email
    user.phone = user_update.phone
    try:
        await db.commit()
        await db.refresh(user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Values already exist")
    return user

@app.delete("/users/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(username: str, db=Depends(get_db)):
    result = await db.execute(select(UserModel).filter(UserModel.username == username))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    try:
        await db.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Delete failed")
    return

@app.get("/users", response_model=List[UserSchema])
async def list_users(skip: int = 0, limit: int = 10, db=Depends(get_db)):
    result = await db.execute(select(UserModel).offset(skip).limit(limit))
    users = result.scalars().all()
    return users

# Метод для вызова 5xx ошибки 
@app.get("/cause-5xx")
def cause_5xx():
    if random.random() < 0.75:  # 75% вероятность
        raise HTTPException(status_code=502, detail="502 for testing")
    else:
        return {"message": "OK (25% chance)"}

# # Prometheus
# Instrumentator().instrument(app).expose(app, endpoint="/metrics")