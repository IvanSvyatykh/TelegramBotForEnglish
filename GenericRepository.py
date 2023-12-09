import calendar

from sqlalchemy.orm import Session
from datetime import date
from datetime import datetime


class TableRepository:
    entity: object = NotImplementedError
    db: Session = NotImplementedError

    def __init__(self, db: Session, entity: object):
        self.db = db
        self.entity = entity

    def get_by_id(self, id: int):
        return self.db.query(self.entity).filter(self.entity.id == id).first()

    def get_by_date_and_id(self, date: datetime, id: int):
        return self.db.query(self.entity).filter(self.entity.date == date, self.entity.person_id == id).first()

    def all_reports_by_year_and_month(self, year: int, month: int, id: int):
        num_days = calendar.monthrange(year, month)[1]
        start_date = date(year, month, 1)
        end_date = date(year, month, num_days)
        return self.db.query(self.entity.breakfast, self.entity.lunch, self.entity.dinner, self.entity.date).filter(
            self.entity.date >= start_date, self.entity.date <= end_date, self.entity.person_id == id).all()

    def add(self, entity):
        self.db.add(entity)
        self.db.commit()
