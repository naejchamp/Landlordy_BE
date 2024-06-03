from application import ma

class PropertySchema(ma.Schema):
    class Meta:
       
        fields = ('id', 'title', 'property_type', 'selling_type', 'picture_1', 'picture_2', 'picture_3', 'description', 'no_rooms', 'no_washrooms', 'price')
