import flet as ft

def ClasesView(page, clases_controller, unidades_controller):

    data = page.user_data
    user = data["usuario"]

    clases = data["clases"]

    select_clases = ft.Dropdown(
        label="Selecciona una clase de Classroom",
        width=400,
        options=[
            ft.dropdown.Option(
                key=c["id"],
                text=c["name"]
            )
            for c in clases
        ]
    )

    lista_clases = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)

    def agregar(e):

        if not select_clases.value:
            page.show_snack_bar(ft.SnackBar(ft.Text("Selecciona una clase")))
            return

        clase = next(
            (c for c in clases if c["id"] == select_clases.value),
            None
        )

        if not clase:
            return

        success, message = clases_controller.agregar_clase(
            user["id_profesor"],
            clase["id"],
            clase["name"],
            clase.get("section", "")
        )

        page.show_snack_bar(ft.SnackBar(ft.Text(message)))

        if success:
            cargar_clases()

    def unidades_click(clase):
        page.session.set("clase_actual", clase)
        page.go(f"/unidades/{clase['id_clase']}")

    def cargar_clases():

        lista_clases.controls.clear()

        clases_db = clases_controller.obtener_clases(user['id_profesor'])

        for c in clases_db:

            lista_clases.controls.append(
                ft.ElevatedButton(
                    on_click=lambda e, c=c: unidades_click(c),
                    content=ft.Container(
                        padding=20,
                        width=500,
                        content=ft.Column([
                            ft.Text(c["nombre"], size=24, weight="bold"),
                            ft.Text(c["descripcion"], size=20),
                        ])
                    ),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=15),
                        elevation=5
                    )
                )
            )

        page.update()

    cargar_clases()

    return ft.View(
        route="/clases",
        appbar=ft.AppBar(
            title=ft.Text("Clases"),
            bgcolor=ft.Colors.BLUE_GREY_900,
            color="white",
            actions=[
                ft.IconButton(ft.Icons.PERSON, on_click=lambda _: page.go("/perfil")),
                ft.IconButton(ft.Icons.EXIT_TO_APP, on_click=lambda _: page.go("/")),
            ],
        ),
        controls=[
            ft.Row([select_clases], spacing=20),
            ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=agregar),
            ft.Divider(),
            lista_clases
        ]
    )