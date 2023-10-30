from sqlalchemy.orm import Session


class TableRepository:
    entity: object = NotImplementedError
    db: Session = NotImplementedError

    def __init__(self, db: Session, entity: object):
        self.db = db
        self.entity = entity

    def get_by_id(self, id: int):
        return self.db.query(self.entity).filter(self.entity.id == id).first()

    def add(self, entity, created_by_user_id: int = None):
        entity.created_by = created_by_user_id
        self.db.add(entity)
