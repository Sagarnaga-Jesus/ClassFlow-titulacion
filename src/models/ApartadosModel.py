from models.databaseModel import Database
from googleapiclient.discovery import build

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
                        "tipo": a.get("workType")
                    })

                page_token = response.get("nextPageToken")
                if not page_token:
                    break

            except Exception as e:
                print("Error obteniendo actividades:", e)
                break

        return actividades
    
    def guardar_actividades(self, id_google_clase, actividades):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id_clase FROM clase WHERE id_google=%s", (id_google_clase,))
        row = cursor.fetchone()
        if not row:
            print("Clase no encontrada en BD")
            return
        id_clase_interno = row["id_clase"]
    
        for act in actividades:
            fecha = None
            if act["fecha_entrega"]:
                fecha = f"{act['fecha_entrega']['year']}-{act['fecha_entrega']['month']:02d}-{act['fecha_entrega']['day']:02d}"
    
            cursor.execute("SELECT id_actividades FROM actividades WHERE id_google=%s", (act["id_google"],))
            row_act = cursor.fetchone()
    
            if row_act:
                cursor.execute(
                    "UPDATE actividades SET nombre=%s, descripcion=%s, fecha_entrega=%s, tipo=%s WHERE id_google=%s",
                    (act["titulo"], act["descripcion"], fecha, act["tipo"], act["id_google"])
                )
            else:
                cursor.execute(
                    "INSERT INTO actividades (id_google, nombre, descripcion, fecha_entrega, tipo) VALUES (%s, %s, %s, %s, %s)",
                    (act["id_google"], act["titulo"], act["descripcion"], fecha, act["tipo"])
                )
    
        conn.commit()
        cursor.close()
        conn.close()


