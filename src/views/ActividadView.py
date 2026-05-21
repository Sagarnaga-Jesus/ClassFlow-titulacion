import flet as ft

def ActividadView(page):
    
    select_actividad = ft.Dropdown(
        label="Selecciona Actividad",
        width=400,
        options=[
            ft.dropdown.Option(
            )
        ]
    )
    
    
    
    return ft.view(
        route="/actividad",
        appbar=ft.AppBar(
            title=ft.Text("Clase"),
            bgcolor=ft.Colors.BLUE_GREY_900,
            color="white",
            actions=[
                ft.IconButton(ft.Icons.WEB_STORIES, on_click=lambda _: page.go("/clases"), tooltip="Volver a clases"),
                ft.IconButton(ft.Icons.PERSON, on_click=lambda _: page.go("/perfil"), tooltip="Ver perfil"),
                ],
        ),
        
        controls=[
            ft.Container(
                ft.Row([select_actividad, ], spacing=20),
            ),
            ft.Divider(),
        ]
    )