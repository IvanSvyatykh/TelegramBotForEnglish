from sqlalchemy.orm import Session
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
        return self.db.query(self.entity).filter(self.entity.date == date and self.entity.person_id == id).first()

    def add(self, entity):
        self.db.add(entity)
        self.db.commit()
