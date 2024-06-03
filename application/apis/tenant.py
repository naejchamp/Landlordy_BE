from flask import Blueprint,request,jsonify
from application.models.tenant import Tenant
from application.schemas.tenant import TenantSchema
from application.models.tenant_assigned_property import TenantAssignedProperty
from application import db
from utils import save_file,remove_file
tenant = Blueprint('tenant',__name__)


tenant_schema = TenantSchema(many=False)
tenants_schema = TenantSchema(many=True)

# Create a new tenant
@tenant.route('/tenants', methods=['POST'])
def add_tenant():
    name = request.form.get('name')
    phone_no = request.form.get('phone_no')
    landlord_id = request.form.get('landlord_id')
    email = request.form.get('email')
    country = request.form.get('country')
    address = request.form.get('address')
    id_number = request.form.get('id_number')
    document = request.files.get('document')
    saved_document = None
    if document:
        saved_document = save_file(document,'uploads')[1]

    new_tenant = Tenant(name=name, phone_no=phone_no, landlord_id=landlord_id, email=email,document=saved_document, country=country, address=address,id_number=id_number)
    db.session.add(new_tenant)
    db.session.commit()

    tenant = tenant_schema.dump(new_tenant)

    return tenant_schema.jsonify(tenant), 201

# Get all tenants
@tenant.route('/tenants', methods=['GET'])
def get_tenants():
    landlord_id = request.args.get('landlord_id')
    all_tenants = Tenant.query.filter_by(landlord_id=landlord_id).all()
    result = tenants_schema.dump(all_tenants)
    
    return jsonify(result)

# Get a single tenant by id
@tenant.route('/tenants/<int:id>', methods=['GET'])
def get_tenant(id):
    tenant = Tenant.query.get_or_404(id)
    tenant_data = tenant_schema.dump(tenant)
    return jsonify(tenant_data),200


# Delete a tenant by id
@tenant.route('/tenants/<int:id>', methods=['DELETE'])
def delete_tenant(id):

    tenant = Tenant.query.get_or_404(id)
    assignments = TenantAssignedProperty.query.filter_by(tenant_id=id).all()
    for assignment in assignments:
        db.session.delete(assignment)

    db.session.delete(tenant)
    db.session.commit()
    remove_file(tenant.document,'uploads')
    return jsonify({"message": "Tenant deleted successfully"}), 200
