import flet as ft
from models.ParticipantesModel import ParticipantesModel

class ParticipantesController:
    def __init__(self, db):
        self.model = ParticipantesModel()
        
    def obtener(self, id_clase):
        return self.model.obtener_participantes(id_clase), "Participantes obtenidos exitosamente"