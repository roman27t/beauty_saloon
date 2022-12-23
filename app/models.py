# from sqlalchemy import Column, String, Integer
from sqlmodel import Field, SQLModel

# from database import Base


# class CityModel(Base):
#     __tablename__ = "city"
#
#     id = Column(Integer, autoincrement=True, primary_key=True, index=True)
#     name = Column(String, unique=True)
#     population = Column(Integer)


class CitySchema(SQLModel):
    name: str
    population: int


class CityModel(CitySchema, table=True):
    id: int = Field(default=None, primary_key=True)
    # __table_args__ = (
    #     Index(
    #         "compound_index_origin_name_version_destination_name", "origin_name", "origin_version", "destination_name"
    #     ),
    # )
