import flet as ft

def DetallesView(page, actividades_controller):
    unidad = page.user_data.get("unidad_actual")
    
    actividad = page.user_data.get("actividad_actual")

    if not actividad:
        page.show_snack_bar(ft.SnackBar(ft.Text("No hay actividad seleccionada"), bgcolor="red"))
        return

    creds = page.user_data["creds"]
    id_clase = page.user_data["clase_actual"]["id_clase"]
    id_google_clase = page.user_data["clase_actual"]["id_google"]

    entregados, no_entregados = actividades_controller.obtener_entregas_por_actividad(
        creds, id_clase, id_google_clase, actividad["id_google"]
    )

    detalle = ft.Column([
        ft.Text(actividad["nombre"], size=22, weight="bold"),
        ft.Text(actividad.get("descripcion", "Sin descripción"), size=16),
        ft.Text(f"Valor: {actividad.get('valor', 'N/A')}"),
        ft.Text(f"Fecha entrega: {actividad.get('fecha_entrega', 'N/A')}")
    ], spacing=10)
    
    num_entregados = len(entregados)
    
    num_noentre = len(no_entregados)

    lista_entregados = ft.ExpansionTile(
        title=ft.Text(f"Entregaron:  {num_entregados}"),
        controls=[ft.ListTile(title=ft.Text(a["nombre"]), subtitle=ft.Text(a["correo"])) for a in entregados]
    )

    lista_no_entregados = ft.ExpansionTile(
        title=ft.Text(f"No entregaron:  {num_noentre}"),
        controls=[ft.ListTile(title=ft.Text(a["nombre"]), subtitle=ft.Text(a["correo"])) for a in no_entregados]
    )

    return ft.View(
        route="/detalles",
        appbar=ft.AppBar(
            title=ft.Text("Detalle de actividad"),
            bgcolor=ft.Colors.BLUE_900,
            color="white",
            actions=[
                ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/actividad"), tooltip="Volver a actividades"),
                ft.IconButton(ft.Icons.WEB_STORIES, icon_size=25, on_click=lambda _: page.go("/clases"), tooltip="Volver a clases"),
                ft.IconButton(ft.Icons.PERSON, on_click=lambda _: page.go("/perfil"), tooltip="Ver perfil"),
            ],
        ),
        controls=[detalle, lista_entregados, lista_no_entregados]
    )
