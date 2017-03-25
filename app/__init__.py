from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app.models import BikeShop


@app.route('/bikeShops', methods=['GET'])
def get_bikeShops():
    return jsonify(json_list=[bs.serialize for bs in BikeShop.query.all()])

@app.route('/bikeShops/<int:bikeShopId>', methods=['GET'])
def get_bikeShop(bikeShopId):
    bikeShop = BikeShop.query.get(bikeShopId)
    print(bikeShop)
    return jsonify({'bikeShop': bikeShop.serialize})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/bikeShops', methods=['POST'])
def create_bikeShop():
    if not request.json or not all(field in request.json for field in ['name', 'latitude', 'longitude']):
        abort(400)

    bikeShop = BikeShop(
        name=request.json.get('name'), address=request.json.get('address',''),
        postcode=request.json.get('postcode',''),website=request.json.get('website',''),
        phone=request.json.get('phone',''),latitude=request.json.get('latitude'),
        longitude=request.json.get('longitude'))

    db.session.add(bikeShop)
    db.session.commit()
    return jsonify({'bikeShop': bikeShop.serialize}), 201

@app.route('/bikeShops/<int:bikeShopId>', methods=['PUT'])
def update_bikeShop(bikeShopId):
    bikeShop = BikeShop.query.get(bikeShopId)
    bikeShop.name = request.json.get('name', bikeShop.name)
    bikeShop.latitude = request.json.get('latitude', bikeShop.latitude)
    bikeShop.longitude = request.json.get('longitude', bikeShop.longitude)
    bikeShop.address = request.json.get('address', bikeShop.address)
    bikeShop.phone = request.json.get('phone', bikeShop.phone)
    bikeShop.website = request.json.get('website', bikeShop.website)
    db.session.commit()
    return jsonify({'bikeShop': bikeShop.serialize})

@app.route('/bikeShops/<int:bikeShopId>', methods=['DELETE'])
def delete_bikeShop(bikeShopId):
    bikeShop = BikeShop.query.get(bikeShopId)
    db.session.delete(bikeShop)
    db.session.commit()
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)




