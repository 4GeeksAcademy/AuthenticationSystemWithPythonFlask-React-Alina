"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from api.models import db, Users, Characters, Planets, Vehicles, Fav_characters, Fav_planets, Fav_vehicles
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

#app = Flask(__name__)

api = Blueprint('api', __name__)
CORS(api)


@api.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    # Aquí deberías validar contra tu base de datos
    users_query = Users.query.filter_by(email=email).first()
    if not users_query:
        return jsonify({"msg": "Noexiste"}), 402
    if password != users_query.password:
        return jsonify({"msg": "Bad username or password"}), 401
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200

@api.route('/register', methods=['POST'])
def register():
    request_body = request.get_json()

    if Users.query.filter_by(email=request_body["email"]).first():
        return jsonify({"msg": "Email already exists"}), 409
   
    user = Users()
    user.new_user(
        email=request_body["email"],    
        password=request_body["password"],
        name = request_body["name"],
        is_active = True
    )

    access_token = create_access_token(identity=request_body["email"])
    return jsonify(access_token=access_token), 200

@api.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user()), 200

@api.route('/users', methods = ['GET'])
@jwt_required()
def get_users(): 
    users = Users.query.all()
    users_serialized = list(map(lambda item:item.serialize(), users))
    response_body = {
        "message" : "Nice!",
        "data": users_serialized
    }
    if not(users):
        return jsonify({"msg: Users doesn't exist"})
    return jsonify(response_body), 200

@api.route('/characters', methods = ['GET'])
@jwt_required()
def get_characters(): 
    characters = Characters.query.all()
    characters_serialized = list(map(lambda item:item.serialize(), characters))
    response_body = {
        "message" : "Nice!",
        "data": characters_serialized
    }
    if not(characters):
        return jsonify({"msg: Characters doesn't exist"})
    return jsonify(response_body), 200


@api.route('/planets', methods = ['GET'])
@jwt_required()
def get_planets(): 
    planets = Planets.query.all()
    planets_serialized = list(map(lambda item:item.serialize(), planets))
    response_body = {
        "message" : "Nice!",
        "data": planets_serialized
    }
    if not(planets):
        return jsonify({"msg: Planets doesn't exist"})
    return jsonify(response_body), 200

@api.route('/vehicles', methods = ['GET'])
@jwt_required()
def get_vehicles(): 
    vehicles = Vehicles.query.all()
    vehicles_serialized = list(map(lambda item:item.serialize(), vehicles))
    response_body = {
        "message" : "Nice!",
        "data": vehicles_serialized
    }
    if not(vehicles):
        return jsonify({"msg: Vehicles doesn't exist"})
    return jsonify(response_body), 200

@api.route('/fav_vehicles', methods = ['GET'])
@jwt_required()
def get_fav_vechicles(): 
    fav_vechicles = Fav_vehicles.query.all()
    fav_vechicles_serialized = list(map(lambda item:item.serialize(), fav_vechicles))
    response_body = {
        "message" : "Nice!",
        "data": fav_vechicles_serialized
    }
    if not(fav_vechicles):
        return jsonify({"msg: You don't have any favorite Vechicle"})
    return jsonify(response_body), 200

@api.route('/fav_characters', methods = ['GET'])
@jwt_required()
def get_fav_characters(): 
    fav_characters = Fav_characters.query.all()
    fav_characters_serialized = list(map(lambda item:item.serialize(), fav_characters))
    response_body = {
        "message" : "Nice!",
        "data": fav_characters_serialized
    }
    if not(fav_characters):
        return jsonify({"msg: You don't have any favorite character"})
    return jsonify(response_body), 200

@api.route('/fav_planets', methods = ['GET'])
@jwt_required()
def get_fav_planets(): 
    fav_planets = Fav_planets.query.all()
    fav_planets_serialized = list(map(lambda item:item.serialize(), fav_planets))
    response_body = {
        "message" : "Nice!",
        "data": fav_planets_serialized
    }
    if not(fav_planets):
        return jsonify({"msg: You don't have any favorite planet"})
    return jsonify(response_body), 200

@api.route('/users/<int:user_id>', methods = ['GET'])
@jwt_required()
def get_user(user_id): 
    user = Users.filter_by(id=user_id).first()
    user_serialized = user.serialize()
    response_body = {
        "message" : "Nice!",
        "data": user_serialized
    }
    if not(user):
        return jsonify({"msg: User doesn't exist"})
    return jsonify(response_body), 200

@api.route('/characters/<int:character_id>', methods = ['GET'])
@jwt_required()
def get_character(character_id): 
    character = Users.filter_by(id=character_id).first()
    character_serialized = character.serialize()
    response_body = {
        "message" : "Nice!",
        "data": character_serialized
    }
    if not(character):
        return jsonify({"msg: Character doesn't exist"})
    return jsonify(response_body), 200

@api.route('/planets/<int:planet_id>', methods = ['GET'])
@jwt_required()
def get_planet(planet_id): 
    planet = Users.filter_by(id=planet_id).first()
    planet_serialized = planet.serialize()
    response_body = {
        "message" : "Nice!",
        "data": planet_serialized
    }
    if not(planet):
        return jsonify({"msg: Planet doesn't exist"})
    return jsonify(response_body), 200

@api.route('/vehicles/<int:vehicle_id>', methods = ['GET'])
@jwt_required()
def get_vehicle(vehicle_id): 
    vehicle = Users.filter_by(id=vehicle_id).first()
    vehicle_serialized = vehicle.serialize()
    response_body = {
        "message" : "Nice!",
        "data": vehicle_serialized
    }
    if not(vehicle):
        return jsonify({"msg: Vehicle doesn't exist"})
    return jsonify(response_body), 200

@api.route('/fav_planets/<int:planet_id>', methods=['POST'])
@jwt_required()
def add_fav_planet(planet_id):
    body = request.json
    me = Fav_planets(planets_relation=body["planets_relation"], user_relation=body["user_relation"])
    db.session.add(me)
    db.session.commit()
    response_body = {
        "msg": "Ok",
        "id": planet_id
    }
    return jsonify(response_body), 200

@api.route('/fav_characters/<int:character_id>', methods=['POST'])
@jwt_required()
def add_fav_character(character_id):
    body = request.json
    me = Fav_characters(characters_relation=body["characters_relation"], user_relation=body["user_relation"])
    db.session.add(me)
    db.session.commit()
    response_body = {
        "msg": "Ok",
        "id": character_id
    }
    return jsonify(response_body), 200

@api.route('/planets/<int:planet_id>', methods=['DELETE'])
@jwt_required()
def delete_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet:
        Fav_planets.query.filter_by(planets_relation=planet_id).delete()
        db.session.delete(planet)
        db.session.commit()
        return jsonify({"msg": "Fav planet deleted"}), 200
    else:
        return jsonify({"msg": "Planet don't exist in fav"}), 401
    

@api.route('/characters/<int:character_id>', methods=['DELETE'])
@jwt_required()
def delete_character(character_id):
    character = Characters.query.get(character_id)
    if character:
        Fav_characters.query.filter_by(characters_relation=character_id).delete()
        db.session.delete(character)
        db.session.commit()
        return jsonify({"msg": "Fav character deleted"}), 200
    else:
        return jsonify({"msg": "Character don't exist in fav"}), 401

