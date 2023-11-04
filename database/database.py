from sqlalchemy import create_engine, Column, ForeignKey, Integer, REAL, String, Date, BigInteger
from sqlalchemy.orm import DeclarativeBase

engine = create_engine(
    "postgresql+psycopg2://okyupals:aH7AaQbo9ywKjB0h_sT2hrPttbmRftjT@raja.db.elephantsql.com/okyupals")


class Base(DeclarativeBase): pass


class Person(Base):
    __tablename__ = "people"

    id = Column(BigInteger, nullable=False, primary_key=True)
    name = Column(String)
    diabetes_type = Column(String)


class Meal_Report(Base):
    __tablename__ = "meal_report"

    id = Column(Integer, primary_key=True, index=True)
    bread_unit = Column(Integer, nullable=False)
    short_insulin = Column(Integer, nullable=True)
    long_insulin = Column(Integer, nullable=True)
    sugar_value_before = Column(REAL, nullable=True)
    sugar_value_after = Column(REAL, nullable=True)
    notes = Column(String, nullable=True)


class Day_Report(Base):
    __tablename__ = "day_report"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("people.id"))
    breakfast_id = Column(Integer, ForeignKey("meal_report.id"))
    lunch_id = Column(Integer, ForeignKey("meal_report.id"))
    dinner_id = Column(Integer, ForeignKey("meal_report.id"))
    date = Column(Date, nullable=False)


Base.metadata.create_all(bind=engine)
