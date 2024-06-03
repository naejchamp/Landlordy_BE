from flask import Blueprint,request,jsonify
from application.models.expense import Expense
from application.schemas.expense import ExpenseSchema
from application.models.property import Property
from application.schemas.property import PropertySchema
from application import db
expense = Blueprint('expense',__name__)

expense_schema = ExpenseSchema(many=False)
expenses_schema = ExpenseSchema(many=True)

property_schema = PropertySchema(many=False)
properties_schema = PropertySchema(many=True)

# Create an Expense
@expense.route('/expenses', methods=['POST'])
def add_expense():
    expense = float(request.form.get('expense'))
    print("expense:",expense)

    property_id = request.form.get('property_id')
    month_name = request.form.get('month_name')
    print(month_name)
    year = int(request.form.get('year'))
    landlord_id = int(request.form.get('landlord_id'))
    new_expense = Expense(
        expense=expense,
        property_id=property_id,
        month_name=month_name,
        year=year,
        landlord_id=landlord_id
    )
    db.session.add(new_expense)
    db.session.commit()

    return expense_schema.jsonify(new_expense), 201

# Get all Expenses
@expense.route('/expenses', methods=['GET'])
def get_expenses():
    landlord_id = request.args.get('landlord_id')
    all_expenses = Expense.query.filter_by(landlord_id=landlord_id).all()
    data = expenses_schema.dump(all_expenses)
   

    return jsonify(data)

@expense.route('/expenses/filter_by_year', methods=['GET'])
def get_expenses_by_year():
    landlord_id = request.args.get('landlord_id')
    year = request.args.get('year')
    
    if not landlord_id or not year:
        return jsonify({"error": "landlord_id and year are required parameters"}), 400
    
    expenses = Expense.query.filter_by(landlord_id=landlord_id, year=int(year)).all()
    print(expenses)
    result = expenses_schema.dump(expenses)
    return jsonify(result)



# Get a single Expense by id
@expense.route('/expenses/<int:id>', methods=['GET'])
def get_expense(id):
    expense = Expense.query.get_or_404(id)
    return expense_schema.jsonify(expense)





@expense.route('/expenses/properties', methods=['GET'])
def get_properties():
    landlord_id = request.args.get('landlord_id')
    all_properties = Property.query.filter_by(landlord_id=landlord_id).all()
    result = properties_schema.dump(all_properties)
    return jsonify(result)

# Delete an Expense by id
@expense.route('/expenses/<int:id>', methods=['DELETE'])
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return jsonify({"message": "Expense deleted successfully"}), 200

