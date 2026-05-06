from flask import Flask, jsonify, render_template, request
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

    
app = Flask(__name__)
mysql = MySQL(app)

#configurar jwt
app.config['JWT_SECRET_KEY'] = '123'
jwt = JWTManager(app)

#Conexion a la BD tienda_db
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "tienda_db"

@app.route('/')
def inicio(): 
    return render_template("login.html")  
    #return render_template("nueva_categoria_text.html")
    #return render_template("nueva_categoria.html")
    #return render_template("index.html")
    #return "Servidor ejecutandose!!! 😎"
    
@app.route('/test')
def test():
    cursor =mysql.connection.cursor()
    sql = "SELECT 1"
    cursor.execute(sql)
    cursor.close()
    return "conexion exitosa!"

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    if username == 'admin' and password == '123':
        token = create_access_token(identity = username)
        return jsonify(access_token=token)
    return jsonify({"error":"credenciales incorrectas"}), 401

#---------------------------------------------------------
#GET
@app.route('/categorias', methods=['GET'])
@jwt_required()
def listar_categorias():
    cursor = mysql.connection.cursor()
    sql = "select id, nombre from categoria"
    cursor.execute(sql)
    datos = cursor.fetchall()

    categorias = []
    for fila in datos:
        categorias.append(
            {
                "id": fila[0],
                "nombre":fila[1]
            }
        )
    cursor.close()
    return jsonify(categorias)

@app.route('/productos', methods=['GET'])
def lista_productos():
    cursor = mysql.connection.cursor()
    sql = "select id, nombre, precio, stock, categoria_id from producto"
    cursor.execute(sql)
    datos = cursor.fetchall()

    productos = []
    for fila in datos:
        productos.append(
            {
                "id": fila[0],
                "nombre": fila[1],
                "precio": fila[2],
                "stock": fila[3],
                "categoria_id": fila[4]
            }
        )
    cursor.close()
    return jsonify(productos)

@app.route('/productos_categoria', methods=['GET'])
def productos_con_categoria():
    cursor = mysql.connection.cursor()
    sql = "select p.id, p.nombre, p.precio, p.stock, c.nombre from producto p join categoria c on p.categoria_id = c.id"
    cursor.execute(sql)
    datos = cursor.fetchall()

    productos = []
    for filas in datos:
        productos.append({
            "id" : filas[0],
            "nombre": filas[1],
            "precio": filas[2],
            "stock": filas[3],
            "categoria": filas[4]
        })
    cursor.close()
    return jsonify(productos)

@app.route('/productos/categoria/<int:id_categoria>', methods=['GET'])
def productos_por_categoria(id_categoria):
    cursor = mysql.connection.cursor()
    sql = """select p.id, p.nombre, p.precio, p.stock, c.nombre
             from producto p 
             join categoria c on p.categoria_id = c.id
             where c.id = %s"""
    cursor.execute(sql,(id_categoria,))
    datos = cursor.fetchall()

    productos = []
    for filas in datos:
        productos.append(
            {
                "id" : filas[0],
                "nombre": filas[1],
                "precio": filas[2],
                "stock": filas[3],
                "categoria": filas[4]
            }
        )
    cursor.close()
    return jsonify(productos)

#------------------------------------------------------------------------
@app.route('/categorias', methods=['POST'])
@jwt_required()
def insertar_categoria():
    #token = request.headers.get('Authorization')
    #if token != 'Bearer 12345':
    #    return jsonify({'error' : 'no esta autorizado'}),401
   
    return jsonify({"mensaje": "Categoria registrada con exito"}),200

    #recuperando los datos en formato json
#    data = request.get_json()
#    nombre = data["nombre"]

    #insertar en la tabla categoria
#    cursor = mysql.connection.cursor()
#    sql = """INSERT INTO categoria(nombre)
#            VALUES(%s)"""
#    cursor.execute(sql, (nombre,))
#    mysql.connection.commit()
#    cursor.close()
#    return jsonify({"mensaje": "Categoria registrada con exito"}),200

#Endpoint POST /productos
@app.route('/productos', methods = ['POST'])
@jwt_required()
def inserta_producto():
    #token = request.headers.get('Authorization')
    #if token != 'Bearer 12345':
    #    return jsonify({'error' : 'no esta autorizado'}),401

    data = request.get_json()
    nombre = data['nombre']
    precio = data['precio']
    stock = data['stock']
    categoria_id = data['categoria_id']

    cursor = mysql.connection.cursor()
    sql = """ insert into producto(nombre, precio, stock, categoria_id)
            values (%s, %s, %s, %s)"""
    cursor.execute(sql,(nombre, precio, stock, categoria_id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"mensaje":"Producto insertado correctamente"}), 201


#PUT: modificar categoria 
@app.route('/categorias/<int:id>', methods=['PUT'])
def modificar_categoria(id):
    data = request.get_json()
    nombre = data['nombre']

    cursor = mysql.connection.cursor()
    sql= """UPDATE categoria
            SET nombre = %s
            WHERE id = %s """

    cursor.execute(sql,(nombre,id))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje":"categoria modificada"}),200

@app.route('/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    
    data = request.get_json()

    nombre = data['nombre']
    precio = data['precio']
    stock = data['stock']
    categoria_id = data['categoria_id']

    cursor = mysql.connection.cursor()
    sql = """UPDATE producto
              SET nombre = %s,  precio = %s,  stock = %s, categoria_id = %s
              WHERE id = %s"""

    cursor.execute(sql, (nombre , precio, stock, categoria_id , id))

    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje": "Producto actualizado correctamente"}), 200


#endpoint DELETE
@app.route('/categorias/<int:id>', methods=['DELETE'])
def eliminar_categoria(id):
    cursor = mysql.connection.cursor()
    #BUSCAR EL CATEGORIA
    sql = """SELECT nombre FROM categoria WHERE id = %s"""
    cursor.execute(sql, (id,))
    datos = cursor.fetchone()

    if datos is None:
        return jsonify({"mensaje": "la categoria no existe!"})
    
    #cursor = mysql.connection.cursor()
    sql = """DELETE FROM categoria
            WHERE id = %s"""
    cursor.execute(sql,(id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje": "Categoria Eliminada"}),200

    


if __name__ == '__main__':
    app.run(debug=True)