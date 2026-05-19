import flet as ft
from models.ParticipantesModel import ParticipantesModel
from googleapiclient.discovery import build

class ParticipantesController:
    def __init__(self):
        self.model = ParticipantesModel()
        
    def obtener_google(self, creds, id_clase):
        # Usar las credenciales del login
        service = build("classroom", "v1", credentials=creds)

        response = service.courses().students().list(courseId=id_clase).execute()
        students = response.get("students", [])

        participantes = []
        for s in students:
            participantes.append({
                "id_google": s["userId"],
                "nombre": s["profile"]["name"]["fullName"],
                "email": s["profile"].get("emailAddress", "")
            })

        return participantes