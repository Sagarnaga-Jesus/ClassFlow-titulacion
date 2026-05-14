from models.databaseModel import Database

class ParticipantesModel:
    
    def __init__(self):
        self.db = Database()
    
    def obtener_participantes(self, id_clase):

        conn = Database().get_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT a.id_alumno, a.nombre, a.correo
            FROM alumnos_clase ac
            JOIN alumnos a ON ac.id_alumno = a.id_alumno
            WHERE ac.id_clase = %s
        """, (id_clase,))

        participantes = cursor.fetchall()

        cursor.close()
        conn.close()

        return participantes

    def agregar_participante(self, nombre, correo, id_clase):
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO alumnos (nombre, correo) VALUES (%s, %s)",
                (
                    nombre,
                    correo
                )
            )
            
            id_alumno = cursor.lastrowid
            
            cursor.execute(
                """INSERT INTO alumnos_clase (id_alumno, id_clase) VALUES (%s, %s)""",
            (id_alumno, id_clase)
            )
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            conn.close()