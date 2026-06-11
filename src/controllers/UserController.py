from models.UserModel import UsuarioModel

class AuthController:
    def __init__(self):
        self.model = UsuarioModel()
        
    def login_google(self, nombre, correo, foto):

        user = self.model.buscar_por_correo(correo)
        if user:
            return user, "Login correcto"
        nuevo = self.model.crear_google(
            nombre,
            correo,
            foto
        )
        return nuevo, "Usuario creado"
        
        
    