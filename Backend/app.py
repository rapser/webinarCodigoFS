from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['JWT_SECRET_KEY']="codigowebinar"
app.config['MYSQL_HOST'] = 'x40p5pp7n9rowyv6.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'd5f3bygd0fctwoir'
app.config['MYSQL_PASSWORD'] = 'owcv1txxh2lb22t5'
app.config['MYSQL_DB'] = 'j6esing1lhmqk7kj'


jwt = JWTManager(app)

CORS(app)
mysql = MySQL(app)

@jwt.unauthorized_loader
def prueba(mensaje):
    print(mensaje)
    if mensaje == 'Missing Authorization Header':
        return jsonify({
            'message':'Salte de mi servidor 😁😁'
        })
    else:
        return jsonify({
            'message': mensaje
        })


@app.route('/') #ENDPOINT
@jwt_required
def inicio():
    return {
        'message':'Bienvenido al webinar CodiGo'
    }


@app.route('/productos', methods=['GET'])
@jwt_required
def getProducts():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM t_productos') # ORM
    data = cur.fetchall()
    print(data)
    cur.close()
    if data:
        resultado = []
        for producto in data:
            print(producto)
            resultado.append({
                'id': producto[0],
                'nombre':producto[1],
                'precio':str(producto[2]),
                'disponible':bool(producto[3]),
            })
        return jsonify({
            'ok': True,
            'content': resultado
        }), 200
    return jsonify({
            'ok': True,
            'content': None
        }), 200

@app.route('/agregar_producto',methods=['POST'])
def addProduct():
    if request.is_json:
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO t_productos (prod_nom, prod_prec, prod_disp) VALUES (%s,%s,%s)',
                    (data['nombre'], data['precio'],data['disponible']))
        mysql.connection.commit()
        cur.close()
        return jsonify({
            'ok':True,
            'message':'Producto agregado exitosamente'
        }), 201
    else:
        return jsonify({
            'ok':False,
            'message':'Faltan campos'
        }), 404

@app.route('/producto/<int:id>', methods=['DELETE'])
def eliminarProduct(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM t_productos where prod_id = %s',(id,))
    mysql.connection.commit()
    cur.close()
    return {
        'message':'Se eliminó exitosamente el producto',
    }

if __name__ =='__main__':
    app.run(debug=True)