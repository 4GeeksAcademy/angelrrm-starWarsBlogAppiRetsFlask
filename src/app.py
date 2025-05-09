"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, FavoritePlanet, FavoritePeople
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_all_people():
    people_list = People.query.all()
    results = list(map(lambda person: person.serialize(), people_list))
    return jsonify(results), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets_list = Planets.query.all()
    results = list(map(lambda planet: planet.serialize(), planets_list))
    return jsonify(results), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_people(people_id):
    person = People.query.get_or_404(people_id)
    return (person.serialize()), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = Planets.query.get_or_404(planet_id)
    return jsonify(planet.serialize()), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
    user = User.query.first()
    new_favorite = FavoritePeople(user_id = user.id, people_id = people_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"message":"Se ha añadido a Favorites"}), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user = User.query.first()  
    new_favorite = FavoritePlanet(user_id=user.id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"message": "Planeta añadido a favoritos"}), 201

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def remove_favorite_people(people_id):
    user = User.query.first() 
    favorite = FavoritePeople.query.filter_by(user_id=user.id, people_id=people_id).first()

    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Personaje eliminado de favoritos"}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    user = User.query.first()
    favorite = FavoritePlanet.query.filter_by(user_id=user.id, planet_id=planet_id).first()

    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Planeta eliminado de favoritos"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
