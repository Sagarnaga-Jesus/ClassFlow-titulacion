import flet as ft
from pydantic import ValidationError
from models.databaseModel import Database
from models.ApartadosModel import ClasesModel, UnidadesModel, ActividadesModel

class ClasesController:
    def __init__(self):
        self.model = ClasesModel()
        
    def obtener_clases(self, id_profesor):
        return self.model.obtener_clases(id_profesor)
    
    def agregar_clase(self, id_profesor, id_google, nombre, descripcion):

        success, message = self.model.agregar_clase(
            id_profesor,
            id_google,
            nombre,
            descripcion
        )
    
        return success, message

class UnidadesController:
    def __init__(self):
        self.model = UnidadesModel()
    
    def obtener_unidades(self, id_clase):
        return self.model.obtener_unidades(id_clase)

    def agregar_unidad(self, id_clase, nombre):
        self.model.agregar_unidad(id_clase, nombre)
        
        return True, "Unidad agregada exitosamente"
    

class ActividadesController:
    def __init__(self):
        self.model = ActividadesModel()
    
    def obtener_actividades(self, creds, id_google):
        actividades = self.model.google_actividades(creds, id_google)
        self.model.guardar_actividades(id_google, actividades)
        return actividades
