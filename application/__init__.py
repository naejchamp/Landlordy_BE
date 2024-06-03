from flask import Flask,jsonify,request
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import DATABASE_URI,SECRET_KEY
from flask_migrate import Migrate
app  = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ma= Marshmallow(app)
db = SQLAlchemy(app)
Migrate(app,db)
CORS(app)


from application.apis.auth import auth
app.register_blueprint(auth)


from application.apis.tenant import tenant
app.register_blueprint(tenant)


from application.apis.property import _property
app.register_blueprint(_property)

from application.apis.expense import expense
app.register_blueprint(expense)


from application.apis.tenant_assigned_properties import tenant_assigned_properties
app.register_blueprint(tenant_assigned_properties)


from application.apis.maintainer import maintainer
app.register_blueprint(maintainer)


from application.apis.maintainance_ticket import maintainance_ticket
app.register_blueprint(maintainance_ticket)