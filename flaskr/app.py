from flaskr import create_app
from .modelos import db
from flask_restful import Api
from .vistas.vistas import VistaLibros, VistaLibro, VistaCategorias, VistaCategoria, VistaLogin, VistaSignIn

app = create_app('default')
app_context = app.app_context()
app_context.push()
db.create_all()

api = Api(app)

# Rutas para ver, editar o eliminar un libro específico
api.add_resource(VistaLibro, '/libro/<int:id_libro>')
api.add_resource(VistaCategoria, '/categoria/<int:id_categoria>')

# Rutas para ver todos los libros y categorías
api.add_resource(VistaLibros, '/libros')
api.add_resource(VistaCategorias, '/categorias')

# Rutas para login e iniciar sesión
api.add_resource(VistaLogin, '/login')
api.add_resource(VistaSignIn, '/signin')
