from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Aaron/Desktop/carpark_availability/carpark.db'
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


    def __init__(self, email, public_id, first_name, last_name, password):
        self.email = email
        self.public_id = public_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password

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


### Start of API points for User ###
@app.route("/user", methods=['POST'])
#create user
def create_user():
    data = request.get_json()
    try:
        hashed_password = generate_password_hash(data["password"], method="sha256")
        new_user = User(email=data["email"],public_id=str(uuid.uuid4()), first_name=data["first_name"], last_name = data["last_name"],  password=hashed_password)
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
            "message": "There are no users retrieved"
        }
    ), 500

@app.route("/login")
#login user
def login_user():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response("Could not verify, please try again.", 401, {"WWW-Authenticate": "Basic realm='Login required!'"})
    #Check if user exist in system
    user = User.query.filter_by(email=auth.username).first()
    if not user:
        return make_response("Username/Email does not exist, please try again", 401, {"WWW-Authenticate": "Basic realm='Login required!'"})
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)