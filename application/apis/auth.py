from flask import Blueprint,request,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from application.schemas.user import UserSchema
from application.models.user import User
from application import db
auth = Blueprint('auth',__name__)


@auth.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role', 'landlord')
    print(password)
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"message": "User with this username or email already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password, role=role)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message":"Account created successfully"
        
    }), 201



@auth.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email,role="landlord").first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid email or password"}), 404

    user_schema = UserSchema(many=False)
    
    return jsonify({"message": "Login successful", "user": user_schema.dump(user)}), 200

@auth.route('/maintainer/login', methods=['POST'])
def maintainer_login():
    username = request.form.get('username')
    password = request.form.get('password')
   
    user = User.query.filter_by(username=username,role="maintainer").first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid email or password"}), 404

    user_schema = UserSchema(many=False)
    
    return jsonify({"message": "Login successful", "user": user_schema.dump(user)}), 200




@auth.route('/auth0_login', methods=['POST'])
def auth0_login():
    email = request.form.get('email')
    username = request.form.get('username')
    role = request.form.get('role', 'landlord')

    user = User.query.filter_by(email=email).first()

    if user:
        user_schema = UserSchema(many=False)
        user_info = user_schema.dump(user)
        return jsonify({"message": "logged in successfully","user":user_info}), 200
    else:
        user= User(email=email,username=username,role=role)
        db.session.add(user)
        db.session.commit()
        user_schema = UserSchema(many=False)
        user_info = user_schema.dump(user)
        return jsonify({"message": "logged in successfully","user":user_info}), 200
    

