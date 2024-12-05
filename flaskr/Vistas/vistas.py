from flask import request
from flask_restful import Resource
from .modelos import db, Usuario, UsuarioSchema, Categoria, CategoriaSchema, Libro, LibroSchema
from flask_jwt_extended import create_access_token

# Uso de los schemas creados en modelos
usuario_schema = UsuarioSchema()
libro_schema = LibroSchema()
categoria_schema = CategoriaSchema()

# Clase para manejar usuarios
class VistaUsuarios(Resource):
    def post(self):
        nuevo_usuario = Usuario(
            nombre=request.json['nombre'],
            correo=request.json['correo'],
            contrasena=request.json['contrasena']  
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return usuario_schema.dump(nuevo_usuario), 201

    def get(self):
        usuarios = Usuario.query.all()
        return [usuario_schema.dump(usuario) for usuario in usuarios], 200

class VistaUsuario(Resource):
    def put(self, id_usuario):
        usuario = Usuario.query.get(id_usuario)
        if not usuario:
            return {'mensaje': 'El usuario no existe'}, 404
        
        usuario.nombre = request.json.get('nombre', usuario.nombre)
        usuario.correo = request.json.get('correo', usuario.correo)
        usuario.contrasena = request.json.get('contrasena', usuario.contrasena)  

        db.session.commit()
        return usuario_schema.dump(usuario), 200
    
    def delete(self, id_usuario):
        usuario = Usuario.query.get(id_usuario)
        if not usuario:
            return {'mensaje': 'Usuario no encontrado'}, 404
        
        db.session.delete(usuario)
        db.session.commit()
        return {'mensaje': 'Usuario eliminado'}, 200

class VistaLibros(Resource):
    def get(self):
        libros = Libro.query.all()
        return [libro_schema.dump(libro) for libro in libros], 200

    def post(self):
        nuevo_libro = Libro(
            titulo=request.json['titulo'],
            autor=request.json['autor'],
            precio=request.json['precio'],
            stock=request.json['stock'],
            categoria_id=request.json['categoria_id'],
            descripcion=request.json['descripcion']
        )
        db.session.add(nuevo_libro)
        db.session.commit()
        return {'mensaje': 'Libro creado exitosamente'}, 201

    def put(self, id_libro):
        libro = Libro.query.get(id_libro)
        if not libro:
            return {'mensaje': 'El libro no existe'}, 404
        
        libro.titulo = request.json.get('titulo', libro.titulo)
        libro.autor = request.json.get('autor', libro.autor)
        libro.precio = request.json.get('precio', libro.precio)
        libro.stock = request.json.get('stock', libro.stock)
        libro.categoria_id = request.json.get('categoria_id', libro.categoria_id)
        libro.descripcion = request.json.get('descripcion', libro.descripcion)

        db.session.commit()
        return libro_schema.dump(libro), 200

    def delete(self, id_libro):
        libro = Libro.query.get(id_libro)
        if not libro:
            return {'mensaje': 'Libro no encontrado'}, 404
        
        db.session.delete(libro)
        db.session.commit()
        return {'mensaje': 'Libro eliminado'}, 200

class VistaCategoria(Resource):
    def put(self, id_categoria):
        categoria = Categoria.query.get(id_categoria)
        if not categoria:
            return {'mensaje': 'La categoría no existe'}, 404
        
        categoria.nombre = request.json.get('nombre', categoria.nombre)
        db.session.commit()
        return categoria_schema.dump(categoria), 200
    
    def delete(self, id_categoria):
        categoria = Categoria.query.get(id_categoria)
        if not categoria:
            return {'mensaje': 'Categoría no encontrada'}, 404
        
        db.session.delete(categoria)
        db.session.commit()
        return {'mensaje': 'Categoría eliminada'}, 200

class VistaCategorias(Resource):
    def get(self):
        categorias = Categoria.query.all()
        return [categoria_schema.dump(categoria) for categoria in categorias], 200

    def post(self):
        nueva_categoria = Categoria(nombre=request.json['nombre'])
        db.session.add(nueva_categoria)
        db.session.commit()
        return {'mensaje': 'Categoría creada exitosamente'}, 201

class VistaLogin(Resource):
    def post(self):
        correo = request.json.get("correo")
        contrasena = request.json.get("contrasena")

        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario and usuario.verificar_contrasena(contrasena):  
            token_de_acceso = create_access_token(identity=correo)
            return {'mensaje': 'Inicio de sesión exitoso', 'token_de_acceso': token_de_acceso}, 200
        return {'mensaje': 'Correo o contraseña incorrectos'}, 401

class VistaSignIn(Resource):
    def post(self):
        correo_existente = Usuario.query.filter_by(correo=request.json["correo"]).first()
        if correo_existente:
            return {'mensaje': 'El correo ya está registrado. Por favor, ingrese otro correo.'}, 400
        
        nuevo_usuario = Usuario(
            nombre=request.json["nombre"],
            correo=request.json["correo"],
            numerodoc=request.json["numerodoc"]
        )
        nuevo_usuario.contrasena = request.json["contrasena"]  

        db.session.add(nuevo_usuario)
        db.session.commit()

        token_de_acceso = create_access_token(identity=nuevo_usuario.correo)
        return {'mensaje': 'Usuario creado exitosamente', 'token': token_de_acceso}, 201
