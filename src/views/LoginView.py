import flet as ft
#from views.RegistroView import RegistroView
from datetime import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
import requests


def LoginView(page: ft.Page, auth_controller):
    
    def ver_contra():
        contra.password = not contra.password
        contra.update()
        
    correo=(ft.TextField(label="Correo",autofocus=True, icon=ft.Icons.PERSON ))
    contra=(ft.TextField(label="Contraseña",suffix=ft.IconButton(icon=ft.Icons.VISIBILITY, on_click=ver_contra) ,password=True, autofocus=True, icon=ft.Icons.PASSWORD))
    
    
    
    def login_click(e):
        if not correo.value or not contra.value:
            page.show_dialog(ft.SnackBar(ft.Text("Por favor, complete todos los campos")))
            return
        
    
        user, msg = auth_controller.login(correo.value, contra.value)
    
        if user:
            page.user_data = user
            page.go("/clases")
        else:
            page.show_dialog(ft.SnackBar(ft.Text(msg)))
            
    def olvidado():
        page.show_dialog(ft.SnackBar(ft.Text("Se a enviado su contraseña al correo")))
    
    def registro():
        page.go("/registro")
    
    def login_google():
        flow = InstalledAppFlow.from_client_secrets_file(
            "src/client_secret_936016113208-e3k9m1dpclpiq3kndf4h92d31a78r9uk.apps.googleusercontent.com.json",
            scopes=[
                "openid",
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile"
            ]
        )
        creds = flow.run_local_server(port=0)
        return creds

    def get_user_info(creds):
        r = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {creds.token}"}
        )
        return r.json()
    
    def login_google_click(e):
        creds = login_google()
        user_info = get_user_info(creds)
    
        # Aquí puedes guardar o verificar en tu BD
        user = {
            "nombre": user_info.get("name"),
            "correo": user_info.get("email")
        }
    
        page.user_data = user
        page.go("/clases")
    
    google_btn = ft.ElevatedButton(
                                    "Iniciar sesión con Google",
                                    icon=ft.Icons.LOGIN,
                                    bgcolor=ft.Colors.RED_400,
                                    color=ft.Colors.WHITE,
                                    on_click=login_google_click
                                    )
    iniciar=( ft.Button("Iniciar sesion",color=ft.Colors.WHITE ,bgcolor=ft.Colors.BLUE,on_click=login_click))
    registrarse =( ft.TextButton("¿Quieres registrarte?", on_click=registro))
    olvidada =( ft.TextButton("¿Olvidaste la contraseña?", on_click=olvidado))
    
    return ft.View(
        route="/",
        vertical_alignment=ft.MainAxisAlignment.CENTER, 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        appbar=ft.AppBar(
            title=ft.Text("Login"),
            bgcolor=ft.Colors.BLUE_GREY_900,
            color="white"
        ),
        controls=[
            ft.Column(
                [
                    ft.Icon(ft.Icons.LOCK_PERSON, size=50, color=ft.Colors.BLUE),
                    ft.Text("Acceso al sistema", size=24, weight="bold"),
                    correo,
                    contra,
                    iniciar,
                    google_btn,
                    registrarse,
                    olvidada
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                tight=True 
            )
        ]
    )
    