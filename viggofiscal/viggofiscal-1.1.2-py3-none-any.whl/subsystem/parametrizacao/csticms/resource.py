from viggocore.database import db
from viggocore.common.subsystem import entity


class Csticms(entity.Entity, db.Model):

    attributes = ['cstcsosn', 'descricao']
    attributes += entity.Entity.attributes

    cstcsosn = db.Column(db.Numeric(5, 0), nullable=False, unique=True)
    descricao = db.Column(db.String(200), nullable=False)

    def __init__(self, id, cstcsosn, descricao,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.cstcsosn = cstcsosn
        self.descricao = descricao