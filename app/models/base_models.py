import datetime as dt

from sqlmodel import SQLModel, Field


class DateCreatedChangedBase(SQLModel):
    created_at: dt.datetime = Field(default=dt.datetime.utcnow(), nullable=False)
    changed_at: dt.datetime = Field(default_factory=dt.datetime.utcnow, nullable=False)