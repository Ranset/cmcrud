from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# @note Config ORM
app.secret_key = 'MySecretKey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:''@localhost:3306/productos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Si no ponemos esto nos manda una advertencia

db = SQLAlchemy(app)

# @note Modelos
class Categoria(db.Model):
    __tablename__ = 'categoria'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    categoria = db.Column(db.String(50), nullable=False, collation='utf8mb4_general_ci')

    def __init__ (self, categoria) -> None:
        self.categoria = categoria

class SubCategoria(db.Model):
    __tablename__ = 'sub_categoria'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    padre = db.Column(db.Integer, nullable=False)
    sub_categoria = db.Column(db.String(50), nullable=False, collation='utf8mb4_general_ci')
    
    def __init__(self, padre, sub_categoria):
        self.padre = padre
        self.sub_categoria = sub_categoria

class Marca(db.Model):
    __tablename__ = 'marca'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    marca = db.Column(db.String(50), nullable=False, collation='utf8mb4_general_ci')

    def __init__(self, marca) -> None:
        self.marca = marca

class Productos(db.Model):
    __tablename__ = 'productos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sku = db.Column(db.String(50, collation='utf8mb4_general_ci'), nullable=True)
    nombre_producto = db.Column(db.String(300, collation='utf8mb4_general_ci'), nullable=True)
    categoria = db.Column(db.Integer, nullable=True)
    sub_categoria = db.Column(db.Integer, nullable=True)
    marca = db.Column(db.Integer, nullable=True)
    modelo = db.Column(db.String(50, collation='utf8mb4_general_ci'), nullable=True)
    costo_con_iva = db.Column(db.Integer, nullable=True)
    costo_sin_iva = db.Column(db.Integer, nullable=True)
    
    def __init__(self, sku, nombre_producto, categoria, sub_categoria, marca, modelo, costo_con_iva, costo_sin_iva):
        self.sku = sku
        self.nombre_producto = nombre_producto
        self.categoria = categoria
        self.sub_categoria = sub_categoria
        self.marca = marca
        self.modelo = modelo
        self.costo_con_iva = costo_con_iva
        self.costo_sin_iva = costo_sin_iva

# FIN Modelos

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)