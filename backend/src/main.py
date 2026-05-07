import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pathlib import Path
from dotenv import load_dotenv
from src.database import AsyncSessionLocal, engine, Base
from src.models import User


app = FastAPI(title = "102 Combo API")

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
BOT_API_KEY = os.getenv("BOT_API_KEY", "dev-secret")

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

class RegisterRequest(BaseModel):
    discord_id: str
    discord_name: str
    profile_link: str

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/api/users/register")
async def register_user(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    # Проверка дубликата
    result = await db.execute(select(User).where(User.discord_id == data.discord_id))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Пользователь уже зарегистрирован")

    user = User(
        discord_id=data.discord_id,
        discord_name=data.discord_name,
        profile_link=data.profile_link
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"status": "ok", "user_id": str(user.id)}

@app.get("/api/users/{discord_id}")
async def get_user(discord_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.discord_id == discord_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return {
        "discord_id": user.discord_id,
        "discord_name": user.discord_name,
        "profile_link": user.profile_link,
        "created_at": user.created_at.isoformat()
    }

@app.delete("/api/users/{discord_id}")
async def delete_user(discord_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.discord_id == discord_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    await db.delete(user)
    await db.commit()
    return {"status": "deleted", "discord_id": discord_id}
