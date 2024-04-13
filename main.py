from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

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
    
    def __init__(self, sku: str, nombre_producto: str, categoria: int, sub_categoria: int, marca: int, modelo: str, costo_sin_iva: float, costo_con_iva: float):
        self.sku = sku
        self.nombre_producto = nombre_producto
        self.categoria = categoria
        self.sub_categoria = sub_categoria
        self.marca = marca
        self.modelo = modelo
        self.costo_con_iva = costo_con_iva
        self.costo_sin_iva = costo_sin_iva

# FIN Modelos

# @note - Endpoints
@app.route('/')
def index():
    productos_con_detalle = db.session.query(
        Productos.sku,
        Productos.nombre_producto,
        Categoria.categoria,
        SubCategoria.sub_categoria,
        Productos.marca,
        Productos.id,
        Productos.costo_sin_iva
        ).\
    join(Categoria, Productos.categoria == Categoria.id).\
    join(SubCategoria, Productos.sub_categoria == SubCategoria.id).\
    join(Marca, Productos.marca == Marca.id).all()

    marca_campos = db.session.query(Marca.id, Marca.marca)

    categoria_campos = db.session.query(Categoria.id, Categoria.categoria)

    sub_categoria_campos = db.session.query(SubCategoria.id, SubCategoria.padre, SubCategoria.sub_categoria)

    print(productos_con_detalle)

    context = {
        "all_data" : productos_con_detalle,
        "marca_data" : marca_campos,
        "categoria_data" : categoria_campos,
        "sub_categoria_data" : sub_categoria_campos,
    }

    return render_template('index.html', **context)

@app.route('/insert', methods = ['POST']) # type: ignore
def insert():
    if request.method == 'POST':

        sku = request.form['sku']
        nombre_producto = request.form['nombre_producto']
        categoria = request.form['categoria']
        sub_categoria = request.form['sub_categoria']
        marca = request.form['marca']
        modelo = request.form['modelo']
        costo_sin_iva = request.form['costo_sin_iva']
        costo_con_iva = costo_sin_iva * 1.16

        my_data = Productos(sku, nombre_producto, categoria, sub_categoria, marca, modelo, costo_sin_iva, costo_con_iva)
        db.session.add(my_data)
        db.session.commit()

        flash('Producto insertado en la base de datos') # Mensaje flask insertar
        
        return redirect(url_for('index'))
    
@app.route('/update', methods = ['GET','POST']) # type: ignore
def update():
    if request.method == 'POST':
        my_data = Productos.query.get(request.form.get('id')) # Se puede obtener también con get

        my_data.name = request.form['nombre_producto']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']

        db.session.commit()

        flash('Producto actualizado')

        return redirect(url_for('index'))

# FIN Endpoints

if __name__ == '__main__':
    app.run(debug=True)