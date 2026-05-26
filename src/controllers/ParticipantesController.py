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
    
    def obtener_alumnos(self, id_clase):
        return self.model.obtener_alumnos(id_clase)