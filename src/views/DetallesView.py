import flet as ft

def DetallesView(page, actividades_controller):
    
    
    vista = ft.View(
        route="/detalles",
        appbar=ft.AppBar(
            title=ft.Text("Detalles de la actividad"),
            bgcolor=ft.Colors.BLUE_900,
            color=ft.Colors.WHITE,
            actions=[
                ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/actividad"), tooltip="Volver a actividades"),
                ft.IconButton(ft.Icons.GROUPS_3, icon_size=25, on_click=lambda _: page.go("/participantes"), tooltip="Ver participantes"),
                ft.IconButton(ft.Icons.WEB_STORIES, icon_size=25, on_click=lambda _: page.go("/clases"), tooltip="Volver a clases"),
                ft.IconButton(ft.Icons.PERSON, icon_size=25, on_click=lambda _: page.go("/perfil"), tooltip="Ver perfil"),
                ],
        ),
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Procesando información...",
                            size=20,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.ProgressRing(
                            width=50,
                            height=50,
                            stroke_width=5
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                expand=True,
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    
    def recargar(e=None):
        page.run_task(cargar_detalles)
    
    async def cargar_detalles():
        
    
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
    
        detalle = ft.Row([
            ft.Column([
                ft.Text(actividad["nombre"], size=25, weight="bold"),]),
            ft.Column([
                ft.Text(actividad.get("descripcion", "Sin descripción"), size=16),
                ]),
            ft.Column([ft.Text(f"Valor: {actividad.get('valor', 'N/A')}"),
                ]),
            ft.Column([ft.Text(f"Fecha entrega: {actividad.get('fecha_entrega', 'N/A')}"),
                ]),
            ft.Column([ft.IconButton(icon=ft.Icons.REFRESH,tooltip="Actualizar",icon_size=30,on_click=lambda e: recargar(),icon_color=ft.Colors.GREEN),
            ]),
        ],alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        
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
        
        
        
    
        vista.controls.clear()
        
        vista.controls.extend([
                detalle,
                lista_entregados,
                lista_no_entregados
                
            ])

        page.update()
        
    page.run_task(cargar_detalles)
    return vista