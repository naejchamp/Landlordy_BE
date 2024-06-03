from application import ma

class TenantAssignedPropertySchema(ma.Schema):
    class Meta:
       
        fields = ('tenant_as_id', 'property_id', 'tenant_id','name','title')