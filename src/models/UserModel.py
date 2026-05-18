import bcrypt
from models.databaseModel import Database

class UsuarioModel:
    def __init__(self):
        self.db = Database()
    
    def buscar_por_correo(self, correo):

        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
    
        cursor.execute(
            "SELECT * FROM profesores WHERE correo = %s",
            (correo,)
        )
    
        user = cursor.fetchone()
    
        cursor.close()
        conn.close()
    
        return user
    
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
    
    def existe_correo(self,correo):
        conn = None
        cursor = None
        
        try:
            conn= self.db.get_connection()
            cursor=conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM profesores WHERE correo=%s",(correo,))
            user = cursor.fetchone()
            conn.close()
            if user:
                return True
            else:
                return False
            
        except Exception as err:
            print(f"Error: {err}")
            return False
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
    
    def cambiar_password(self,password,correo):
        conn = None
        cursor = None
        
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(
            password.encode('utf-8'),
            salt
        )
        
        try:
            conn= self.db.get_connection()
            cursor=conn.cursor(dictionary=True)
            cursor.execute("UPDATE profesores SET password = %s WHERE correo = %s", (hashed, correo))
            
            conn.commit()
            return True
        except Exception as err:
            print(f"Error: {err}")
            return False
        finally:
            if cursor:
                cursor.close()

            if conn:
                conn.close()