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

    def guardar_participantes(self, id_clase, participantes):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        for p in participantes:
            id_google = p["id_google"]
            nombre = p["nombre"]
            email = p["email"]
    
            cursor.execute("SELECT id_alumno FROM alumnos WHERE id_google=%s", (id_google,))
            alumno = cursor.fetchone()
    
            if alumno:
                cursor.execute(
                    "UPDATE alumnos SET nombre=%s, correo=%s WHERE id_google=%s",
                    (nombre, email, id_google)
                )
                id_alumno = alumno[0]
            else:
                cursor.execute(
                    "INSERT INTO alumnos (id_google, nombre, correo) VALUES (%s, %s, %s)",
                    (id_google, nombre, email)
                )
                id_alumno = cursor.lastrowid
    
            cursor.execute(
                "INSERT INTO alumnos_clase (id_alumno, id_clase) VALUES (%s, %s)",
                (id_alumno, id_clase)
            )

    
        conn.commit()
        cursor.close()
        conn.close()

