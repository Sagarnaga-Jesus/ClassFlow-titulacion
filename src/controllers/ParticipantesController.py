import flet as ft
from models.ParticipantesModel import ParticipantesModel
from googleapiclient.discovery import build

class ParticipantesController:
    def __init__(self):
        self.model = ParticipantesModel()
        
    def obtener_google(self, creds, id_clase):
        participantes=self.model.google_participantes(creds, id_clase)
        
        self.model.guardar_participantes(id_clase, participantes)

        return participantes