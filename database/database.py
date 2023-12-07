from sqlalchemy import create_engine, Column, ForeignKey, Integer, REAL, String, Date, BigInteger, JSON
from sqlalchemy.orm import DeclarativeBase

engine = create_engine(
    "postgresql+psycopg2://postgres:Metallika2004@localhost:5432/telegramm_bot", client_encoding='utf8')


class Base(DeclarativeBase): pass


class Person(Base):
    __tablename__ = "people"

    id = Column(BigInteger, nullable=False, primary_key=True)
    name = Column(String)
    diabetes_type = Column(String)


class Meal_Report():
    __tablename__ = "meal_report"

    bread_unit = Column(Integer, nullable=False)
    short_insulin = Column(Integer, nullable=True)
    long_insulin = Column(Integer, nullable=True)
    sugar_value_before = Column(REAL, nullable=True)
    sugar_value_after = Column(REAL, nullable=True)
    notes = Column(String, nullable=True)


class Day_Report(Base):
    __tablename__ = "day_report"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(BigInteger, ForeignKey("people.id"))
    breakfast = Column(JSON)
    lunch = Column(JSON)
    dinner = Column(JSON)
    date = Column(Date, nullable=False)


Base.metadata.create_all(bind=engine)
