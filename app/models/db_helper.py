from sqlalchemy.exc import IntegrityError, InternalError
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import DuplicatedEntryError


async def db_commit(db_session: AsyncSession, message: str = 'obj is already stored'):
    try:
        await db_session.commit()
        return {'ok': True}
    except IntegrityError:
        await db_session.rollback()
        raise DuplicatedEntryError(message)
    # except Exception as e:
    #     breakpoint()
    #     pass
