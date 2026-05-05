import flet as ft
from pydantic import ValidationError
from models.databaseModel import Database
from models.ClasesModel import ClasesModel

class ClasesController:
    def __init__(self):
        self.model = ClasesModel()
        
    def obtener_clases(self, id_profesor):
        return self.model.obtener_clases(id_profesor)
    
    def agregar_clase(self,id_profesor ,nombre, descripcion):
        self.model.agregar_clase(id_profesor, nombre, descripcion)
        return True, "Clase agregada exitosamente"