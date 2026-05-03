import flet as ft
from views.LoginView import LoginView
from views.ClasesView import ClasesView
from controllers.UserController import AuthController

def start(page: ft.Page):
    page.title = "Sistema SIGE"
    page.window_width = 450
    page.window_height = 700
    
    # instanciar controladores ua sola
    auth = AuthController()
    
    def route_change(e):
        page.views.clear()
        
        if page.route == "/":
            page.views.append(LoginView(page,auth))
        if page.route == "/clases":
            page.views.append(ClasesView(page,auth))
            
            #agregas aqui las vistas que necesites
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
