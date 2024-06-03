from application import ma

class MaintainanceTicketSchema(ma.Schema):
    class Meta:
       
        fields = ('ticket_id', 'maintainer_id', 'property_id', 'issue', 'status','detail')