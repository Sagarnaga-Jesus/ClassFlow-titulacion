from models.AsistenciaModel import AsistenciaModel

class AsistenciaController:

    def __init__(self):
        self.model = AsistenciaModel()

    def guardar_asistencia( self, id_alumno, id_unidad, faltas, asistencias_maximas):
        success = self.model.guardar_asistencia( id_alumno, id_unidad, faltas, asistencias_maximas)
        if success:
            return success, "Asistencia guardada correctamente"
        if not success:
            return success, "Error al guardar la asistencia"

    def obtener_asistencia(self,id_unidad):
        return self.model.obtener_asistencia(id_unidad)