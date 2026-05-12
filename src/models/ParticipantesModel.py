import flet as ft

class ParticipantesModel:
    def __init__(self, db):
        self.db = db
        
    def obtener_participantes(self, id_clase):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT a.id_alumno, a.nombre, a.correo
            FROM alumnos_clase ac
            JOIN alumnos a ON ac.id_alumno = a.id_alumno
            WHERE ac.id_clase = %s
        """, (id_clase,))
        return cursor.fetchall()