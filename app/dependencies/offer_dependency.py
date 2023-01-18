from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import OfferLinkModel
from models.database import get_session
from schemas.offer_schema import OfferLinkOptionalSchema
from services.service_service import OfferLinkService


async def valid_patch_id(pk: int, session: AsyncSession = Depends(get_session)) -> OfferLinkModel:
    return await OfferLinkService(db_session=session).get(pk=pk)


async def valid_patch_schema(schema: OfferLinkOptionalSchema) -> OfferLinkOptionalSchema:
    if not schema.dict(exclude_unset=True):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='empty data')
    return schema
