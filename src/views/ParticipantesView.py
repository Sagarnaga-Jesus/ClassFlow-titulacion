import flet as ft

def ParticipantesView(page, participantes_controller,id_clase):
    
    nombre_participante = ft.TextField(label="Nombre del participante", icon=ft.Icons.PERSON)

    
    participantes = participantes_controller.obtener(id_clase["id_clase"])
    
    lista_participantes = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)
    
    for p in participantes:
        lista_participantes.controls.append(
            ft.Text(p["nombre"], size=18)
        )
    
    """def agregar_participante():
        if not nombre_participante.value:
            page.show_dialog(ft.SnackBar(ft.Text("Por favor, complete el campo de nombre")))
            return"""
        
        # Aquí deberías llamar a un método del controlador para agregar el participante a la clase
        # Por ejemplo: success, message = participantes_controller.agregar_participante(id_clase, nombre_participante.value)
        # Luego mostrar el mensaje y recargar la lista de participantes si fue exitoso
    
    def unidades_click(id_clase):
        page.go(f"/unidades/{id_clase}")
    
    return ft.View(
        route="/participantes",
        appbar=ft.AppBar(
            title=ft.Text("Participantes"),
            bgcolor=ft.Colors.BLUE_GREY_900,
            color="white",
            actions=[
                ft.IconButton(ft.Icons.WEB_STORIES, on_click=unidades_click(id_clase), tooltip="Volver a clase"),
                ft.IconButton(ft.Icons.WEB_STORIES, on_click=lambda _: page.go("/clases"), tooltip="Volver a clases"),
                ft.IconButton(ft.Icons.PERSON, on_click=lambda _: page.go("/perfil"), tooltip="Ver perfil"),
            ]
        ),
        
        controls=[
            ft.Row([
                nombre_participante,
                ft.IconButton(ft.Icons.ADD, on_click="", tooltip="Agregar participante")
            ], alignment=ft.MainAxisAlignment.CENTER),
            ##lista_participantes
        ]
    )