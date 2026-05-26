from models.databaseModel import Database
from googleapiclient.discovery import build

class ParticipantesModel:
    
    def __init__(self):
        self.db = Database()
    
    def google_participantes(self, creds, id_google):
        service = build("classroom", "v1", credentials=creds)
        
        students = []
        page_token = None
        
        while True:
            try:
                response = service.courses().students().list(
                    courseId=id_google,
                    pageToken=page_token
                ).execute()
        
                for s in response.get("students", []):
                    students.append({
                        "id_google": s["userId"],
                        "nombre": s["profile"]["name"]["fullName"],
                        "email": s["profile"].get("emailAddress")
                    })
        
                page_token = response.get("nextPageToken")
        
                if not page_token:
                    break
        
            except Exception as e:
                print("Error obteniendo alumnos:", e)
                break
    
        return students

    def guardar_participantes(self, id_google_clase, participantes):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
    
        cursor.execute("SELECT id_clase FROM clase WHERE id_google=%s", (id_google_clase,))
        clase = cursor.fetchone()
        if not clase:
            print("Clase no encontrada en BD")
            return
        id_clase = clase["id_clase"]
    
        for p in participantes:
            id_google = p["id_google"]
            nombre = p["nombre"]
            email = p["email"]
    
            cursor.execute("SELECT id_alumno FROM alumnos WHERE id_google=%s", (id_google,))
            alumno = cursor.fetchone()
    
            if alumno is not None:
                cursor.execute(
                    "UPDATE alumnos SET nombre=%s, correo=%s WHERE id_google=%s",
                    (nombre, email, id_google)
                )
                id_alumno = alumno["id_alumno"]
            else:
                cursor.execute(
                    "INSERT INTO alumnos (id_google, nombre, correo) VALUES (%s, %s, %s)",
                    (id_google, nombre, email)
                )
                id_alumno = cursor.lastrowid
    
            cursor.execute(
                "INSERT IGNORE INTO alumnos_clase (id_alumno, id_clase) VALUES (%s, %s)",
                (id_alumno, id_clase)
            )
    
        conn.commit()
        cursor.close()
        conn.close()


    def obtener_alumnos(self, id_clase):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
    
        query = """
            SELECT a.id_alumno, a.id_google, a.nombre, a.correo
            FROM alumnos a
            INNER JOIN alumnos_clase ac ON a.id_alumno = ac.id_alumno
            WHERE ac.id_clase = %s
        """
        cursor.execute(query, (id_clase,))
        alumnos = cursor.fetchall()
    
        cursor.close()
        conn.close()
        return alumnos
