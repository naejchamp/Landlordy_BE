from application import db
from application.models.user import User
from application.models.property import Property
class MaintainanceTicket(db.Model):
    ticket_id = db.Column(db.Integer, primary_key=True)
    maintainer_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id', ondelete='cascade'), nullable=False)
    issue = db.Column(db.String(100), nullable=False)
    landlord_id = db.Column(db.Integer,db.ForeignKey('user.id', ondelete='cascade'))
    status = db.Column(db.String(30),nullable=False,default="pending")
    detail= db.Column(db.String(300),nullable=False)
   
    property = db.relationship(Property, backref='tickets')


    
