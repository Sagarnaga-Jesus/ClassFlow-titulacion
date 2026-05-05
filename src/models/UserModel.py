import bcrypt
from models.databaseModel import Database

class UsuarioModel:
    def __init__(self):
        self.db = Database()
    
    def registrar(self, usuario_data):
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(
            usuario_data.password.encode('utf-8'),
            salt
        )
        
        conn= self.db.get_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM profesores WHERE correo=%s",(usuario_data.email,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return False
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO profesores (nombre, correo, password, telefono) VALUES (%s, %s, %s, %s)",
                (
                    usuario_data.nombre,
                    usuario_data.email,
                    hashed_pw.decode('utf-8'),
                    usuario_data.telefono
                )
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            conn.close()
    
    def validar_login(self,email,password):
        
        conn = None
        cursor = None
        try:
            conn= self.db.get_connection()
            cursor=conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM profesores WHERE correo=%s",(email,))
            user = cursor.fetchone()
            conn.close()
            
            if user and bcrypt.checkpw(password.encode('utf-8'),user['password'].encode('utf-8')):
                conn = self.db.get_connection()
                cursor = conn.cursor()
            
                """cursor.execute(
                    "UPDATE profesores SET ultimo_ingreso = NOW() WHERE id_profesor = %s",
                    (user["id_profesor"],)
                )"""
                
                
            
                conn.commit()
                conn.close()
                return user
            return None
        except Exception as err:
            return False
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
            