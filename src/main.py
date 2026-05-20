import flet as ft
from views.LoginView import LoginView
from views.ClasesView import ClasesView
from views.UnidadesView import UnidadesView
from views.PerfilView import PerfilView
from views.ParticipantesView import ParticipantesView
from controllers.UserController import AuthController
from controllers.ApartadosController import ClasesController, UnidadesController
from controllers.ParticipantesController import ParticipantesController

def start(page: ft.Page):
    page.title = "ClassFlow"
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 450
    page.window_height = 700
    auth = AuthController()
    clases = ClasesController()
    unidades = UnidadesController()
    participantes = ParticipantesController()
    def route_change(e):
        page.views.clear()
        
        if page.route == "/":
            page.views.append(LoginView(page,auth))
        elif page.route == "/clases":
            page.views.append(ClasesView(page, clases, unidades))
        elif page.route == "/perfil":
            page.views.append(PerfilView(page, unidades,))
        elif page.route.startswith("/unidades"):
            page.views.append(UnidadesView(page, unidades,))
        elif page.route.startswith("/participantes"):
            page.views.append(ParticipantesView(page, participantes, clases))
            
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
