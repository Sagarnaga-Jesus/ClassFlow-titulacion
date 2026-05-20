import flet as ft
from controllers.ParticipantesController import ParticipantesController

def UnidadesView(page, unidades_controller):
    
    clase = page.user_data.get("clase_actual")
    
    if not clase:
        page.show_snack_bar(ft.SnackBar(ft.Text("No hay clase seleccionada"), bgcolor="red"))
        return
        
    nombre = ft.TextField(label="Nombre de la unidad", icon=ft.Icons.TITLE)
    lista_unidades = ft.GridView(
    expand=True,
    max_extent=250,   # ancho máximo por tarjeta
    child_aspect_ratio=2,  # proporción ancho/alto
    spacing=20,
    run_spacing=20
    )


    
    def cargar_unidades():
        lista_unidades.controls.clear()
        unidades = unidades_controller.obtener_unidades(clase['id_clase'])

        for u in unidades:
            lista_unidades.controls.append(
                ft.ElevatedButton(
                    content=ft.Container(
                        padding=20,
                        width=250, 
                        content=ft.Column([
                            ft.Text(u["nombre"], size=18, weight="bold"),
                        ])
                    ),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=15),
                        elevation=5
                    )
                )
            )

        page.update()
    
    cargar_unidades()
    
    def agregar():
        if not nombre.value:
            page.show_dialog(ft.SnackBar(ft.Text("Por favor, complete el campo de nombre")))
            return
        
        success, message = unidades_controller.agregar_unidad(clase['id_clase'], nombre.value)
        page.show_dialog(ft.SnackBar(ft.Text(message)))
        
        if success:
            nombre.value = ""
            cargar_unidades()

    agregar_unidad = ft.IconButton(ft.Icons.ADD_BOX, on_click=agregar, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), icon_size=40, tooltip="Agregar unidad")
    
    return ft.View(
        route="/unidades",
        appbar=ft.AppBar(
            title=ft.Text("Clase"),
            bgcolor=ft.Colors.BLUE_GREY_900,
            color="white",
            actions=[
                ft.IconButton(ft.Icons.WEB_STORIES, on_click=lambda _: page.go("/clases"), tooltip="Volver a clases"),
                ft.IconButton(ft.Icons.PERSON, on_click=lambda _: page.go("/perfil"), tooltip="Ver perfil"),
                ft.IconButton(ft.Icons.EXIT_TO_APP, on_click=lambda _: page.go("/"), tooltip="Cerrar sesión")
                ],
        ),
        
        controls=[
            ft.Container(
                padding=20,
                content=ft.Row([
                    ft.Column([
                        ft.Row([
                            ft.Text("Agregar nueva unidad", size=18, weight="bold"),
                            nombre,
                            agregar_unidad
                        ], alignment=ft.MainAxisAlignment.START, spacing=10),
                    ]),
                    ft.Column([
                        ft.Row([
                            ft.Text("Participantes", size=18, weight="bold"),
                            ft.IconButton(ft.Icons.PEOPLE, icon_size=40, on_click=lambda _: page.go("/participantes"), tooltip="Ver participantes")
                            ], alignment=ft.MainAxisAlignment.END, spacing=10),
                    ], alignment=ft.MainAxisAlignment.END,)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ),ft.Divider(height=1, thickness=1, color=ft.Colors.GREY_300),
            ft.Text("Aquí van las unidades de la clase seleccionada"),
            lista_unidades
        ]
    )