from flask import Blueprint,request,jsonify
from application.models.maintainance_ticket import MaintainanceTicket
from application.schemas.maintainance_ticket import MaintainanceTicketSchema
from application import db
maintainance_ticket = Blueprint('maintainance_ticket',__name__)

maintainance_ticket_schema = MaintainanceTicketSchema(many=False)
maintainance_tickets_schema = MaintainanceTicketSchema(many=True)


# Create a Maintenance Ticket
@maintainance_ticket.route('/maintenance_tickets', methods=['POST'])
def add_maintenance_ticket():
   
    maintainer_id = request.json['maintainerId']
    detail = request.json['details']
   
    property_id = request.json['propertyId']
    issue = request.json['issue']
    status = request.json['status']
    landlord_id = request.json['landlord_id']
    new_maintenance_ticket = MaintainanceTicket(
        landlord_id=landlord_id,
        maintainer_id=maintainer_id,
        property_id=property_id,
        detail=detail,
        issue=issue,
        status=status
    )

    db.session.add(new_maintenance_ticket)
    db.session.commit()

    return maintainance_ticket_schema.jsonify(new_maintenance_ticket), 201

# Get all Maintenance Tickets
@maintainance_ticket.route('/maintenance_tickets', methods=['GET'])
def get_all_maintenance_tickets():
    landlord_id = request.args.get('landlord_id')
    
    tickets = MaintainanceTicket.query.filter_by(landlord_id=landlord_id).all()
    print("Tickets: ",tickets)
    # Extract ticket details along with property title and maintainer username
    ticket_details = list()
    for ticket in tickets:
      
        ticket_data = {
            'ticket_id': ticket.ticket_id,
            'detail':ticket.detail,
            'maintainer_id':ticket.maintainer_id,
            'property_title': ticket.property.title,
            'issue': ticket.issue,
            'status': ticket.status
        }
        ticket_details.append(ticket_data)
    print(ticket_details)

    return jsonify(ticket_details)



# Get a single Maintenance Ticket by ticket_id
@maintainance_ticket.route('/maintenance_tickets/<ticket_id>', methods=['GET'])
def get_maintenance_ticket(ticket_id):
    maintenance_ticket = MaintenanceTicket.query.get_or_404(ticket_id)
    return maintainance_ticket_schema.jsonify(maintenance_ticket)



# Delete a Maintenance Ticket by ticket_id
@maintainance_ticket.route('/maintenance_tickets/<ticket_id>', methods=['DELETE'])
def delete_maintenance_ticket(ticket_id):
    maintenance_ticket = MaintainanceTicket.query.get_or_404(ticket_id)
    db.session.delete(maintenance_ticket)
    db.session.commit()
    return jsonify({"message": "Maintenance Ticket deleted successfully"}), 200

@maintainance_ticket.route('/complete_ticket', methods=['POST'])
def complete_ticket():
    ticket_id = request.form.get('ticket_id')
    maintainer_id = request.form.get('maintainer_id')
    ticket = MaintainanceTicket.query.filter_by(ticket_id=ticket_id,maintainer_id=maintainer_id).first()
    
    ticket.status = 'completed'
    db.session.commit()
    return jsonify(maintainance_ticket_schema.dump(ticket)), 200