import flet as ft

def UnidadesView(page, unidades_controller, id_clase):

    nombre = ft.TextField(label="Nombre de la unidad", icon=ft.Icons.TITLE)

    lista_unidades = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)

    clase = page.session.get("clase_actual")

    def cargar_unidades():

        lista_unidades.controls.clear()

        unidades = unidades_controller.obtener_unidades(id_clase["id_clase"])

        for u in unidades:

            lista_unidades.controls.append(
                ft.ElevatedButton(
                    content=ft.Container(
                        padding=20,
                        width=250,
                        content=ft.Text(u["nombre"], size=18, weight="bold")
                    ),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=15),
                        elevation=5
                    )
                )
            )

        page.update()

    def agregar():

        if not nombre.value:
            page.show_snack_bar(ft.SnackBar(ft.Text("Completa el nombre")))
            return

        success, message = unidades_controller.agregar_unidad(
            id_clase["id_clase"],
            nombre.value
        )

        page.show_snack_bar(ft.SnackBar(ft.Text(message)))

        if success:
            nombre.value = ""
            cargar_unidades()

    def ver_participantes():

        page.session.set("clase_actual", clase)
        page.go("/participantes")

    cargar_unidades()

    return ft.View(
        route="/unidades",
        appbar=ft.AppBar(
            title=ft.Text("Unidades"),
            bgcolor=ft.Colors.BLUE_GREY_900,
            actions=[
                ft.IconButton(
                    ft.Icons.PEOPLE,
                    on_click=lambda _: ver_participantes()
                )
            ]
        ),
        controls=[
            ft.Row([
                nombre,
                ft.IconButton(ft.Icons.ADD, on_click=lambda _: agregar())
            ]),
            ft.Divider(),
            lista_unidades
        ]
    )