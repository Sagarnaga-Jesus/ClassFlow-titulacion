from models.databaseModel import Database


class AsistenciaModel:
    def __init__(self):
        self.db = Database()
        
    def guardar_asistencia( self, id_alumno, id_unidad, faltas, asistencias_maximas):
        
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT id_asistencia
                FROM asistencia
                WHERE id_alumno = %s AND id_unidad = %s
            """, (id_alumno, id_unidad))

            existe = cursor.fetchone()

            if existe:
                cursor.execute("""
                    UPDATE asistencia
                    SET faltas = %s, asistencias_maximas = %s
                    WHERE id_alumno = %s AND id_unidad = %s
                """, (faltas, asistencias_maximas, id_alumno, id_unidad))
            else:
                cursor.execute("""
                    INSERT INTO asistencia
                    (id_alumno, id_unidad, faltas, asistencias_maximas)
                    VALUES (%s, %s, %s, %s)
                """, (id_alumno, id_unidad, faltas, asistencias_maximas))

            conn.commit()

            return True, "Asistencia guardada correctamente"

        except Exception as e:
            conn.rollback()
            print("ERROR:", e)
            return False, str(e)

        finally:
            cursor.close()
            conn.close()
            
    def obtener_asistencia(
        self,
        id_unidad
    ):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT 
                    a.id_alumno,
                    a.nombre,
                    asis.faltas,
                    asis.asistencias_maximas
                FROM asistencia asis
                JOIN alumnos a ON asis.id_alumno = a.id_alumno
                WHERE asis.id_unidad = %s
            """, (id_unidad,))

            resultados = cursor.fetchall()

            return resultados

        except Exception as e:
            print("ERROR:", e)
            return []

        finally:
            cursor.close()
            conn.close()