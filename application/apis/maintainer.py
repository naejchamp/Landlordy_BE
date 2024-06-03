from flask import Blueprint,request,jsonify
from application.models.user import User
from application.schemas.user import UserSchema
from application.models.maintainance_ticket import MaintainanceTicket
from application.schemas.maintainance_ticket import MaintainanceTicketSchema
from werkzeug.security import generate_password_hash, check_password_hash

from application import db
maintainer = Blueprint('maintainer',__name__)

user_schema = UserSchema(many=False)
users_schema = UserSchema(many=True)

tickets_schema = MaintainanceTicketSchema(many=True)

# Create a User (Maintainer)
@maintainer.route('/maintainers', methods=['POST'])
def add_maintainer():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    role = 'maintainer'  # Assuming role for maintainers

    # Extracting maintainer-specific fields
    phone_no = request.form.get('phone_no')
    service = request.form.get('service')

    new_maintainer = User(
        username=username,
        email=email,
        password=generate_password_hash(password),
        role=role,
        phone_no=phone_no,
        service=service
    )
    db.session.add(new_maintainer)
    db.session.commit()

    return jsonify(user_schema.dump(new_maintainer)), 201

# Get all Maintainers
@maintainer.route('/maintainers', methods=['GET'])
def get_maintainers():
    maintainers = User.query.filter_by(role='maintainer').all()
    result = users_schema.dump(maintainers)
    return jsonify(result)

# Get a single Maintainer by id
@maintainer.route('/maintainers/<int:id>', methods=['GET'])
def get_maintainer(id):
    maintainer = User.query.filter_by(id=id, role='maintainer').first_or_404()

    return jsonify(user_schema(maintainer))



# Delete a Maintainer by id
@maintainer.route('/maintainers/<int:id>', methods=['DELETE'])
def delete_maintainer(id):
    maintainer = User.query.filter_by(id=id, role='maintainer').first_or_404()
    maintainance_tickets = MaintainanceTicket.query.filter_by(maintainer_id=id).all()
    for ticket in maintainance_tickets:
        db.session.delete(ticket)

    db.session.delete(maintainer)
    db.session.commit()
    return jsonify({"message": "Maintainer deleted successfully"}), 200



@maintainer.route('/get_tickets')
def get_tickets():
    maintainer_id = request.args.get('maintainer_id')
    tickets = MaintainanceTicket.query.filter_by(maintainer_id=maintainer_id).all()
    data = list()
    for ticket in tickets:
        single_ticket = {
        "ticket_id": ticket.ticket_id,
        "detail": ticket.detail,
        "property_id": ticket.property_id,
        "property_title": ticket.property.title,
        "issue": ticket.issue,
        "status": ticket.status,
        }
        data.append(single_ticket)
    
    return jsonify(data)



