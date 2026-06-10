import flet as ft
from views.LoginView import LoginView
from views.ClasesView import ClasesView
from views.UnidadesView import UnidadesView
from views.ActividadesView import ActividadesView
from views.DetallesView import DetallesView
from views.EvaluacionView import EvaluacionView
from views.PerfilView import PerfilView
from views.ParticipantesView import ParticipantesView
from views.AsistenciaView import AsistenciaView
from controllers.AsistenciaController import AsistenciaController
from controllers.ExportarController import ExportarController
from controllers.UserController import AuthController
from controllers.ApartadosController import ClasesController, UnidadesController, ActividadesController, EvaluacionController
from controllers.ParticipantesController import ParticipantesController

def start(page: ft.Page):
    
    page.title = "ClassFlow"
    page.scroll = ft.ScrollMode.AUTO
    page.scroll = ft.ScrollMode.ALWAYS
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.min_width = 390
    page.window.min_height = 700
    
    page.window.width = 1200
    page.window.height = 800
    
    page.window.max_width = 1920
    page.window.max_height = 1080
    
    auth = AuthController()
    clases = ClasesController()
    unidades = UnidadesController()
    participantes = ParticipantesController()
    actividades = ActividadesController()
    evaluacion = EvaluacionController()
    asistencia = AsistenciaController()
    exportar = ExportarController()
    def route_change(e):
        page.views.clear()
        
        if page.route == "/":
            page.views.append(LoginView(page,auth))
        elif page.route == "/clases":
            page.views.append(ClasesView(page, clases))
        elif page.route == "/perfil":
            page.views.append(PerfilView(page))
        elif page.route.startswith("/unidades"):
            page.views.append(UnidadesView(page, unidades, actividades))
        elif page.route.startswith("/evaluacion"):
            page.views.append(EvaluacionView(page, evaluacion, exportar))
        elif page.route == ("/actividad"):
            page.views.append(ActividadesView(page,actividades))
        elif page.route.startswith("/detalles"):
            page.views.append(DetallesView(page,actividades))
        elif page.route == ("/participantes"):
            page.views.append(ParticipantesView(page, participantes, clases))
        elif page.route == ("/asistencia"):
            page.views.append(AsistenciaView(page, asistencia, participantes))

        page.update()

    def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            page.update()
            top_view = page.views[-1]
            page.go(top_view.route)
    
    #Manejos de eventos
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    if page.route == "/":
        route_change(None)
    else:
        page.go("/")
    
def main ():
    ft.app(start)
    
if __name__ == "__main__":
    main()
