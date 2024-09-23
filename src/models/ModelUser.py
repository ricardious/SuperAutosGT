from models.entities.User import User


# Datos predefinidos para autenticación (sin base de datos)
class ModelUser:

    @classmethod
    def get_user(cls, username):

        predefined_users = [User("empleado", "$uper4utos#")]

        for user in predefined_users:
            if user.username == username:
                return user
        return None
