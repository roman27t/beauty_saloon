from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import DuplicatedEntryException


async def db_commit(db_session: AsyncSession, message: str = 'obj is already stored'):
    try:
        await db_session.commit()
        return {'ok': True}
    except IntegrityError:
        await db_session.rollback()
        raise DuplicatedEntryException(message)
