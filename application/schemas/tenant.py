from application import ma


class TenantSchema(ma.Schema):
    class Meta:
        
        fields = ('tenant_id', 'name', 'phone_no', 'email','address','country','id_number','document')