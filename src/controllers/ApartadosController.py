from models.ApartadosModel import ClasesModel, UnidadesModel, ActividadesModel, EvaluacionModel
from models.ParticipantesModel import ParticipantesModel
from models.AsistenciaModel import AsistenciaModel

class EvaluacionController:
    def __init__(self):
        self.model = EvaluacionModel()
        self.participantes_model = ParticipantesModel()
        self.actividades_model = ActividadesModel()
        self.asistencia_model = AsistenciaModel()

    def calcular_por_unidad(self, creds, clase, unidad):
    
        alumnos = self.participantes_model.obtener_alumnos(clase["id_clase"])
        actividades = self.actividades_model.obtener_actividades(unidad["id_unidad"])
        asistencias = self.asistencia_model.obtener_asistencia(unidad["id_unidad"])
    
        resultados = []
        for alumno in alumnos:
    
            detalle = {
                "examen": {"obtenido": 0, "posible": 0},
                "proyecto": {"obtenido": 0, "posible": 0},
                "actividades": {"obtenido": 0, "posible": 0},
                "extra": {"obtenido": 0, "posible": 0},
            }
    
            for act in actividades:
                tipo_act = str(act.get("tipo", "")).strip().lower()
    
                if tipo_act == "actividad":
                    tipo_act = "actividades"
    
                if tipo_act not in detalle:
                    continue
    
                try:
                    valor_maximo = float(act.get("valor") or 0)
                except (ValueError, TypeError):
                    valor_maximo = 0
    
                entregas = self.actividades_model.obtener_entregas(
                    creds,
                    clase["id_google"],
                    act["id_google"]
                ) or []
    
                entrega = next(
                    (
                        e for e in entregas
                        if str(e.get("userId"))
                        == str(alumno["id_google"])
                    ),
                    None
                )
    
                nota_alumno = 0
    
                if entrega:
    
                    nota = (
                        entrega.get("assignedGrade")
                        or entrega.get("draftGrade")
                        or entrega.get("calificacion")
                        or 0
                    )
    
                    try:
                        nota_alumno = float(nota)
                    except (ValueError, TypeError):
                        nota_alumno = 0
    
                detalle[tipo_act]["obtenido"] += nota_alumno
                detalle[tipo_act]["posible"] += valor_maximo
    
            porcentajes = {}
    
            for tipo, datos in detalle.items():
    
                if datos["posible"] > 0:
    
                    porcentajes[tipo] = round(
                        (
                            datos["obtenido"]
                            / datos["posible"]
                        ) * 100,
                        2
                    )
    
                else:
                    porcentajes[tipo] = 0
    
            porcentaje_asistencia = 0
            
            
    
            registro_asistencia = next(
                (
                    a for a in asistencias
                    if str(a["id_alumno"])
                    == str(alumno["id_alumno"])
                ),
                None
            )
    
            if registro_asistencia:
    
                faltas = int(registro_asistencia.get("faltas",0))
    
                asistencias_maximas = int(registro_asistencia.get("asistencias_maximas",0))
    
                if asistencias_maximas > 0:
    
                    porcentaje_asistencia = ((asistencias_maximas- faltas)/ asistencias_maximas) * 100
    
            porcentaje_asistencia = round(porcentaje_asistencia,2)
    
            calificacion_final = (
                (porcentajes["examen"] * unidad["examen"] / 100)
                +
                (porcentajes["proyecto"] * unidad["proyecto"] / 100)
                +
                (porcentaje_asistencia * unidad["lista"] / 100)
                +
                (porcentajes["actividades"] * unidad["actividades"] / 100)
                +
                (porcentajes["extra"] * unidad["extra"] / 100)
            )
    
            calificacion_final = round(calificacion_final,2)
    
            self.model.guardar_calificacion_unidad(alumno["id_alumno"],unidad["id_unidad"],calificacion_final)
    
            resultados.append({
                "alumno": alumno["nombre"],
                "examen": round(porcentajes["examen"] * unidad["examen"] / 100, 2),
                "proyecto": round(porcentajes["proyecto"] * unidad["proyecto"] / 100, 2),
                "actividades": round(porcentajes["actividades"] * unidad["actividades"] / 100, 2),
                "extra": round(porcentajes["extra"] * unidad["extra"] / 100, 2),
                "asistencia": round(porcentaje_asistencia * unidad["lista"] / 100, 2),
                "calificacion_final": calificacion_final
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
    
    def actualizar_unidad(self, id_unidad, datos):

        try:
            # Validación básica
            campos_obligatorios = ["nombre", "examen", "proyecto", "lista", "actividades", "extra"]
    
            for c in campos_obligatorios:
                if c not in datos or datos[c] == "":
                    return False, f"Falta el campo {c}"
    
            # Validar suma 100
            total = (
                int(datos["examen"]) +
                int(datos["proyecto"]) +
                int(datos["lista"]) +
                int(datos["actividades"]) +
                int(datos["extra"])
            )
    
            if total != 100:
                return False, f"La suma debe ser 100, actualmente es {total}"
    
            # Llamar al model
            success, msg = self.model.actualizar_unidad(id_unidad, datos)
    
            if success:
                return True, msg
    
            return False, "Error al actualizar unidad"
    
        except Exception as e:
            return False, str(e)
    

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
    
    def eliminar_actividades(self, actividad):
        
        eliminar=self.model.eliminar_actividad( actividad)
        
        if eliminar:
            return True, "Eliminada Correcta"
        else:
            return False, "Fallo en eliminar actividad"
        

