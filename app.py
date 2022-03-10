from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import requests
import os


app = Flask(__name__)
file_path = os.path.abspath(os.getcwd())+"/carpark.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config['SECRET_KEY'] = 'randomsecret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

### Class User ###
class User(db.Model):
    __tablename__ = 'user'
    email= db.Column(db.String(64), primary_key=True)
    public_id = db.Column(db.String(64), unique=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    password= db.Column(db.String(64), nullable=False)
    contact_number = db.Column(db.Integer, nullable=True)


    def __init__(self, email, public_id, first_name, last_name, password, contact_number):
        self.email = email
        self.public_id = public_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.contact_number = contact_number

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result
### Class User ###


### Auto-initate SQL DB and table once app.py launched ###
db.create_all()
db.session.commit()
### Auto-initate SQL DB and table once app.py launched ###

### Create a wrapper for token authentication ###
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        #check if there is token in header
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        if not token:
            return jsonify(
                {
                    "message": "There is no token!"
                }
            ), 401
        #verify that token is valid
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])
            user = User.query.filter_by(public_id= data['public_id']).first()
        except:
            return jsonify(
                {
                    "message": "Token is invalid!"
                }
            ), 401

        return f(user, *args, **kwargs)

    return decorated
### Create a wrapper for token authentication ###


### Start of API points for User creation ###
@app.route("/user", methods=['POST'])
def create_user():
    expected = ["email","first_name","last_name","password"]
    data = request.get_json()

    #set default contact number if not inserted
    if "contact_number" not in data.keys():
        data["contact_number"] = None
    
    #Check for missing input
    for key in expected:
        if key not in data.keys():
            return jsonify(
            {
                "message": f"{key} is not found!"
            }
            ), 500

    #Simple email checker
    if '@' not in data["email"]:
        return jsonify(
            {
                "message": f"@ is not found in email!"
            }
            ), 500
    
    #Simple password validator
    if len(data["password"])<8:
        return jsonify(
            {
                "message": f"Password is too short! Please make it 8 characters or more."
            }
            ), 500
    
    try:
        hashed_password = generate_password_hash(data["password"], method="sha256")
        new_user = User(email=data["email"],public_id=str(uuid.uuid4()), first_name=data["first_name"], last_name = data["last_name"],  password=hashed_password, contact_number=data["contact_number"])
        db.session.add(new_user)
        db.session.commit()
        return jsonify(
            {
                "message": f"Congrats {data['first_name']}! Your account has been created."
            }
        ), 200
    except Exception as e:
        return jsonify(
            {
                "message": "Account creation failed."
            }
        ), 500
### End of API points for User creation ###


### Start of API points for User login ###
@app.route("/login")
#login user
def login_user():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response("Could not verify, please try again.", 401, {"WWW-Authenticate": "Basic realm='Login required!'"})
    #Check if user exist in system
    user = User.query.filter_by(email=auth.username).first()
    if not user:
        return make_response("Username/Email does not exist in the system, please try again", 401, {"WWW-Authenticate": "Basic realm='Login required!'"})
    #Check if password matched
    if check_password_hash(user.password, auth.password):
        #Generate JWT token if password matched
        token = jwt.encode({'public_id': user.public_id, 'exp':datetime.datetime.utcnow()+ datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
        return jsonify(
            {
                "token": token,
                "public_id": user.public_id
            }
        ), 200
    return make_response("Password is wrong, please try again.", 401, {"WWW-Authenticate": "Basic realm='Login required!'"})
### End of API points for User login ###


### Start of API points for querying user detail ###
@app.route("/user/<public_id>", methods=['GET'])
@token_required
#query user's detail
def query_user(user,public_id):
    user_data = User.query.filter_by(public_id=public_id).first()
    user_retrieved = user_data.to_dict()
    if user_retrieved:
        return jsonify(
            {
                "message": f"User's details have been retrieved successfully",
                "data": user_retrieved
            }
        ), 200
    return jsonify(
        {
            "message": "There is no user retrieved"
        }
    ), 500
### End of API points for querying user detail ###


### Start of API points for querying carpark availability ###
@app.route("/car", methods=['GET'])
@token_required
#Get Carpark Availability
def get_car(user):
    data = requests.get("https://api.data.gov.sg/v1/transport/carpark-availability")
    if data.status_code!=200:
        return jsonify(
            {
                "message": "Request unsuccessful."
            }
        ), data.status_code
    else:
        return jsonify(
            {
                "data": data.json()
            }
        ), 200
### End of API points for querying carpark availability ###



if __name__ == '__main__':
    app.run(debug=True)