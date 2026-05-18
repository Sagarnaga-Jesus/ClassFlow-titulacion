import flet as ft
from models.ParticipantesModel import ParticipantesModel

class ParticipantesController:
    def __init__(self):
        self.model = ParticipantesModel()
        
    def obtener_google(self, creds, id_google):
        return self.model.obtener_participantes(creds, id_google)
    