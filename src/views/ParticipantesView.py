import flet as ft

def ParticipantesView(page,participantes_controller,clases_controller,id_clase):

    lista_participantes = ft.Column(
        scroll=ft.ScrollMode.ALWAYS,
        expand=True
    )

    def cargar_participantes():

        lista_participantes.controls.clear()

        clase = clases_controller.obtener_clase(
            id_clase["id_clase"]
        )

        participantes = participantes_controller.obtener_google(
            page.user_data["creds"],
            clase["id_google"]
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

                            ft.Text(
                                perfil.get(
                                    "emailAddress",
                                    ""
                                )
                            )

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
                        f"/unidades/{id_clase['id_clase']}"
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