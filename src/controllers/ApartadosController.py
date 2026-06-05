from models.ApartadosModel import ClasesModel, UnidadesModel, ActividadesModel, EvaluacionModel
from models.ParticipantesModel import ParticipantesModel

class EvaluacionController:
    def __init__(self):
        self.model = EvaluacionModel()
        self.participantes_model = ParticipantesModel()
        self.actividades_model = ActividadesModel()

    def calcular_por_unidad(self, creds, clase, unidad):
        alumnos = self.participantes_model.obtener_alumnos(clase["id_clase"])
        actividades = self.actividades_model.obtener_actividades(unidad["id_unidad"])
    
        resultados = []
    
        for alumno in alumnos:
            total = 0
            detalle = {
                "examen": 0,
                "proyecto": 0,
                "lista": 0,
                "actividades": 0,
                "extra": 0
            }
    
            for tipo in ["examen", "proyecto", "lista", "actividades", "extra"]:
                notas_tipo = []
    
                for act in actividades:
                    tipo_act = str(act["tipo"]).strip().lower()
                    if tipo_act == "actividad":
                        tipo_act = "actividades"
    
                    if tipo_act != tipo:
                        continue
    
                    entregas = self.actividades_model.obtener_entregas(
                        creds,
                        clase["id_google"],
                        act["id_google"]
                    )
    
                    entrega = next(
                        (e for e in entregas if str(e["userId"]) == str(alumno["id_google"])),
                        None
                    )
    
                    if entrega:
                        nota = (
                            entrega.get("assignedGrade")
                            or entrega.get("draftGrade")
                            or entrega.get("calificacion")
                        )
    
                        if nota is not None:
                            try:
                                notas_tipo.append(float(nota))
                            except ValueError:
                                print("IGNORADO (no numérico):", nota)
    
                if notas_tipo:
                    promedio = sum(notas_tipo) / len(notas_tipo)
                    detalle[tipo] = round(promedio, 2)
                    total += promedio
    
            final = round(total, 2)
            self.model.guardar_calificacion_unidad(
                alumno["id_alumno"],
                unidad["id_unidad"],
                final
            )
    
            resultados.append({
                "alumno": alumno["nombre"],
                "examen": detalle["examen"],
                "proyecto": detalle["proyecto"],
                "lista": detalle["lista"],
                "actividades": detalle["actividades"],
                "extra": detalle["extra"],
                "calificacion_final": final,
            })
    
        return resultados
    


class ClasesController:
    def __init__(self):
        self.model = ClasesModel()
        self.actividades_model = ActividadesModel()
        
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
        alumnos = self.participantes_model.obtener_alumnos(id_clase)
        entregas = self.model.obtener_entregas(creds, id_google_clase, coursework_id)
    
        entregados = []
        no_entregados = []
        
    
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

