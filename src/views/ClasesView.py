import flet as ft

def ClasesView(page, clases_controller, unidades_controller):
    
    user = getattr(page, "user_data", None)
    
    titulo = ft.TextField(label="Titulo de la clase", icon=ft.Icons.TITLE)
    descripcion = ft.TextField(label="Descripción de la clase", icon=ft.Icons.DESCRIPTION)
    lista_clases = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)
    
    def agregar():
        if not titulo.value or not descripcion.value:
            page.show_dialog(ft.SnackBar(ft.Text("Por favor, complete todos los campos")))
            return
        
        success, message = clases_controller.agregar_clase(user["id_profesor"], titulo.value, descripcion.value)
        
        page.show_dialog(ft.SnackBar(ft.Text(message)))
        
        if success:
            titulo.value = ""
            descripcion.value = ""
            cargar_clases()
            
    def unidades_click(id_clase):
        unidades_controller.obtener_unidades(id_clase)
        page.go(f"/unidades/{id_clase}")
        
    
    def cargar_clases():
        if user and 'id_profesor' in user:
            lista_clases.controls.clear()
            clases = clases_controller.obtener_clases(user['id_profesor'])
    
            for c in clases:
                lista_clases.controls.append(
                    ft.ElevatedButton(
                        on_click=lambda e, id_clase=c["id_clase"]: unidades_click(id_clase),
                        content=ft.Container(
                            padding=20,
                            width=500,
                            content=ft.Column([
                                ft.Text(c["nombre"], size=24, weight="bold"),
                                ft.Text(c["descripcion"], size=20),
                            ], alignment=ft.MainAxisAlignment.CENTER,)
                        ),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=15),
                            elevation=5
                        )
                    )
                )
    
            page.update()
    
    cargar_clases()
    
    agregar_clase = ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=agregar)
    
    return ft.View(
        route="/clases",
        appbar=ft.AppBar(
            title=ft.Text("Clases"),
            bgcolor=ft.Colors.BLUE_GREY_900,
            color="white",
            actions=[
                    ft.IconButton(ft.Icons.PERSON, on_click=lambda _: page.go("/perfil")),
                    ft.IconButton(ft.Icons.EXIT_TO_APP, on_click=lambda _: page.go("/"))
                ],
        ),
        
        controls=[
            ft.Container(
                ft.Row([titulo, descripcion, agregar_clase], spacing=20),
        ),
            ft.Divider(),
            lista_clases
        ]
    )