import flet as ft
from googleapiclient.discovery import build

def ActividadesView(page, actividades_controller):
    clase = page.user_data.get("clase_actual")
    actividad = page.user_data.get("actividades", [])
    unidad = page.user_data.get("unidad_actual")
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
    
    select_actividad = ft.Dropdown(
        label="Selecciona la actividad para esta unidad",
        width=400,
        options=[
            ft.dropdown.Option(
                key=a["id_google"],
                text=a["titulo"]
            )
            for a in actividad
        ]
    )
    
    tipo = ft.Dropdown(
        label="Tipo de actividad",
        width=400,
        options=[
            ft.dropdown.Option("Examen"),
            ft.dropdown.Option("Proyecto"),
            ft.dropdown.Option("Actividad"),
            ft.dropdown.Option("Extra"),
        ]
    )
    
    
    
    def agregar(e):
        if not select_actividad.value:
            page.show_dialog(ft.SnackBar(ft.Text("Selecciona una clase")))
            return
    
        actividad_sel = next((a for a in actividad if a["id_google"] == select_actividad.value), None)
        if not actividad:
            return
    
        success, message = actividades_controller.agregar_actividad(
            unidad["id_unidad"],
            actividad_sel["titulo"],
            actividad_sel.get("descripcion", ""),
            tipo.value,
            actividad_sel.get("valor", 0),
            actividad_sel.get("fecha_entrega", None),
            actividad_sel["id_google"]
            )
    
        page.show_dialog(ft.SnackBar(ft.Text(message)))
    
        if success:
            cargar_actividades()

    def actividad_click(e, actividad):
        page.user_data["actividad_actual"] = actividad
        page.go("/detalle_actividad")

    def cargar_actividades():
        lista_actividades.controls.clear()
        actividades = actividades_controller.obtener_actividades(unidad["id_unidad"])
        for act in actividades:
            lista_actividades.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=15,
                        content=ft.Column([
                            ft.Text(act["nombre"], size=18, weight="bold", color="Green"),
                            ft.Text(act.get("descripcion", "Sin descripción"), size=14, color=ft.Colors.GREY),
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
    
    agregar_act = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        on_click=agregar,
        tooltip="Agregar clase",
        bgcolor=ft.Colors.GREEN,
        foreground_color=ft.Colors.WHITE
    )

    return ft.View(
        route="/actividad",
        appbar=ft.AppBar(
            title=ft.Text(f"Actividades"),
            bgcolor=ft.Colors.BLUE_900,
            color="white",
            actions=[
                ft.IconButton(ft.Icons.ARROW_BACK,on_click=lambda _:page.go(f"/unidades/{clase.get("id_clase","")}")),
                ft.IconButton(ft.Icons.WEB_STORIES, on_click=lambda _: page.go("/clases"), tooltip="Volver a clases"),
                ft.IconButton(ft.Icons.PERSON, on_click=lambda _: page.go("/perfil"), tooltip="Ver perfil"),
            ],
        ),
        
        controls=[
            ft.Row([select_actividad,tipo, agregar_act],),
            ft.Divider(color="green")
                ,lista_actividades]
    )
