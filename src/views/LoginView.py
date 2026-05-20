import flet as ft
#from views.RegistroView import RegistroView
from googleapiclient.discovery import build
from datetime import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
import requests


def LoginView(page: ft.Page, auth_controller):

    
    def login_google():
        flow = InstalledAppFlow.from_client_secrets_file(
            "src/client_secret_936016113208-e3k9m1dpclpiq3kndf4h92d31a78r9uk.apps.googleusercontent.com.json",
            scopes=[
                "openid",
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
                "https://www.googleapis.com/auth/classroom.courses.readonly",
                "https://www.googleapis.com/auth/classroom.rosters.readonly",
                "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly",
                "https://www.googleapis.com/auth/classroom.student-submissions.me.readonly"
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
    
    def get_classroom_courses(creds):

        service = build(
            "classroom",
            "v1",
            credentials=creds
        )
    
        results = service.courses().list().execute()

        return results.get("courses", [])
    
    def login_google_click(e):
    
        creds = login_google()
        user_info = get_user_info(creds)
        courses = get_classroom_courses(creds)
    
        for c in courses:
            print(c["name"])
        
        user, msg = auth_controller.login_google(
            user_info.get("name"),
            user_info.get("email"),
            user_info.get("picture")
        )

        page.user_data = {
            "usuario": user,
            "clases": courses,
            "creds": creds
        }
        page.go("/clases")

    appbar_color = ft.Colors.BLUE_500
    button_color = ft.Colors.GREEN
    
    google_btn = ft.ElevatedButton(
        content=ft.Row([
            ft.Icon(ft.Icons.LOGIN),
            ft.Text("Autorización con Google")
        ], alignment=ft.MainAxisAlignment.CENTER),
        width=250,
        bgcolor=button_color,
        color=ft.Colors.WHITE,
        on_click=login_google_click
    )

    return ft.View(
        route="/",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        appbar=ft.AppBar(
            title=ft.Text("Login"),
            bgcolor=appbar_color,
            color="white"
        ),
        controls=[
            ft.Card(
                bgcolor=ft.Colors.WHITE,
                shadow_color=ft.Colors.BLUE_600,
                elevation=24,
                shape=ft.RoundedRectangleBorder(radius=15),
                content=ft.Container(
                    border=ft.border.all(2, ft.Colors.BLUE),   # borde azul
                    border_radius=15,
                    padding=20,
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.LOCK_PERSON, size=50, color=button_color),
                            ft.Text("Sistema ClassFlow", size=24, weight="bold"),
                            google_btn,
                            ft.Text(
                                "Nota: Este sistema solo acepta inicios de sesión con Google",
                                size=14,
                                weight="bold"
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                        tight=True
                    )
                )
            )
        ]
    )
