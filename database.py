from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import  Column, Integer, String
from sqlalchemy.orm import Session

engine = create_engine("postgresql+psycopg2://okyupals:aH7AaQbo9ywKjB0h_sT2hrPttbmRftjT@raja.db.elephantsql.com/okyupals")

class Base(DeclarativeBase): pass

class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)

Base.metadata.create_all(bind=engine)
