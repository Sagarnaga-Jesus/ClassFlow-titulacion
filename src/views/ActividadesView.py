import flet as ft
from googleapiclient.discovery import build

def ActividadesView(page, actividades_controller):
    clase = page.user_data.get("clase_actual")
    if not clase:
        page.show_snack_bar(ft.SnackBar(ft.Text("No hay clase seleccionada"), bgcolor="red"))
        return

    lista_actividades = ft.GridView(
        expand=True,
        max_extent=250,
        child_aspect_ratio=2,
        spacing=20,
        run_spacing=20
    )

    def actividad_click(e, actividad):
        page.user_data["actividad_actual"] = actividad
        page.go("/detalle_actividad")

    def cargar_actividades():
        lista_actividades.controls.clear()
        creds = page.user_data["creds"] 
        id_google = clase["id_google"]
        actividades = actividades_controller.obtener_actividades(creds, id_google)
        for act in actividades:
            lista_actividades.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=15,
                        content=ft.Column([
                            ft.Text(act["titulo"], size=18, weight="bold"),
                            ft.Text(act.get("description", "Sin descripción"), size=14, color=ft.Colors.GREY),
                        ]),
                        on_click=lambda e, a=act: actividad_click(e, a)
                    ),
                    elevation=5,
                    margin=10,
                    shape=ft.RoundedRectangleBorder(radius=12),
                )
            )
        page.update()

    cargar_actividades()

    return ft.View(
        route="/actividad",
        appbar=ft.AppBar(
            title=ft.Text(f"Actividades"),
            bgcolor=ft.Colors.BLUE_GREY_900,
            color="white",
            actions=[
                ft.IconButton(ft.Icons.WEB_STORIES, on_click=lambda _: page.go("/clases"), tooltip="Volver a clases"),
                ft.IconButton(ft.Icons.PERSON, on_click=lambda _: page.go("/perfil"), tooltip="Ver perfil"),
            ],
        ),
        controls=[lista_actividades]
    )
