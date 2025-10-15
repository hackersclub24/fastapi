from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL")
# DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:5432/postgres"
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True, future=True)

sessions = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autoflush=True
)

Base = declarative_base()

async def get_db():
    async with sessions() as s:
        # SESSON OPEN HONE SE PEHLE
        print("OPENING SESSION")
        yield s
        # SESSION BAND HONE SE JUST PEHLE
        print("CLOSE SESSION")