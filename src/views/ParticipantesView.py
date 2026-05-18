import flet as ft

def ParticipantesView(page, participantes_controller):

    lista_participantes = ft.Column(
        scroll=ft.ScrollMode.ALWAYS,
        expand=True
    )

    def cargar_participantes():

        lista_participantes.controls.clear()

        clase = page.session.get("clase_actual")

        if not clase:
            page.show_snack_bar(ft.SnackBar(ft.Text("No hay clase seleccionada")))
            return

        participantes = participantes_controller.obtener_google(
            page.user_data["creds"],
            clase["id"]   # 👈 Google Classroom ID
        )

        for p in participantes:

            perfil = p["profile"]

            lista_participantes.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=15,
                        content=ft.Column([
                            ft.Text(
                                perfil["name"]["fullName"],
                                size=18,
                                weight="bold"
                            ),
                            ft.Text(perfil.get("emailAddress", ""))
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
            actions=[
                ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/unidades")
                )
            ]
        ),
        controls=[
            ft.Text("Participantes de la clase", size=24, weight="bold"),
            lista_participantes
        ]
    )