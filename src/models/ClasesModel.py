from models.databaseModel import Database

class ClasesModel:
    def __init__(self):
        self.db = Database()
    
    def obtener_clases(self, id_profesor):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM clase WHERE id_profesor = %s", (id_profesor,))
            clases = cursor.fetchall()
            return clases
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    
    def agregar_clase(self, id_profesor, nombre, descripcion):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clase (nombre, descripcion, id_profesor) VALUES (%s, %s, %s)",
            (nombre,descripcion,id_profesor)
        )
        conn.commit()
        conn.close()