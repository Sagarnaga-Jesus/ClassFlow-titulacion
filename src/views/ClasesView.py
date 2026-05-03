import flet as ft

def ClasesView(page: ft.Page, auth_controller):
    return ft.View(
        route="/clases",
        vertical_alignment=ft.MainAxisAlignment.CENTER, 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        appbar=ft.AppBar(
            title=ft.Text("Clases"),
            bgcolor=ft.Colors.BLUE_GREY_900,
            color="white"
        ),
        controls=[
            ft.Text("Bienvenido a la sección de clases")
        ]
    )
     