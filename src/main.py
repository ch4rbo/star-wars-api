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
from models import db, Usuario, People, Favorito_people, Favorito_planeta, Planeta
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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
def get_allusers():
    usuarios=Usuario.query.all()
    usuarios=list(map(lambda usuario:usuario.serialize(),usuarios)) #Recorre una lista y ejecutva el metodo "serialize" para cada item de la lista (te amo miyagi)
    if not usuarios:
        return jsonify("No se encontraron usuarios"), 404
        
    return jsonify(usuarios), 200

@app.route('/planets', methods=['GET'])
def get_allplanets():
    planetas=Planeta.query.all()
    planetas=list(map(lambda planeta:planeta.serialize(),planetas)) #Recorre una lista y ejecutva el metodo "serialize" para cada item de la lista (te amo miyagi)
    if not planetas:
        return jsonify("No se encontraron planetas"), 404
        
    return jsonify(planetas), 200

@app.route('/planets/<int:id_planeta>', methods=['GET'])
def get_planeta(id_planeta):
    planet=Planeta.query.get(id_planeta)
    if not planet:
        return jsonify("No se encontraron el planeta"), 404
    result=planet.serialize()
    return jsonify(result), 200



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
