from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)


#configuracion de la BD
app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='tienda_db'

mysql = MySQL(app)

@app.route('/')
def inicio():
    return render_template('index.html')

#PRIMER ENDPOINT LISTAR CATEGORIAS
@app.route('/categorias', methods=['GET'])
def listar_categorias():
    cursor = mysql.connection.cursor()
    cursor.execute("select id, nombre from categoria")
    datos = cursor.fetchall()

    categorias = []
    for fila in datos:
        categorias.append({
            "id": fila[0],
            "nombre": fila[1]
        })
    cursor.close()
    return jsonify(categorias)

#SEGUNDO ENDPOINT: LISTAR PRODUCTOS
@app.route('/productos', methods=['GET'])
def listar_productos():
    cursor = mysql.connection.cursor()
    sql = "select * from producto"
    cursor.execute(sql)
    datos = cursor.fetchall()
    productos = []
    for filas in datos:
        productos.append(
            {
                "id" : filas[0],
                "nombre": filas[1],
                "precio": filas[2],
                "stock": filas[3],
                "categoria_id": filas[4]
            }
        )
    cursor.close()
    return jsonify(productos)

#Tercer endpoint: productos con nombre de categoría
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

#Cuarto endpoint: filtrar productos por categoría
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

#Endpoint POST /productos
@app.route('/productos', methods = ['POST'])
def inserta_producto():
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

#ENDPOINT QUE FILTRA DATOS USANDO PARAMETROS
@app.route('/productos_filtrados', methods=['GET'])
def productos_filtrados():
    categoria = request.args.get('categoria')
    precio_min = request.args.get('precio_min')
    stock = request.args.get('stock')

    cursor = mysql.connection.cursor()
    query = "SELECT id, nombre, precio, stock FROM producto WHERE 1 = 1"
    param = []
    if categoria:
        query+= " AND categoria_id = %s"
        param.append(categoria)
    if precio_min:
        query+= " AND precio >= %s"
        param.append(precio_min)
    if stock:
        query+=" AND stock >= %s"
        param.append(stock)
    print(query)
    cursor.execute(query, tuple(param))
    datos = cursor.fetchall()

    productos=[]
    for fila in datos:
        productos.append(
            {
                "id": fila[0],
                "nombre": fila[1],
                "precio": fila[2],
                "stock": fila[3]
            }
        )
    cursor.close()
    return jsonify(productos)



if __name__ == '__main__':
    app.run(debug=True)