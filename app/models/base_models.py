import datetime as dt

from sqlmodel import Field, SQLModel


class BaseSQLModel(SQLModel):
    pass


class DateCreatedChangedBase(BaseSQLModel):
    created_at: dt.datetime = Field(default=dt.datetime.utcnow(), nullable=False)
    changed_at: dt.datetime = Field(default_factory=dt.datetime.utcnow, nullable=False)
