from pydantic import BaseModel as PydanticBaseModel


class BasePydanticSchema(PydanticBaseModel):
    class Config:
        orm_mode = True
        anystr_strip_whitespace = True
        validate_assignment = True
        validate_all = True


class PaginationSchema(BasePydanticSchema):
    page: int
    page_size: int
    max_rows: int
    max_page: int