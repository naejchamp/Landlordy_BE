from flask import Blueprint,request,jsonify
from application.models.tenant_assigned_property import TenantAssignedProperty
from application.schemas.tenant_assigned_property import TenantAssignedPropertySchema
from application.models.tenant import Tenant
from application.models.property import Property

from application import db
tenant_assigned_properties = Blueprint('tenant_assigned_properties',__name__)

tenant_assigned_property_schema = TenantAssignedPropertySchema(many=False)
tenant_assigned_properties_schema = TenantAssignedPropertySchema(many=True)


@tenant_assigned_properties.route('/tenant_assigned_properties', methods=['POST'])
def add_tenant_assigned_property():
    property_id = request.form.get('property_id')
    tenant_id = request.form.get('tenant_id')
    landlord_id = request.form.get('landlord_id')
    new_tenant_assigned_property = TenantAssignedProperty(
        property_id=property_id,
        tenant_id=tenant_id,
        landlord_id=landlord_id
    )
    db.session.add(new_tenant_assigned_property)
    db.session.commit()

    return jsonify({
        "message":"assigned property successfully"
    }), 201




@tenant_assigned_properties.route('/tenant_assigned_properties', methods=['GET'])
def get_tenant_assigned_property_by_ids():
    landlord_id = request.args.get('landlord_id')
    tenant_assigned_properties = TenantAssignedProperty.query.filter_by(landlord_id=landlord_id).all()

    data = list()
    for assign in tenant_assigned_properties:
        data.append({
            "tenant_as_id":assign.tenant_as_id,
            "tenant_id":assign.tenant_id,
            "property_id":assign.property_id,
             "property_title":assign.property.title,
             "tenant_name":assign.tenant.name
        })

    print(data)
    return jsonify(data)


@tenant_assigned_properties.route('/tenant_assigned_properties/<int:id>', methods=['DELETE'])
def delete_tenant_assigned_property(id):
    tenant_assigned_property = TenantAssignedProperty.query.get_or_404(id)
    db.session.delete(tenant_assigned_property)
    db.session.commit()
    return jsonify({"message": "Tenant assigned property deleted successfully"}), 200
