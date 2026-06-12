import flet as ft
import asyncio


def ClasesView(page, clases_controller, unidades_controller,actividades_controller,participantes_controller):
    
    vista = ft.View(
        route="/clases",
        appbar=ft.AppBar(
            title=ft.Text("Clases",size=25, weight="bold"),
            bgcolor=ft.Colors.BLUE_900,
            color="white",
            actions=[
                ft.IconButton(ft.Icons.PERSON, on_click=lambda _: page.go("/perfil"), tooltip="Ver perfil",icon_size=30),
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
    
    async def clases_carga():
        await asyncio.sleep(1)
        data = page.user_data
        user = data["usuario"]
        clases = data["clases"]
        
        select_clases = ft.Dropdown(
            label="Selecciona una clase de Classroom",
            width=350,
            options=[
                ft.dropdown.Option(
                    key=c["id"],
                    text=c["name"]
                )
                for c in clases
            ]
        )
        
        lista_clases = ft.GridView(expand=True,max_extent=300,child_aspect_ratio=2,spacing=20,run_spacing=20)
        
        def agregar(e):
            if not select_clases.value:
                page.show_dialog(ft.SnackBar(ft.Text("Selecciona una clase")))
                return
        
            clase = next((c for c in clases if c["id"] == select_clases.value), None)
            if not clase:
                return
        
            success, message = clases_controller.agregar_clase(
                user["id_profesor"],
                clase["id"],
                clase["name"],
                clase.get("section", "")
            )
        
            page.show_dialog(ft.SnackBar(ft.Text(message)))
        
            if success:
                cargar_clases()
        
        def unidades_click(clase):
            page.user_data["clase_actual"] = clase
            page.go("/unidades")
            
        def actividad_click(clase,unidad):
            page.user_data["clase_actual"] = clase
            creds = page.user_data["creds"]
            id_google = page.user_data["clase_actual"]["id_google"]
            
            participantes_controller.obtener_google(creds, id_google)
        
            actividades = actividades_controller.obtener_google(creds,id_google)
            page.user_data["actividades"]= actividades
            page.user_data["unidad_actual"] = unidad
            page.go("/actividad")
            
        def eliminar(c):
            id_clase = c["id_clase"]
            msg=clases_controller.eliminar_clase(id_clase)
            if msg:
                cargar_clases()
                page.show_dialog(ft.SnackBar(ft.Text(msg)))
            page.show_dialog(ft.SnackBar(ft.Text("Hubo un error al eliminar")))
        def cerrar_dialog(dialog):
            dialog.open = False
            page.update()
            
        def mostrar_unidades(c,color):
            unidades = unidades_controller.obtener_unidades(c["id_clase"])
        
            items = [
                ft.ListTile(
                    title=ft.Text(u["nombre"]),
                    bgcolor=color,
                    on_click=lambda e, c=c, u=u: actividad_click(c,u),
                    leading=ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE)
                )
                for u in unidades
            ]
        
            dialog = ft.AlertDialog(
                title=ft.Text(f"Unidades - {c['nombre']}"),
                bgcolor=color,
                
                content=ft.Column(items, tight=True),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialog(dialog))
                ]
            )
        
            page.overlay.append(dialog)
            dialog.open = True
            page.update()
        
            
        colores_tarjetas = [
            "#84ABE0",
            "#81C784",
            "#B39DDB",
            "#ED9AB5",
            "#9DEDE9",
        ]
            
        def cargar_clases():
            if user and 'id_profesor' in user:
                lista_clases.controls.clear()
                clases_bd = clases_controller.obtener_clases(user['id_profesor'])
                
                for c in clases_bd:
                    color = colores_tarjetas[
                        hash(c["id_clase"]) % len(colores_tarjetas)
                    ]
                    lista_clases.controls.append(
                        ft.Card(
                            bgcolor=color,
                            shadow_color=ft.Colors.BLUE_GREY_300,
                            elevation=10,
                            shape=ft.RoundedRectangleBorder(radius=12),
                            content=ft.Container(
                                padding=20,
                                expand=True,
                                on_click=lambda e, c=c: unidades_click(c),
                                content=ft.Column([
                                    ft.Row([
                                        ft.Text(c["nombre"], size=22, weight="bold", color="dark", expand=True),
                                        ft.Column([
                                        ft.PopupMenuButton(
                                            items=[
                                                ft.PopupMenuItem(
                                                    content=ft.Text("Ver unidades"),
                                                    on_click=lambda e, c=c, color=color: mostrar_unidades(c,color),
                                                    expand=True
                                                ),
                                                ft.PopupMenuItem(
                                                    content=ft.Text("Eliminar"),
                                                    on_click=lambda e, c=c: eliminar(c),
                                                    expand=True
                                                ),
                                            ]
                                        )
                                    ], horizontal_alignment=ft.CrossAxisAlignment.END),
                                        
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                    ft.Text(c["descripcion"], weight="bold", expand=True ,size=18, color="dark"),
                                ], alignment=ft.MainAxisAlignment.START)
                            )
                        )
                    )
        
                page.update()
        
        cargar_clases()
        
        agregar_clase = ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            on_click=agregar,
            tooltip="Agregar clase",
            bgcolor=ft.Colors.GREEN,
            foreground_color=ft.Colors.WHITE
        )
        
        
            
                
        vista.controls.clear()

        vista.controls.extend([
            
            ft.Container(
                
                content=ft.Row(
                    
                    [ft.Image(src="src/image/Logo.png",width=150,height=150,),select_clases, agregar_clase],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                )
            ),
            ft.Divider(),
            lista_clases
        ])
        
        page.update()
        
    page.run_task(clases_carga)

    return vista
        
    