import flet as ft
import asyncio

def ActividadesView(page, actividades_controller):
    clase = page.user_data.get("clase_actual")
    
    vista = ft.View(
            route="/actividad",
            appbar=ft.AppBar(
                title=ft.Text(f"Actividades"),
                bgcolor=ft.Colors.BLUE_900,
                color="white",
                actions=[
                    ft.IconButton(ft.Icons.ARROW_BACK,on_click=lambda _: page.go(f"/unidades/{clase.get('id_clase','')}")),
                    ft.IconButton(ft.Icons.GROUPS_3, icon_size=25, on_click=lambda _: page.go("/participantes"), tooltip="Ver participantes"),
                    ft.IconButton(ft.Icons.WEB_STORIES, on_click=lambda _: page.go("/clases"), tooltip="Volver a clases"),
                    ft.IconButton(ft.Icons.PERSON, on_click=lambda _: page.go("/perfil"), tooltip="Ver perfil"),
                ],
            ),
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "Cargando actividades...",
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
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    
    async def cargar_actividades_async():
        await asyncio.sleep(2)
        
        actividad = page.user_data.get("actividades", [])
        unidad = page.user_data.get("unidad_actual")
        if not clase:
            page.show_snack_bar(ft.SnackBar(ft.Text("No hay clase seleccionada"), bgcolor="red"))
            return
    
        lista_actividades = ft.GridView(
            expand=True,
            max_extent=400,
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
            creds = page.user_data["creds"]
            id_google_clase = page.user_data["clase_actual"]["id_google"]
        
            entregas = actividades_controller.obtener_entregas(
                creds,
                id_google_clase,
                actividad["id_google"]
            )
        
            page.user_data["actividad_actual"] = actividad
            page.user_data["entregas"] = entregas
            page.go("/detalles")
            
        def eliminar(c):
            succens,msg=actividades_controller.eliminar_actividades(c)
            if succens:
                cargar_actividades()
                page.show_dialog(ft.SnackBar(ft.Text(msg)))
            else:
                page.show_dialog(ft.SnackBar(ft.Text("Hubo un error al eliminar")))
            
            page.update()
    
    
    
        def cargar_actividades():
            lista_actividades.controls.clear()
            actividades = actividades_controller.obtener_actividades(unidad["id_unidad"])
            for act in actividades:
                lista_actividades.controls.append(
                    ft.Card(
                        content=ft.Container(
                            padding=15,
                            on_click=lambda e, a=act: actividad_click(e, a),
                            expand=True,
                            content=ft.Column([
                                    ft.Row([
                                        ft.Text(act["nombre"], size=22, weight="bold", color=ft.Colors.BLUE_700, expand=True),
                                        ft.IconButton(
                                            ft.Icons.DELETE,
                                            tooltip="Eliminar Actividad",
                                            on_click=lambda e, c=act: eliminar(c)
                                        )
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                    ft.Text(act["descripcion"], size=18, color=ft.Colors.BLUE_GREY_400, expand=True),
                                ], alignment=ft.MainAxisAlignment.START)
                            
                            ),
                        elevation=5,
                        margin=10,
                        shape=ft.RoundedRectangleBorder(radius=12),
                        ),
                        
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
        
    
    
        vista.controls.clear()
        
        vista.controls.extend([
            ft.ResponsiveRow(
                [
                    ft.Column([select_actividad], col={"xs": 12, "sm": 5, "md": 4}),
                    ft.Column([tipo], col={"xs": 12, "sm": 5, "md": 4}),
                    ft.Column([agregar_act], col={"xs": 12, "sm": 2, "md": 2}),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                run_spacing=10,
            ),
            ft.Divider(color="green"),
            lista_actividades
        ])
        

        page.update()
        
    page.run_task(cargar_actividades_async)
    return vista