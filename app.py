from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json

app = Flask(__name__)
app.secret_key = 'clave_secreta_mazahuas'

# ==========================================
# CONEXIÓN INTELIGENTE (LOCAL O INTERNET)
# ==========================================
URL_NUBE = os.environ.get('DATABASE_URL')

if URL_NUBE:
    import psycopg2
    def conectar():
        return psycopg2.connect(URL_NUBE)
else:
    import mysql.connector
    def conectar():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="directorio_artesanos"
        )

class ConvertidorDecimal(json.JSONEncoder):
    def default(self, obj):
        import decimal
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(ConvertidorDecimal, self).default(obj)

@app.template_filter('tojson_seguro')
def tojson_seguro(obj):
    return json.dumps(obj, cls=ConvertidorDecimal, ensure_ascii=False)

@app.route('/')
def menu_principal():
    return render_template('index.html')

@app.route('/artesanos', methods=['GET', 'POST'])
def artesanos():
    conexion = conectar()
    cursor = conexion.cursor()
    if request.method == 'POST':
        accion = request.form.get('accion')
        id_artesano = request.form.get('id_artesano')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        telefono = request.form.get('telefono')
        email = request.form.get('email')
        direccion = request.form.get('direccion')
        municipio = request.form.get('municipio')
        descripcion = request.form.get('descripcion')
        pagina_web = request.form.get('pagina_web')
        redes_sociales = request.form.get('redes_sociales')

        if accion == 'insertar':
            sql = "INSERT INTO artesanos VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, (id_artesano, nombre, apellido, telefono, email, direccion, municipio, descripcion, pagina_web, redes_sociales))
            flash("Registro agregado correctamente")
        elif accion == 'modificar':
            sql = "UPDATE artesanos SET nombre=%s, apellido=%s, telefono=%s, email=%s, direccion=%s, municipio=%s, descripcion=%s, pagina_web=%s, redes_sociales=%s WHERE id_artesano=%s"
            cursor.execute(sql, (nombre, apellido, telefono, email, direccion, municipio, descripcion, pagina_web, redes_sociales, id_artesano))
            flash("Registro modificado correctamente")
        elif accion == 'eliminar':
            sql = "DELETE FROM artesanos WHERE id_artesano=%s"
            cursor.execute(sql, (id_artesano,))
            flash("Registro eliminado correctamente")
        conexion.commit()
        return redirect(url_for('artesanos'))

    cursor.execute("SELECT * FROM artesanos")
    registros = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template('artesanos.html', registros=registros)

@app.route('/productos', methods=['GET', 'POST'])
def productos():
    conexion = conectar()
    cursor = conexion.cursor()
    if request.method == 'POST':
        accion = request.form.get('accion')
        id_producto = request.form.get('id_producto')
        id_artesano = request.form.get('id_artesano')
        id_categoria = request.form.get('id_categoria')
        nombre_producto = request.form.get('nombre_producto')
        descripcion_producto = request.form.get('descripcion_producto')
        precio = request.form.get('precio')

        if accion == 'insertar':
            sql = "INSERT INTO productos VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, (id_producto, id_artesano, id_categoria, nombre_producto, descripcion_producto, precio))
            flash("Producto agregado correctamente")
        elif accion == 'modificar':
            sql = "UPDATE productos SET id_artesano=%s, id_categoria=%s, text_producto=%s, descripcion_producto=%s, precio=%s WHERE id_producto=%s" if URL_NUBE else "UPDATE productos SET id_artesano=%s, id_categoria=%s, nombre_producto=%s, descripcion_producto=%s, precio=%s WHERE id_producto=%s"
            cursor.execute(sql, (id_artesano, id_categoria, nombre_producto, descripcion_producto, precio, id_producto))
            flash("Producto modificado correctamente")
        elif accion == 'eliminar':
            sql = "DELETE FROM productos WHERE id_producto=%s"
            cursor.execute(sql, (id_producto,))
            flash("Producto eliminado correctamente")
        conexion.commit()
        return redirect(url_for('productos'))

    cursor.execute("SELECT * FROM productos")
    registros = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template('productos.html', registros=registros)

@app.route('/categorias', methods=['GET', 'POST'])
def categorias():
    conexion = conectar()
    cursor = conexion.cursor()
    if request.method == 'POST':
        accion = request.form.get('accion')
        id_categoria = request.form.get('id_categoria')
        nombre_categoria = request.form.get('nombre_categoria')

        if accion == 'insertar':
            sql = "INSERT INTO categorias VALUES (%s,%s)"
            cursor.execute(sql, (id_categoria, nombre_categoria))
            flash("Categoría agregada correctamente")
        elif accion == 'modificar':
            sql = "UPDATE categorias SET nombre_categoria=%s WHERE id_categoria=%s"
            cursor.execute(sql, (nombre_categoria, id_categoria))
            flash("Categoría modificada correctamente")
        elif accion == 'eliminar':
            sql = "DELETE FROM categorias WHERE id_categoria=%s"
            cursor.execute(sql, (id_categoria,))
            flash("Categoría eliminada correctamente")
        conexion.commit()
        return redirect(url_for('categorias'))

    cursor.execute("SELECT * FROM categorias")
    registros = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template('categorias.html', registros=registros)

if __name__ == '__main__':
    puerto = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=puerto)