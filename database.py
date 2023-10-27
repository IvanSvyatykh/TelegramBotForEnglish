from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, REAL, DateTime, Date, ForeignKey

engine = create_engine(
    "postgresql+psycopg2://okyupals:aH7AaQbo9ywKjB0h_sT2hrPttbmRftjT@raja.db.elephantsql.com/okyupals")


class Base(DeclarativeBase): pass


class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone_number = Column(String, nullable=False)
    type_of_diabet = Column(Integer)


class Day_Report(Base):
    __tablename__ = "day_report"

    id = Column(Integer, primary_key=True, index=True)

    person_id = Column(Integer, ForeignKey("people.id"))

    breakfast_id = Column(Integer, ForeignKey("meal_report.id"))

    lunch_id = Column(Integer, ForeignKey("meal_report.id"))

    dinner_id = Column(Integer, ForeignKey("meal_report.id"))

    date = Column(Date, nullable=False)


class Meal_Report(Base):
    __tablename__ = "meal_report"

    id = Column(Integer, primary_key=True, index=True)
    bread_unit = Column(Integer, nullable=False)
    notes = Column(String, nullable=True)
    sugar_value_before = Column(REAL, nullable=True)
    sugar_value_after = Column(REAL, nullable=True)
    datetime = Column(DateTime(), nullable=False)


Base.metadata.create_all(bind=engine)
