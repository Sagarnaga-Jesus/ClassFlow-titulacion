import flet as ft

def UnidadesView(page: ft.Page, auth_controller):
    return ft.View(
        route="/unidades",
        appbar=ft.AppBar(
            title=ft.Text("Unidades"),
            bgcolor=ft.Colors.BLUE_GREY_900,
            color="white",
            actions=[
                    ft.IconButton(ft.Icons.PERSON, on_click=lambda _: page.go("/perfil")),
                    ft.IconButton(ft.Icons.EXIT_TO_APP, on_click=lambda _: page.go("/"))
                ],
        ),
        
        controls=[
            ft.Text("Aquí van las unidades de la clase seleccionada"),
        ]
    )