from flask import Blueprint,request,jsonify
from application.models.property import Property
from application.schemas.property import PropertySchema
from application.models.tenant_assigned_property import TenantAssignedProperty
from application.models.maintainance_ticket import MaintainanceTicket
from utils import save_file,remove_file
from application import db
_property = Blueprint('property',__name__)

property_schema = PropertySchema(many=False)
properties_schema = PropertySchema(many=True)




# Create a new property
@_property.route('/properties', methods=['POST'])
def add_property():
    title = request.form.get('title')
    landlord_id = request.form.get('landlord_id')
    property_type = request.form.get('property_type')
    selling_type = request.form.get('selling_type')
    description = request.form.get('description')
    no_rooms = request.form.get('no_rooms')
    no_washrooms = request.form.get('no_washrooms')
    price = request.form.get('price')
    picture_1 = None
    picture_2 = None
    picture_3 = None

    if request.files.get('picture_1'):
        picture_1 = save_file(request.files.get('picture_1'),'uploads')[1]

    if request.files.get('picture_2'):
        picture_2 = save_file(request.files.get('picture_2'),'uploads')[1]

    if request.files.get('picture_3'):
        picture_3 = save_file(request.files.get('picture_3'),'uploads')[1]


    print(picture_1)
    new_property = Property(
        landlord_id = landlord_id,
        title=title,
        property_type=property_type,
        selling_type=selling_type,
        picture_1=picture_1,
        picture_2=picture_2,
        picture_3=picture_3,
        description=description,
        no_rooms=no_rooms,
        no_washrooms=no_washrooms,
        price=price
    )
    db.session.add(new_property)
    db.session.commit()

    
    return jsonify(property_schema.dump(new_property)), 201

# Get properties
@_property.route('/properties', methods=['GET'])
def get_properties():
    landlord_id = request.args.get('landlord_id')

    all_properties = Property.query.filter_by(landlord_id=landlord_id).all()
    result = properties_schema.dump(all_properties)
    return jsonify(result)

# Get All properties
@_property.route('/get_all_properties', methods=['GET'])
def get_all_properties():
    all_properties = Property.query.all()

    result = properties_schema.dump(all_properties)
  
    return jsonify(result)



# Get a single property by id
@_property.route('/properties/<int:id>', methods=['GET'])
def get_property(id):
    property_data = Property.query.get_or_404(id)
    return jsonify(property_schema.dump(property_data))


# Delete a property by id
@_property.route('/properties/<int:id>', methods=['DELETE'])
def delete_property(id):
    property = Property.query.get_or_404(id)

    assignments = TenantAssignedProperty.query.filter_by(property_id=id).all()
    for assignment in assignments:
        db.session.delete(assignment)

    maintainance_tickets = MaintainanceTicket.query.filter_by(property_id=id).all()
    for ticket in maintainance_tickets:
        db.session.delete(ticket)

    db.session.delete(property)
    db.session.commit()

    if property.picture_1:
        remove_file(property.picture_1,'uploads')
    else:
        pass

    if property.picture_2:
        remove_file(property.picture_2,'uploads')
    else:
        pass

    if property.picture_3:
        remove_file(property.picture_3,'uploads')
    else:
        pass


    return jsonify({"message": "Property deleted successfully"}), 200


@_property.route('/fetch_8_properties', methods=['GET'])
def Fetch4Properties():
    all_properties = Property.query.limit(8)
    result = properties_schema.dump(all_properties)
    return jsonify(result)



@_property.route('/view_property', methods=['GET'])
def view_property():
    property_id = request.args.get('property_id')
    property_data = Property.query.get_or_404(property_id)
    
    data = {
        'id':property_data.id,
        'landlord_id':property_data.landlord_id,
        'landlord_name':property_data.landlord.username,
        'landlord_phone_no':property_data.landlord.phone_no,
        'landlord_email':property_data.landlord.email,

        'picture_1':property_data.picture_1,
        'picture_2':property_data.picture_2,
        'picture_3':property_data.picture_3,
        'title':property_data.title,
        'property_type':property_data.property_type,
        'description':property_data.description,
        'no_rooms':property_data.no_rooms,
        'no_washrooms':property_data.no_washrooms,
        'price':property_data.price,
        'selling_type':property_data.selling_type
    }
    
    return jsonify(data)


@_property.route('/search_properties', methods=['GET'])
def search_properties():
    title = request.args.get('title')
    selling_type = request.args.get('selling_type')
    property_type = request.args.get('property_type')
    query = Property.query
    
    if title:
        query = query.filter(Property.title.ilike(f'%{title}%'))
    
    if selling_type:
        query = query.filter_by(selling_type=selling_type)
    
    if property_type:
        query = query.filter_by(property_type=property_type)
        
    properties = query.all()
    result = properties_schema.dump(properties)
    
    return jsonify(result)