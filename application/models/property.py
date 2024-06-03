from application import db
from application.models.user import User
 
class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    property_type = db.Column(db.String(50), nullable=False)
    selling_type = db.Column(db.String(10), nullable=False)  # 'rent' or 'sell'
    picture_1 = db.Column(db.String(255),nullable=True)
    picture_2 = db.Column(db.String(255),nullable=True)
    picture_3 = db.Column(db.String(255),nullable=True)
    description = db.Column(db.Text, nullable=False)
    no_rooms = db.Column(db.Integer, nullable=False)
    no_washrooms = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    landlord_id = db.Column(db.ForeignKey('user.id'))

    landlord = db.relationship(User,backref='property')