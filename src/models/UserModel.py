import bcrypt
from models.databaseModel import Database

class UsuarioModel:
    def __init__(self):
        self.db = Database()
    
    def buscar_por_correo(self, correo):

        conn = None
        cursor = None
        
        try:
            conn= self.db.get_connection()
            cursor=conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM profesores WHERE correo=%s",(correo,))
            user = cursor.fetchone()
            conn.close()
            if user:
                return user
            else:
                return False
            
        except Exception as err:
            print(f"Error: {err}")
            return False
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
    
    def crear_google(self, nombre, correo, foto):

        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
    
        cursor.execute(
            """
            INSERT INTO profesores(nombre, correo, foto)
            VALUES(%s, %s, %s)
            """,
            (nombre, correo, foto)
        )
    
        conn.commit()
    
        id_usuario = cursor.lastrowid
    
        cursor.execute(
            "SELECT * FROM profesores WHERE id_profesor = %s",
            (id_usuario,)
        )
    
        user = cursor.fetchone()
    
        cursor.close()
        conn.close()
    
        return user
    