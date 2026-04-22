from flask import Flask, jsonify
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
    
@app.route('/test')
def test():
    cursor =mysql.connection.cursor()
    sql = "SELECT 1"
    cursor.execute(sql)
    cursor.close()
    return "conexion exitosa!"


#GET
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


if __name__ == '__main__':
    app.run(debug=True)