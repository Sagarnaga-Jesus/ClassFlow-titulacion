import flet as ft
from pydantic import ValidationError
from models.databaseModel import Database
from models.ApartadosModel import ClasesModel, UnidadesModel, ActividadesModel, EvaluacionModel
from models.ParticipantesModel import ParticipantesModel

class EvaluacionController:
    def __init__(self, model, alumnos_model, unidades_model):
        self.model = EvaluacionModel()
        self.alumnos_model = ParticipantesModel()
        self.unidades_model = UnidadesModel()
        

    def calcular_por_clase(self, id_clase):
        alumnos = self.alumnos_model.obtener_alumnos(id_clase)
        unidades = self.unidades_model.obtener_unidades(id_clase)

        resultados = []
        for alumno in alumnos:
            total_clase = 0
            detalle_unidades = []
            for unidad in unidades:
                r = self.calcular_evaluacion(unidad["id_unidad"], alumno["id_alumno"])
                detalle_unidades.append({"unidad": unidad["nombre"], "resultado": r})
                total_clase += r["total"]

            resultados.append({
                "alumno": alumno["nombre"],
                "detalle_unidades": detalle_unidades,
                "total_clase": round(total_clase, 2)
            })
        return resultados


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
        self.participantes_model = ParticipantesModel()
        
    def obtener_google(self, creds, id_google):
        return self.model.google_actividades(creds,id_google)
    
    def obtener_actividades(self, id_unidad):
        return self.model.obtener_actividades(id_unidad)
    
    def obtener_entregas(self, creds, course_id, coursework_id):
        return self.model.obtener_entregas(creds, course_id, coursework_id)
    
    def obtener_entregas_por_actividad(self, creds, id_clase, id_google_clase, coursework_id):
    # 1. Alumnos de la BD
        alumnos = self.participantes_model.obtener_alumnos(id_clase)
    
        # 2. Entregas desde Classroom
        entregas = self.model.obtener_entregas(creds, id_google_clase, coursework_id)
    
        entregados = []
        no_entregados = []
        
        print("Alumnos BD:", [(a["id_google"], a["nombre"]) for a in alumnos])
        print("Entregas Classroom:", [(e["userId"], e["estado"]) for e in entregas])

    
        for alumno in alumnos:
            entrega = next((e for e in entregas if e["userId"] == alumno["id_google"]), None)
            if entrega and entrega["estado"] in ["TURNED_IN", "RETURNED"]:
                entregados.append(alumno)
            else:
                no_entregados.append(alumno)
                
            for alumno in alumnos:
                entrega = next((e for e in entregas if e["userId"] == alumno["id_google"]), None)
                estado = entrega["estado"] if entrega else "NO ENCONTRADO"
                print(alumno["nombre"], alumno["id_google"], "->", estado)

    
        return entregados, no_entregados

    
    def agregar_actividad(self, id_unidad, titulo, descripcion, tipo, valor, fecha_entrega, id_google):
        return self.model.guardar_actividades(id_unidad, titulo, descripcion, tipo, valor, fecha_entrega, id_google)

