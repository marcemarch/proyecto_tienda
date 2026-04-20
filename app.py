from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL(app)

#Conexion a la BD tienda_db
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "tienda_db"

@app.route('/')
def inicio():
    return "Servidor ejecutandose!!! 😎"

@app.route('/categorias', methods=['GET'])
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

@app.route('/test')
def test():
    cursor =mysql.connection.cursor()
    sql = "SELECT 1"
    cursor.execute(sql)
    cursor.close()
    return "conexion exitosa!"



@app.route('/productos', methods=['GET'])
def lista_productos():
    cursor = mysql.connection.cursor()
    sql = "select , nombre, precio, stock, categoria_id from producto"
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
    sql = """select p.id, p.nombre, p.precio, p.stock, c.nombre
            from producto p
            join categoria c on p.categoria_id = c.id"""
    cursor.execute(sql)
    datos = cursor.fetchall()

    productos = []
    for fila in datos:
        productos.append(
            {
                "id": fila[0],
                "nombre": fila[1],
                "precio": float(fila[2]),
                "stock": fila[3],
                "categoria": fila[4]
            }
        )
    cursor.close()
    return jsonify(productos)
    
#3er endpoint post sobre categoria
@app.route('/categorias', methods=['POST'])
def inserta_categoria():
    data = request.get_json()
    nombre = data['nombre']

    cursor = mysql.connection.cursor()
    sql = """insert into categoria(nombre)
            values (%s)"""
    cursor.execute(sql, (nombre,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"mensaje":"Producto insertado"}), 201

if __name__ == '__main__':
    app.run(debug=True)