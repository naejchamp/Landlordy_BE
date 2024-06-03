from application import db

class Tenant(db.Model):
    tenant_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_no = db.Column(db.String(20), nullable=True)
    id_number = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    document = db.Column(db.String(200), nullable=True)

    address = db.Column(db.String(200), nullable=True)
    landlord_id = db.Column(db.ForeignKey('user.id'))
    email = db.Column(db.String(100), nullable=False)