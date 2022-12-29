from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import DuplicatedEntryError
from models.database import get_session
from services.stub_init_service import StubInitService

router_init_stub = APIRouter()


@router_init_stub.get('/init-stub/', response_model=dict[str, bool], status_code=200)
async def init_stub(session: AsyncSession = Depends(get_session)):
    StubInitService(db_session=session).init()
    try:
        await session.commit()
        return {'ok': True}
    except IntegrityError:
        await session.rollback()
        raise DuplicatedEntryError('The employee is already stored')
