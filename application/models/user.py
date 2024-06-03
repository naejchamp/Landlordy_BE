from application import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=True)
    role = db.Column(db.String(20), nullable=False)

    #maintainter columns
    phone_no = db.Column(db.String(200), nullable=True,default='None')
    service = db.Column(db.String(200), nullable=True,default='None')

