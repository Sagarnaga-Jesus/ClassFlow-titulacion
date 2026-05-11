import flet as ft

def UnidadesView(page: ft.Page, unidades_controller, id_clase):
        
    nombre = ft.TextField(label="Nombre de la unidad", icon=ft.Icons.TITLE)
    lista_unidades = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)
    
    def cargar_unidades():
        if id_clase and 'id_clase' in id_clase:
            lista_unidades.controls.clear()
            unidades = unidades_controller.obtener_unidades(id_clase['id_clase'])
    
            for u in unidades:
                lista_unidades.controls.append(
                    ft.ElevatedButton(
                        on_click=cargar_unidades,
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
        
        success, message = unidades_controller.agregar_unidad(id_clase['id_clase'], nombre.value)
        page.show_dialog(ft.SnackBar(ft.Text(message)))
        
        if success:
            nombre.value = ""
            cargar_unidades()
    
    agregar_unidad = ft.Button("Agregar unidad", on_click=agregar)
    
    return ft.View(
        route="/unidades",
        appbar=ft.AppBar(
            title=ft.Text("Unidades"),
            bgcolor=ft.Colors.BLUE_GREY_900,
            color="white",
            actions=[
                ft.IconButton(ft.Icons.WEB_STORIES, on_click=lambda _: page.go("/clases")),
                    ft.IconButton(ft.Icons.PERSON, on_click=lambda _: page.go("/perfil")),
                    ft.IconButton(ft.Icons.EXIT_TO_APP, on_click=lambda _: page.go("/"))
                ],
        ),
        
        controls=[
            ft.Container(
                padding=20,
                content=ft.Column([
                    ft.Text("Agregar nueva unidad", size=18, weight="bold"),
                    nombre,
                    agregar_unidad
                ])
            ),
            ft.Text("Aquí van las unidades de la clase seleccionada"),
            lista_unidades
        ]
    )