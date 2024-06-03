from application import db


class Expense(db.Model):
    expense_id = db.Column(db.Integer, primary_key=True)
    expense = db.Column(db.Float, nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    month_name = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    landlord_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)