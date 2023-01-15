from pydantic import BaseModel as PydanticBaseModel


class BasePydanticSchema(PydanticBaseModel):
    class Config:
        anystr_strip_whitespace = True
        validate_assignment = True
        validate_all = True
