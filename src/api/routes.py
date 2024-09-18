"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from flask_jwt_extended import get_jwt, create_access_token, get_jwt_identity, jwt_required, JWTManager
from flask_bcrypt import Bcrypt
from api.models import db, User, TokenBlockedList
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

app = Flask(__name__)
bcrypt = Bcrypt(app)
api = Blueprint('api', __name__)


# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/signup', methods=['POST'])
def user_signup():
    body = request.get_json()

    if "email" not in body:
        return jsonify({"msg" : "email is required"}), 400
    if "password" not in body:
        return jsonify({"msg" : "password is required"}), 400
    
    encrypted_password = bcrypt.generate_password_hash(body["password"]).decode('utf-8')

    new_user = User(email=body["email"], password=encrypted_password, is_active=True)

    if "firs_name" in body:
        new_user.firs_name = body["firs_name"]
    else: 
        new_user.firs_name = ""
    if "last_name" in body:
        new_user.last_name = body["last_name"]
    else: 
        new_user.last_name = ""

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "ok"}),200
    


@api.route('/login', methods=['POST'])
def user_login():
    body = request.get_json() 
    if "email" not in body:
        return jsonify({"msg" : "email is required"}), 400
    if "password" not in body:
        return jsonify({"msg" : "password is required"}), 400
    
    user = User.query.filter_by(email=body["email"]).first()
    if user is None:
        return jsonify({"msg" : "User not found"}), 404
    
    password_checked = bcrypt.check_password_hash(
        user.password, body["password"])

    if password_checked == False:
        return jsonify({"msg":"Invalid password"})
    

    token = create_access_token(
        identity=user.id, additional_claims={"role": "user"}
    )

    return jsonify({"token" : token}), 200


 
@api.route('/private', methods=['GET'])
@jwt_required()
def user_private():
    user = get_jwt_identity()
    payload = get_jwt()
    return jsonify({"user":user, "role":payload["role"]})


@api.route('/logout', methods=['POST'])
@jwt_required()
def user_logout():
    jti = get_jwt()["jti"]
    token_blocked=TokenBlockedList(jti=jti)

    db.session.add(token_blocked)
    db.session.commit()

    return jsonify({"msg": "Logout Succes"})