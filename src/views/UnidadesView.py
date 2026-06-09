import flet as ft
import asyncio

def UnidadesView(page, unidades_controller, actividades_controller):
    
    vista = ft.View(
        route="/unidades",
        appbar=ft.AppBar(
            title=ft.Text("Clase"),
            bgcolor=ft.Colors.BLUE_900,
            color=ft.Colors.WHITE,
            actions=[
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
                            "Cargando informacion de las unidades..",
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
    
    unidad_editando = {"data": None}
    
    nombre_edit = ft.TextField(label="Nombre de la unidad")
    examen_edit = ft.TextField(label="Examen", keyboard_type=ft.KeyboardType.NUMBER)
    proyecto_edit = ft.TextField(label="Proyecto", keyboard_type=ft.KeyboardType.NUMBER)
    lista_edit = ft.TextField(label="Lista", keyboard_type=ft.KeyboardType.NUMBER)
    actividades_edit = ft.TextField(label="Actividades", keyboard_type=ft.KeyboardType.NUMBER)
    extra_edit = ft.TextField(label="Extra", keyboard_type=ft.KeyboardType.NUMBER)
    
    dialog_editar = ft.AlertDialog(
        title=ft.Text("Editar unidad"),
        content=ft.Column([
            nombre_edit,
            examen_edit,
            proyecto_edit,
            lista_edit,
            actividades_edit,
            extra_edit
        ], tight=True),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo()),
            ft.ElevatedButton("Guardar", on_click=lambda e: guardar_edicion())
        ]
    )
    page.overlay.append(dialog_editar)
    def cerrar_dialogo():
        dialog_editar.open = False
        page.update()
    
    def guardar_edicion():
        u = unidad_editando["data"]
    
        total = (
            int(examen_edit.value) +
            int(proyecto_edit.value) +
            int(lista_edit.value) +
            int(actividades_edit.value) +
            int(extra_edit.value)
        )
    
        if total != 100:
            page.show_snack_bar(ft.SnackBar(ft.Text("La suma debe ser 100")))
            return

        datos = {
            "nombre": nombre_edit.value,
            "examen": int(examen_edit.value),
            "proyecto": int(proyecto_edit.value),
            "lista": int(lista_edit.value),
            "actividades": int(actividades_edit.value),
            "extra": int(extra_edit.value),
        }
    
        unidades_controller.actualizar_unidad(u["id_unidad"], datos)

        dialog_editar.open = False
        page.update()
        page.run_task(cargar_unidades_vista)
        
    
    def abrir_editar(u):
        unidad_editando["data"] = u
    
        nombre_edit.value = u["nombre"]
        examen_edit.value = str(u["examen"])
        proyecto_edit.value = str(u["proyecto"])
        lista_edit.value = str(u["lista"])
        actividades_edit.value = str(u["actividades"])
        extra_edit.value = str(u["extra"])
    
        dialog_editar.open = True
        page.update()
    
    async def cargar_unidades_vista():
        await asyncio.sleep(1.5)
        clase = page.user_data.get("clase_actual")
        
        if not clase:
            page.show_snack_bar(ft.SnackBar(ft.Text("No hay clase seleccionada"), bgcolor="red"))
            return
            
        nombre = ft.TextField(label="Nombre de la unidad", icon=ft.Icons.TITLE)
        lista_unidades = ft.GridView(expand=True, max_extent=400, child_aspect_ratio=1.2, spacing=20, run_spacing=20)
        
        def actividad_click(unidad):
            creds = page.user_data["creds"]
            id_google = page.user_data["clase_actual"]["id_google"]
        
            actividades = actividades_controller.obtener_google(creds,id_google)
            page.user_data["actividades"]= actividades
            page.user_data["unidad_actual"] = unidad
            page.go("/actividad")
            
        def evaluacion_click(unidad):
            page.user_data["unidad_actual"] = unidad
            page.go("/evaluacion")
            page.update()
        
        def asistencia_click(unidad):
            page.user_data["unidad_actual"] = unidad
            page.go("/asistencia")
    
            
        def eliminar(u):
            id_unidad = u["id_unidad"]
            msg = unidades_controller.elimina(id_unidad)
            if msg:
                cargar_unidades()
                page.show_dialog(ft.SnackBar(ft.Text(msg)))
            else:
                page.show_dialog(ft.SnackBar(ft.Text("Hubo un error al eliminar")))
    
        
        def cargar_unidades():
            lista_unidades.controls.clear()
            unidades = unidades_controller.obtener_unidades(clase['id_clase'])
    
            for u in unidades:
                lista_unidades.controls.append(
                    ft.Card(
                        width=500,
                        height=550,
                        bgcolor=ft.Colors.WHITE,
                        shadow_color=ft.Colors.BLUE_700,
                        elevation=10,
                        expand=True,
                        shape=ft.RoundedRectangleBorder(radius=12),
                        content=ft.Container(
                            padding=10,
                            content=ft.Column([
                                ft.Row([
                                    ft.Column([
                                        ft.Text(u["nombre"], size=18, weight="bold", color="blue")
                                        ]),
                                    
                                    ft.Column([
                                        ft.PopupMenuButton(
                                            items=[
                                                ft.PopupMenuItem(
                                                    content=ft.Text("Editar"),
                                                    on_click=lambda e, u=u: abrir_editar(u)
                                                ),
                                                ft.PopupMenuItem(
                                                    content=ft.Text("Eliminar"),
                                                    on_click=lambda e, u=u: eliminar(u)
                                                ),
                                            ]
                                        )
                                    ], horizontal_alignment=ft.CrossAxisAlignment.END)
                                    
                                    ],alignment=ft.MainAxisAlignment.CENTER,),
                                
                                ft.Text("Valores", size=16, weight="bold", color="green"),
                                ft.Text(f"Actividades: {u["actividades"]}\n Proyecto: {u["proyecto"]} \n Examen: {u["examen"]}\n Asistencia: {u["lista"]}\n Extra: {u["extra"]}", size=14,),
                                
                                
                                ft.TextButton("Inasistencias",icon=ft.Icons.BAR_CHART,style=ft.ButtonStyle(color=ft.Colors.BLUE_700, overlay_color=ft.Colors.BLUE_100),on_click=lambda e, u=u: asistencia_click(u)),
                                ft.TextButton("Ir a Evaluaciones",icon=ft.Icons.BAR_CHART,style=ft.ButtonStyle(color=ft.Colors.BLUE_700, overlay_color=ft.Colors.BLUE_100),on_click=lambda e, u=u: evaluacion_click(u)),
    
    
                                
                                
                            ],alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER,),
                            on_click=lambda e, u=u: actividad_click(u),
                        ),
                    )
                )
    
            page.update()
        
        cargar_unidades()
        
        
        
        def agregar():
            if not nombre.value or not examen.value or not proyecto.value or not actividades.value or not lista.value or not extra.value:
                page.show_dialog(ft.SnackBar(ft.Text("Por favor, complete los campos solicitados")))
                return
            
            try:
                total = int(examen.value) + int(proyecto.value) + int(lista.value) + int(actividades.value) + int(extra.value)
                if total != 100:
                    resultado.value = f"La suma debe ser 100, ahora es {total}"
                    return
                    
            except ValueError:
                resultado.value = "Todos los campos deben ser números"
                return
            
            examen_val = int(examen.value or 0)
            proyecto_val = int(proyecto.value or 0)
            lista_val = int(lista.value or 0)
            actividades_val = int(actividades.value or 0)
            extra_val = int(extra.value or 0)
    
            
            
            success, message = unidades_controller.agregar_unidad(clase['id_clase'], nombre.value, examen_val, proyecto_val, lista_val, actividades_val, extra_val)
            page.show_dialog(ft.SnackBar(ft.Text(message)))
            
            if success:
                nombre.value = ""
                examen.value = ""
                proyecto.value = ""
                lista.value = ""
                actividades.value = ""
                extra.value = ""
                cargar_unidades()
    
        
    
        agregar_unidad = ft.IconButton(ft.Icons.ADD_BOX, expand=True, on_click=agregar, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), icon_size=40, tooltip="Agregar unidad")
        examen = ft.TextField(label="Valor examen", expand=True, keyboard_type=ft.KeyboardType.NUMBER,width=200, height=60)
        proyecto = ft.TextField(label="Valor proyecto", expand=True, keyboard_type=ft.KeyboardType.NUMBER,width=200, height=60)
        lista = ft.TextField(label="Valor lista (asistencia)", expand=True, keyboard_type=ft.KeyboardType.NUMBER,width=200, height=60)
        actividades = ft.TextField(label="Valor actividades", expand=True, keyboard_type=ft.KeyboardType.NUMBER,width=200, height=60)
        extra = ft.TextField(label="Valor extra", expand=True, keyboard_type=ft.KeyboardType.NUMBER,width=200, height=60)
        resultado = ft.Text(value="", color="red")
        
        def evaluacion_click(unidad):
            creds = page.user_data["creds"]
            id_google = page.user_data["clase_actual"]["id_google"]
        
            actividades = actividades_controller.obtener_google(creds,id_google)
            page.user_data["actividades"]= actividades
            page.user_data["unidad_actual"] = unidad
            page.go("/evaluacion")
        
        vista.controls.clear()
        vista.controls.extend([
                ft.Container(
                    expand=True,
                    padding=20,
                    content=ft.Row([
                        ft.Column([
                            ft.Row([
                                ft.Text("Agregar nueva unidad", size=18, weight="bold", color="green"),
                                nombre,agregar_unidad
                                
                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                            resultado,
                            ft.ResponsiveRow([
    ft.Column([actividades], col={"xs": 12, "sm": 6, "md": 4, "lg": 2}),
    ft.Column([proyecto], col={"xs": 12, "sm": 6, "md": 4, "lg": 2}),
    ft.Column([examen], col={"xs": 12, "sm": 6, "md": 4, "lg": 2}),
    ft.Column([lista], col={"xs": 12, "sm": 6, "md": 4, "lg": 2}),
    ft.Column([extra], col={"xs": 12, "sm": 6, "md": 4, "lg": 2}),
])
                                
                        ],alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER,),
                        
                    ], alignment=ft.MainAxisAlignment.CENTER,)
                ),ft.Divider(height=2, thickness=2, color=ft.Colors.GREEN_600),
                lista_unidades
            ]
        )
        page.update()
    
    page.run_task(cargar_unidades_vista)
    return vista