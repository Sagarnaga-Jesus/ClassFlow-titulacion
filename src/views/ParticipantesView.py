import flet as ft

def ParticipantesView(page,participantes_controller,clases_controller):
    
    clase = page.user_data.get("clase_actual")

    if not clase:
        page.show_snack_bar(ft.SnackBar(ft.Text("No hay clase seleccionada"), bgcolor="red"))
        return

    lista_participantes = ft.Column(
        scroll=ft.ScrollMode.ALWAYS,
        expand=True
    )

    def cargar_participantes():
        lista_participantes.controls.clear()
    
        id_google = clase["id_google"]
        creds = page.user_data.get("creds")
    
        participantes = participantes_controller.obtener_google(creds, id_google)
    
        for p in participantes:
            lista_participantes.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=15,
                        content=ft.Column([
                            ft.Text(p["nombre"], size=18, weight="bold"),
                            ft.Text(p["email"])
                        ])
                    )
                )
            )
    
        page.update()

    cargar_participantes()

    return ft.View(
        route="/participantes",

        appbar=ft.AppBar(
            title=ft.Text("Participantes"),
            bgcolor=ft.Colors.BLUE_GREY_900,
            color="white",

            actions=[

                ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    on_click=lambda _:
                    page.go(
                        f"/unidades/{clase['id_clase']}"
                    )
                ),

                ft.IconButton(
                    ft.Icons.WEB_STORIES,
                    on_click=lambda _:
                    page.go("/clases")
                )
            ]
        ),

        controls=[
            ft.Text(
                "Participantes de la clase",
                size=24,
                weight="bold"
            ),

            lista_participantes
        ]
    )