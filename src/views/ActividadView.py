import flet as ft
from googleapiclient.discovery import build

def ActividadView(page):
    # Obtenemos credenciales y clase actual desde user_data
    credentials = page.user_data.get("credentials")
    clase_actual = page.user_data.get("clase_actual")

    # Construimos servicio de Classroom
    service = build("classroom", "v1", credentials=credentials)
    results = service.courses().courseWork().list(courseId=clase_actual["id"]).execute()
    actividades = results.get("courseWork", [])

    # Dropdown con actividades
    select_actividad = ft.Dropdown(
        label="Selecciona Actividad",
        width=400,
        options=[
            ft.dropdown.Option(key=act["id"], text=act["title"])
            for act in actividades
        ]
    )

    # Lista de actividades como ListTile
    lista_actividades = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)
    for act in actividades:
        lista_actividades.controls.append(
            ft.Card(
                content=ft.Container(
                    padding=15,
                    content=ft.Column([
                        ft.Text(act["title"], size=20, weight="bold", color=ft.colors.BLUE),
                        ft.Text(act.get("description", "Sin descripción"), size=16, color=ft.colors.GREEN),
                        ft.Text(f"Entrega: {act.get('dueDate', 'Sin fecha')}", size=14, color=ft.colors.BLUE_GREY),
                    ])
                ),
                elevation=5,
                margin=10,
                shape=ft.RoundedRectangleBorder(radius=12),
            )
        )

    return ft.View(
        route="/actividad",
        appbar=ft.AppBar(
            title=ft.Text("Actividades"),
            bgcolor=ft.colors.BLUE_GREY_900,
            color="white",
            actions=[
                ft.IconButton(ft.Icons.WEB_STORIES, on_click=lambda _: page.go("/clases"), tooltip="Volver a clases"),
                ft.IconButton(ft.Icons.PERSON, on_click=lambda _: page.go("/perfil"), tooltip="Ver perfil"),
            ],
        ),
        controls=[
            ft.Container(
                ft.Row([select_actividad], spacing=20),
            ),
            ft.Divider(),
            lista_actividades
        ]
    )
