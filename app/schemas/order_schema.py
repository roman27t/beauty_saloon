from pydantic import BaseModel as PydanticBaseModel

from models.choices import StatusOrder


class OrderOptionalSchema(PydanticBaseModel):
    status: StatusOrder
