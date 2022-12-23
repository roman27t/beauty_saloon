from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import i_config

engine = create_async_engine(i_config.DB_URL, echo=True)
Base = declarative_base()
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# Dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


# from fastapi import HTTPException
# from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import update, delete, select, insert
#
# from typing import AsyncGenerator
#
# from database import async_session
#
#
# async def get_session() -> AsyncGenerator:
#     async with async_session() as session:
#         try:
#             yield session
#             await session.commit()
#         except SQLAlchemyError as sql_ex:
#             await session.rollback()
#             raise sql_ex
#         except HTTPException as http_ex:
#             await session.rollback()
#             raise http_ex
#         finally:
#             await session.close()
#
