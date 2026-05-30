from sqlalchemy.orm import Session


class SQLAlchemyRepository:
    """
    Generic repository for SQLAlchemy models
    """

    def __init__(self, session: Session, model):
        self.session = session
        self.model = model

    # ======================
    # CREATE
    # ======================
    def create(self, obj):
        self.session.add(obj)
        self.session.commit()
        return obj

    # ======================
    # GET BY ID
    # ======================
    def get(self, obj_id):
        return self.session.query(self.model).get(obj_id)

    # ======================
    # GET ALL
    # ======================
    def get_all(self):
        return self.session.query(self.model).all()

    # ======================
    # UPDATE
    # ======================
    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if not obj:
            return None

        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        self.session.commit()
        return obj

    # ======================
    # DELETE
    # ======================
    def delete(self, obj_id):
        obj = self.get(obj_id)
        if not obj:
            return False

        self.session.delete(obj)
        self.session.commit()
        return True