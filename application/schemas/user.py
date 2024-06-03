from application import ma

class UserSchema(ma.Schema):
    class Meta:
       
        fields = ('id', 'username', 'email', 'password', 'role','phone_no','service')
