from models.ExportarModel import ExportarModel

class ExportarController:

    def __init__(self):
        self.model = ExportarModel()

    def exportar_evaluaciones(self,resultados,nombre_archivo="evaluaciones.xlsx"):
        export=self.model.exportar_excel(resultados,nombre_archivo)
        if export:
            return True, "Archivo descargado exitosamente"
        else:
            return False, "Problemas al descargar el archivo"