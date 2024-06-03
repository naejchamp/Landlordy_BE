from application import ma

class ExpenseSchema(ma.Schema):
    class Meta:
        
        fields = ('expense_id', 'expense', 'property_id', 'month_name', 'year', 'landlord_id')
