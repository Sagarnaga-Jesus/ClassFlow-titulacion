from models.databaseModel import Database
from googleapiclient.discovery import build

class EvaluacionModel:
    def __init__(self):
        self.db = Database()
        
    def guardar_calificacion_unidad(self, id_alumno, id_unidad, calificacion):
        conn = self.db.get_connection()
        cursor = conn.cursor()
    
        try:
            cursor.execute("""
                SELECT id_evaluacion
                FROM evaluacion
                WHERE id_alumno = %s AND id_unidad = %s
            """, (id_alumno, id_unidad))
    
            existe = cursor.fetchone()
    
            if existe:
                cursor.execute("""
                    UPDATE evaluacion
                    SET calificacion = %s
                    WHERE id_alumno = %s
                    AND id_unidad = %s
                """, (float(calificacion), id_alumno, id_unidad))
            else:
                cursor.execute("""
                    INSERT INTO evaluacion
                    (id_alumno, id_unidad, calificacion)
                    VALUES (%s, %s, %s)
                """, (id_alumno, id_unidad, float(calificacion)))
    
            conn.commit()
    
            return True, "Calificación guardada correctamente"
    
        except Exception as e:
            conn.rollback()
            print("ERROR:", e)
            return False, str(e)
    
        finally:
            cursor.close()
            conn.close()
    def obtener_calificaciones_por_clase(self, id_clase):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT 
                    a.id_alumno,
                    a.nombre,
                    u.id_unidad,
                    u.nombre AS unidad,
                    e.calificacion
                FROM evaluacion e
                JOIN alumnos a ON e.id_alumno = a.id_alumno
                JOIN unidad u ON e.id_unidad = u.id_unidad
                WHERE u.id_clase = %s
                ORDER BY a.id_alumno, u.id_unidad
            """, (id_clase,))

            return cursor.fetchall()

        except Exception as e:
            print("ERROR:", e)
            return []

        finally:
            cursor.close()
            conn.close()

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
    
    def agregar_clase(self, id_profesor, id_google, nombre, descripcion):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""SELECT * FROM clase WHERE id_google = %s AND id_profesor = %s""",(id_google, id_profesor))
        existe = cursor.fetchone()
    
        if existe:
            return False, "Clase ya existente"
            
        cursor.execute(
            "INSERT INTO clase (nombre, descripcion, id_profesor, id_google) VALUES (%s, %s, %s,%s)",
            (nombre,descripcion,id_profesor,id_google)
        )
        conn.commit()
        conn.close()
        return True, "Clase agregada correctamente"
    
    def eliminar(self, id_clase):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM clase WHERE id_clase=%s", (id_clase,))
        conn.commit()
        conn.close()
        return "clase eliminada"
        


class UnidadesModel:
    def __init__(self):
        self.db = Database()
    
    def obtener_unidades(self, id_clase):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM unidad WHERE id_clase = %s", (id_clase,))
            unidades = cursor.fetchall()
            return unidades
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
            
    def agregar_unidad(self, id_clase, nombre, examen, proyecto, lista, actividades, extra):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO unidad (nombre, examen, proyecto, lista, actividades, extra ,id_clase) VALUES (%s, %s,%s, %s,%s, %s,%s)",
            (nombre, examen, proyecto, lista, actividades, extra, id_clase)
        )
        conn.commit()
        conn.close()
    
    def eliminar_unidad(self, id_unidad):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM unidad WHERE id_unidad=%s", (id_unidad,))
        conn.commit()
        conn.close()
        return "unidad eliminada"
    def actualizar_unidad(self, id_unidad, datos):
        conn = self.db.get_connection()
        cursor = conn.cursor()
    
        query = """UPDATE unidad SET nombre = %s, examen = %s, proyecto = %s, lista = %s, actividades = %s, extra = %s WHERE id_unidad = %s """
    
        cursor.execute(query, (datos["nombre"],datos["examen"],datos["proyecto"],datos["lista"],datos["actividades"],datos["extra"],id_unidad ))
    
        conn.commit()
        conn.close()
    
        return True, "Unidad actualizada correctamente"

class ActividadesModel:
    
    def __init__(self):
        self.db = Database()
    
    def google_actividades(self, creds, id_google):
        service = build("classroom", "v1", credentials=creds)
        actividades = []
        page_token = None

        while True:
            try:
                response = service.courses().courseWork().list(
                    courseId=id_google,
                    pageToken=page_token
                ).execute()

                for a in response.get("courseWork", []):
                    
                    actividades.append({
                        "id_google": a["id"],
                        "titulo": a["title"],
                        "descripcion": a.get("description"),
                        "fecha_entrega": a.get("dueDate"),
                        "tipo": a.get("workType"),
                        "valor": a.get("maxPoints", 0)
                    })

                page_token = response.get("nextPageToken")
                if not page_token:
                    break

            except Exception as e:
                print("Error obteniendo actividades:", e)
                break

        return actividades
    
    def guardar_actividades(self, id_unidad, titulo, descripcion, tipo, valor, fecha_entrega, id_google):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id_actividades FROM actividades WHERE id_google=%s", (id_google,))
        existe = cursor.fetchone()
    
        if existe:
            return False, "Clase ya existente"
            
        cursor.execute(
            "INSERT INTO actividades (nombre, descripcion, tipo, valor, fecha_entrega, id_google, id_unidad) VALUES (%s, %s, %s,%s,%s, %s,%s)",
            (titulo,descripcion, tipo, valor, fecha_entrega, id_google, id_unidad)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Actividad agregada correctamente"
        
    
    def obtener_actividades(self, id_unidad):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM actividades WHERE id_unidad = %s", (id_unidad,))
            clases = cursor.fetchall()
            return clases
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    
    def obtener_entregas(self, creds, course_id, coursework_id):
        service = build("classroom", "v1", credentials=creds)
    
        response = service.courses().courseWork().studentSubmissions().list(
            courseId=course_id,
            courseWorkId=coursework_id
        ).execute()
    
        submissions = response.get("studentSubmissions", [])
    
        entregas = []
        for s in submissions:
            entregas.append({
                "userId": s.get("userId"),
                "estado": s.get("state"),
                "calificacion": s.get("assignedGrade", s.get("draftGrade", 0))
            })
    
        return entregas
    
    def eliminar_actividad(self, actividad):
        conn = self.db.get_connection()
        cursor = conn.cursor()
    
        try:
            id_actividad = actividad.get("id_actividades")
    
            if not id_actividad:
                return False
    
            cursor.execute(
                "DELETE FROM actividades WHERE id_actividades = %s",
                (id_actividad,)
            )
    
            conn.commit()
    
            return cursor.rowcount > 0
    
        except Exception as e:
            print("Error al eliminar actividad:", e)
            return False
    
        finally:
            conn.close()




