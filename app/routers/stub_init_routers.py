from fastapi import Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.database import get_session
from services.stub_init_service import StubInitService

router_init_stub = APIRouter()


@router_init_stub.get('/init-stub/', response_model=dict[str, bool], status_code=status.HTTP_200_OK)
async def view_init_stub_view(session: AsyncSession = Depends(get_session)):
    await StubInitService(db_session=session).save_data_to_db()
    return {'ok': True}
