import flet as ft
from models.ParticipantesModel import ParticipantesModel

class ParticipantesController:
    def __init__(self):
        self.model = ParticipantesModel()
        
    def obtener(self, id_clase):
        return self.model.obtener_participantes(id_clase)
    
    def agregar (self,nombre,correo,id_clase):
        return self.model.agregar_participante(nombre,correo,id_clase)