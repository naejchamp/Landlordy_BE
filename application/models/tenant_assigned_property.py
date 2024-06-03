from application import db
from application.models.tenant import Tenant
from application.models.property import Property


class TenantAssignedProperty(db.Model):
  tenant_as_id = db.Column(db.Integer, primary_key=True)
  landlord_id = db.Column(db.ForeignKey('user.id'))
  property_id = db.Column(db.Integer, db.ForeignKey('property.id', ondelete='cascade'), nullable=False)
  tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.tenant_id', ondelete='cascade'), nullable=False)

  # Define relationships (assuming 'user' model exists)
  tenant = db.relationship(Tenant, backref='assignments')
  property = db.relationship(Property, backref='assignments')