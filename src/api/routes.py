"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt, jwt_required
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/login', methods=['POST'])
def user_login():
    body=request.get_json()
    if body["username"]!="arnaldo": 
        return jsonify({"msg": "No autorizado"}), 401
    if body["password"]!="123":
        return jsonify({"msg": "No autorizado"}), 401
    token = create_access_token(identity="arnaldo", additional_claims={"role":"admin"})
    return jsonify({"token":token}), 200


@api.route("/userinfo", methods=['GET'])
@jwt_required() 
def user_info():
    user=get_jwt_identity()
    payload=get_jwt()
    return jsonify({"user":user,"role":payload["role"]})