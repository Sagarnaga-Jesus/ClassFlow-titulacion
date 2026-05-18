from models.databaseModel import Database
from googleapiclient.discovery import build

class ParticipantesModel:
    
    def __init__(self):
        self.db = Database()
    
    def obtener_google(self,creds,id_google):

        service = build(
            "classroom",
            "v1",
            credentials=creds
        )
    
        results = service.courses().students().list(
            courseId=id_google
        ).execute()
    
        return results.get("students", [])