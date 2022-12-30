from typing import Callable

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import DuplicatedEntryError


async def db_commit(db_session: AsyncSession, service_call: Callable):
    service_call()
    try:
        await db_session.commit()
        return {'ok': True}
    except IntegrityError:
        await db_session.rollback()
        raise DuplicatedEntryError('obj is already stored')
