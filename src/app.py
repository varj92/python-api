from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS,cross_origin

app = Flask(__name__)
app.config['MONGO_URI']='mongodb+srv://api:api@cluster0.fm27z.mongodb.net/prospectos?retryWrites=true&w=majority'
mongo = PyMongo(app) # conexión
# CORS(app)
cors = CORS(app, resources={r"/prospectos/*": {"origins": "*"}},
            headers="Content-Type")
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}},
#             headers="Content-Type")

db = mongo.db.prospectos

@app.route('/prospectos/captura', methods=['POST'])
@cross_origin()
def captura():
    id = db.insert({
        'nombre': request.json['nombre'],
        'appaterno': request.json['appaterno'],
        'apmaterno': request.json['apmaterno'],
        'calle': request.json['calle'],
        'colonia': request.json['colonia'],
        'codpos': request.json['codpos'],
        'telefono': request.json['telefono'],
        'rfc': request.json['rfc'],
        'estatus': request.json['estatus'],
        'rechazo': request.json['rechazo']
    })
    return jsonify(str(ObjectId(id)))

@app.route('/prospectos/listado', methods=['GET'])
@cross_origin()
def listado():
    prospectos = []
    for prospecto in db.find():
        prospectos.append({
            '_id': (str(ObjectId(prospecto['_id']))),
            'nombre': prospecto['nombre'],
            'appaterno': prospecto['appaterno'],
            'apmaterno': prospecto['apmaterno'],
            'estatus': prospecto['estatus']
        })
    return jsonify(prospectos)

@app.route('/prospectos/detalle/<id>', methods=['GET'])
@cross_origin()
def detalle(id):
    prospecto = db.find_one({'_id': ObjectId(id)})
    print(prospecto)
    return jsonify({
        '_id': str(ObjectId(prospecto['_id'])),
        'nombre': prospecto['nombre'],
        'appaterno': prospecto['appaterno'],
        'apmaterno': prospecto['apmaterno'],
        'calle': prospecto['calle'],
        'colonia': prospecto['colonia'],
        'codpos': prospecto['codpos'],
        'telefono': prospecto['telefono'],
        'rfc': prospecto['rfc'],
        'estatus': prospecto['estatus'],
        'rechazo': prospecto['rechazo']
    })

@app.route('/prospectos/evaluacion/<id>', methods=['PUT'])
@cross_origin()
def evaluacion(id):
    prospecto = db.find_one({'_id': ObjectId(id)})
    print(prospecto)
    db.update_one({'_id': ObjectId(id)}, {'$set': {
        'nombre': request.json['nombre'],
        'appaterno': request.json['appaterno'],
        'apmaterno': request.json['apmaterno'],
        'calle': request.json['calle'],
        'colonia': request.json['colonia'],
        'codpos': request.json['codpos'],
        'telefono': request.json['telefono'],
        'rfc': request.json['rfc'],
        'estatus': request.json['estatus'],
        'rechazo': request.json['rechazo']
    }})
    return jsonify({'msg': 'Prospecto Evaluado'})

if __name__ == "__main__":
    app.run(debug=True)