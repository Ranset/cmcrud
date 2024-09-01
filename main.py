from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqlamodel import ModelView

app = Flask(__name__)

# @note - Config ORM
app.secret_key = 'MySecretKey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:''@localhost:3306/productos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Si no ponemos esto nos manda una advertencia

db = SQLAlchemy(app)

# @note - Modelos
class Categoria(db.Model):
    __tablename__ = 'categoria'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    categoria = db.Column(db.String(50), nullable=False)

    def __init__ (self, categoria) -> None:
        self.categoria = categoria

class SubCategoria(db.Model):
    __tablename__ = 'sub_categoria'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    padre = db.Column(db.Integer, nullable=False)
    sub_categoria = db.Column(db.String(50), nullable=False)
    
    def __init__(self, padre, sub_categoria):
        self.padre = padre
        self.sub_categoria = sub_categoria

class Marca(db.Model):
    __tablename__ = 'marca'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    marca = db.Column(db.String(50), nullable=False)

    def __init__(self, marca) -> None:
        self.marca = marca

class Productos(db.Model):
    __tablename__ = 'productos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sku = db.Column(db.String(50), nullable=True)
    nombre_producto = db.Column(db.String(300), nullable=True)
    categoria = db.Column(db.Integer, nullable=True)
    sub_categoria = db.Column(db.Integer, nullable=True)
    marca = db.Column(db.Integer, nullable=True)
    modelo = db.Column(db.String(50), nullable=True)
    costo_con_iva = db.Column(db.Integer, nullable=True)
    costo_sin_iva = db.Column(db.Integer, nullable=True)
    peso = db.Column(db.Float, nullable=True)
    
    def __init__(self, sku: str, nombre_producto: str, categoria: int, sub_categoria: int, marca: int, modelo: str, costo_sin_iva: float, costo_con_iva: float, peso: float):
        self.sku = sku
        self.nombre_producto = nombre_producto
        self.categoria = categoria
        self.sub_categoria = sub_categoria
        self.marca = marca
        self.modelo = modelo
        self.costo_con_iva = costo_con_iva
        self.costo_sin_iva = costo_sin_iva
        self.peso = peso

    def __repr__(self) -> str:
        return self.nombre_producto
    
class Config(db.Model):
    __tablename__ = 'config'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Clave = db.Column(db.String(50), nullable=True)
    Valor = db.Column(db.String(50), nullable=True)

# FIN Modelos

# @note - Endpoints
@app.route('/')
def index():
    productos_con_detalle = db.session.query(
        Productos.sku,
        Productos.nombre_producto,
        Categoria.categoria,
        SubCategoria.sub_categoria,
        Marca.marca,
        Productos.modelo,
        Productos.id,
        Productos.costo_sin_iva,
        Productos.costo_con_iva,
        Productos.peso
        ).\
    join(Categoria, Productos.categoria == Categoria.id).\
    join(SubCategoria, Productos.sub_categoria == SubCategoria.id).\
    join(Marca, Productos.marca == Marca.id).all()

    cambio_dolar = db.session.query(Config.Valor).filter(Config.Clave == "cambio_dolar").first()[0]
    
    costo_kg_cuba = db.session.query(Config.Valor).filter(Config.Clave == "costo_kg_cuba").first()[0]

    context = {
        "all_data" : productos_con_detalle,
        "cambio_dolar" : cambio_dolar,
        "costo_kg_cuba" : costo_kg_cuba,
        "test" : '["Mark", "mark@gmail.com", "(01) 22 888 4444"],["Carlos", "carlos@gmail.com", "(01) 22 888 2222"]'
    }

    return render_template('index.html', **context)

@app.route('/insert', methods = ['GET','POST']) # type: ignore
def insert():
    if request.method == 'POST':

        sku = request.form['sku']
        nombre_producto = request.form['nombre_producto']
        
        categoria_and_subcat = request.form['categoria_and_subcat']
        
        categoria = categoria_and_subcat.split('-')[0]
        sub_categoria = categoria_and_subcat.split('-')[1]
        marca = request.form['marca']
        modelo = request.form['modelo']
        costo_sin_iva = request.form['costo_sin_iva']
        costo_con_iva = int(costo_sin_iva) * 1.16
        peso = request.form['peso']

        my_data = Productos(sku, nombre_producto, categoria, sub_categoria, marca, modelo, costo_sin_iva, costo_con_iva,peso)
        db.session.add(my_data)
        db.session.commit()

        flash('Producto insertado en la base de datos') # Mensaje flask insertar
        
        return redirect(url_for('index'))
    
    # method != POST
    marca_campos = db.session.query(Marca.id, Marca.marca)
    categoria_campos = db.session.query(Categoria.id, Categoria.categoria)
    sub_categoria_campos = db.session.query(SubCategoria.id, SubCategoria.padre, SubCategoria.sub_categoria)

    context = {
        "marca_data" : marca_campos,
        "categoria_data" : categoria_campos,
        "sub_categoria_data" : sub_categoria_campos,
    }
    
    return render_template('insert.html', **context)
    
@app.route('/update', methods = ['GET','POST']) # type: ignore
def update():
    if request.method == 'POST':
        my_data = Productos.query.get(request.form.get('id')) # Se puede obtener también con get

        my_data.sku = request.form['sku']
        my_data.nombre_producto = request.form['nombre_producto']
        
        categoria_and_subcat = request.form['categoria_and_subcat']
        
        my_data.categoria = categoria_and_subcat.split('-')[0]
        my_data.sub_categoria = categoria_and_subcat.split('-')[1]
        my_data.marca = request.form['marca']
        my_data.modelo = request.form['modelo']

        costo_sin_iva = request.form['costo_sin_iva']

        my_data.costo_sin_iva = costo_sin_iva
        my_data.costo_con_iva = int(costo_sin_iva) * 1.16

        db.session.commit()

        flash('Producto actualizado')

        return redirect(url_for('index'))
    
@app.route('/delete', methods= ['POST'])
def delete():
    data = request.json  # Obtener el JSON enviado en la solicitud
    if data:
        array = data.get('array')  # Extraer el array del JSON
        for data in array:
            id = data['id']
            my_data = Productos.query.get(id)
            db.session.delete(my_data)
            db.session.commit()

        flash('Producto Borrado')
        return redirect(url_for('index'))
        
    else:
        return jsonify({"message": "No se recibió ningún array"}), 400


    # flash('Producto Borrado')


# FIN Endpoints

# @note - Admin
admin = Admin(app)

# Agregamos los medelos a la view del Admin
# admin.add_view(ModelView(Productos, db.session))
admin.add_view(ModelView(Categoria, db.session))
admin.add_view(ModelView(SubCategoria, db.session))
admin.add_view(ModelView(Marca, db.session))

# FIN Admin

if __name__ == '__main__':
    app.run(debug=True)