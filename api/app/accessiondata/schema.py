from sqlite3 import SQLITE_SAVEPOINT
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate, validates, validates_schema, ValidationError,post_load
from app.accessiondata.models import Accessiondata
from app import db

class AccessiondataSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Accessiondata
        sqla_session = db.session
        load_instance = True
        # include_relationships = True

    id = fields.Number(dump_only=True)
    accession = fields.String(required=True)
    disease = fields.String(required=True)
    tissue = fields.String(required=True)
    age = fields.String()
    gender = fields.String()
    gse_alias = fields.String(required=True)
    # collection_id = fields.Integer()
    cellnum = fields.Integer(required=True)
    # created = fields.String(dump_only=True)
    
    @post_load
    def post_load(self,instance,**kwargs):
        db.session.add(instance)
        db.session.commit()
        return instance