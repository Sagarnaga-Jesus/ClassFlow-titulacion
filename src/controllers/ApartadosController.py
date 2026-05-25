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
    
    def eliminar_clase(self, id_clase):
        return self.model.eliminar(id_clase)

class UnidadesController:
    def __init__(self):
        self.model = UnidadesModel()
    
    def obtener_unidades(self, id_clase):
        return self.model.obtener_unidades(id_clase)

    def agregar_unidad(self, id_clase, nombre, examen, proyecto, lista, actividades, extra):
        self.model.agregar_unidad(id_clase, nombre, examen, proyecto, lista, actividades, extra)
        
        return True, "Unidad agregada exitosamente"
    
    def elimina(self, id_unidad):
        return self.model.eliminar_unidad(id_unidad)

class ActividadesController:
    def __init__(self):
        self.model = ActividadesModel()
        
    def obtener_google(self, creds, id_google):
        return self.model.google_actividades(creds,id_google)
    
    def obtener_actividades(self, id_unidad):
        return self.model.obtener_actividades(id_unidad)
        
    
    def agregar_actividad(self, id_unidad, titulo, descripcion, tipo, valor, fecha_entrega, id_google):
        return self.model.guardar_actividades(id_unidad, titulo, descripcion, tipo, valor, fecha_entrega, id_google)

