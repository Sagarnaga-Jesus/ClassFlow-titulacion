from models.databaseModel import Database

class ParticipantesModel:

    def __init__(self):
        self.db = Database().get_connection()

    def obtener_participantes(self, id_clase):
        
        

        cursor = self.db.cursor(dictionary=True)

        cursor.execute("""
            SELECT a.id_alumno, a.nombre, a.correo
            FROM alumnos_clase ac
            JOIN alumnos a ON ac.id_alumno = a.id_alumno
            WHERE ac.id_clase = %s
        """, (id_clase,))

        participantes = cursor.fetchall()

        cursor.close()
        self.db.close()

        return participantes