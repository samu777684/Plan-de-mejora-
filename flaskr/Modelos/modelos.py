from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Categoria(db.Model):
    __tablename__ = 'categoria'
    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))

class Libro(db.Model):
    __tablename__ = 'libro'
    id_libro = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    autor = db.Column(db.String(100))
    precio = db.Column(db.Float)
    stock = db.Column(db.Integer)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id_categoria'))
    descripcion = db.Column(db.String(255))

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    numerodoc = db.Column(db.Integer)
    correo = db.Column(db.String(100), unique=True)
    contrasena_hash = db.Column('contrasena_hash', db.String(100))
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id_rol'))

    @property
    def contrasena(self):
        raise AttributeError("La contraseña no es un atributo legible")

    @contrasena.setter
    def contrasena(self, password):
        if not password:
            raise ValueError("La contraseña no puede estar vacía.")
        self.contrasena_hash = generate_password_hash(password)

    def verificar_contrasena(self, password):
        return check_password_hash(self.contrasena_hash, password)

class Rol(db.Model):
    __tablename__ = 'rol'
    id_rol = db.Column(db.Integer, primary_key=True)
    nombre_rol = db.Column(db.String(50))

# Esquemas

class CategoriaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Categoria
        include_relationships = True
        load_instance = True

class LibroSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Libro
        include_relationships = True
        load_instance = True

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True

class RolSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Rol
        include_relationships = True
        load_instance = True
