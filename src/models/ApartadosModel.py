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
                INSERT INTO evaluacion (id_alumno, id_unidad, calificacion)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE calificacion = VALUES(calificacion)
            """, (id_alumno, id_unidad, calificacion))
            conn.commit()
            return True, "Calificación guardada correctamente"
        except Exception as e:
            print(f"Error: {e}")
            return False, "Error al guardar calificación"
        finally:
            cursor.close()
            conn.close()

    def obtener_calificaciones_por_clase(self, id_clase):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT a.id_alumno, a.nombre, u.id_unidad, u.nombre AS unidad, e.calificacion
                FROM evaluacion e
                JOIN alumnos a ON e.id_alumno = a.id_alumno
                JOIN unidad u ON e.id_unidad = u.id_unidad
                WHERE u.id_clase = %s
                ORDER BY a.id_alumno, u.id_unidad
            """, (id_clase,))
            resultados = cursor.fetchall()
            return resultados
        except Exception as e:
            print(f"Error: {e}")
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
        submissions = service.courses().courseWork().studentSubmissions().list(
            courseId=course_id,
            courseWorkId=coursework_id
        ).execute().get("studentSubmissions", [])
        
        entregas = []
        for s in submissions:
            calificacion = s.get("assignedGrade") or s.get("draftGrade")
            if s["state"] == "RETURNED":
                entregas.append({
                    "userId": s["userId"],
                    "estado": s["state"],
                    "calificacion": calificacion if calificacion is not None else "Sin calificación"
                })
            else:
                entregas.append({
                    "userId": s["userId"],
                    "estado": s["state"],
                    "calificacion": "No entregó"
                })
        return entregas





