from app import db

class Accessiondata(db.Model):
    __tablename__ = 'accessiondata'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    accession = db.Column(db.String(20))
    disease = db.Column(db.String(20))
    tissue = db.Column(db.String(20))
    age = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    gse_alias = db.Column(db.String(20))
    cellnum = db.Column(db.Integer())
    # created = db.Column(db.DateTime, server_default=db.func.now())
    # collection = db.relationship('collection', backref='accessiondata',cascade="all, delete-orphan")

    def __init__(self,accession,disease,tissue,
                age,gender,cellnum,gse_alias):
        self.accession = accession
        self.disease = disease
        self.tissue = tissue
        self.age = age
        self.gender = gender
        self.gse_alias = gse_alias
        self.cellnum = cellnum
        # self.collection = collection
    
    def __repr__(self):
        return f"{self.accession}:{self.gse_alias}"