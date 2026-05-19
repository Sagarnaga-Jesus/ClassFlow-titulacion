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
                        "email": s["profile"]["emailAddress"]
                    })
        
                page_token = response.get("nextPageToken")
        
                if not page_token:
                    break
        
            except Exception as e:
                print("Error obteniendo alumnos:", e)
                break
    
        return students
