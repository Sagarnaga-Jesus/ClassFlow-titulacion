import flet as ft

def EvaluacionView(page, evaluacion_controller):

    clase_actual = page.user_data.get("clase_actual")
    unidad_actual = page.user_data.get("unidad_actual")
    creds = page.user_data.get("creds")

    if not clase_actual or not unidad_actual:
        page.snack_bar = ft.SnackBar(
            ft.Text("No hay clase o unidad seleccionada"),
            bgcolor=ft.Colors.RED
        )
        page.snack_bar.open = True
        page.update()
        return ft.View(route="/evaluacion")

    resultados = evaluacion_controller.calcular_por_unidad(
        creds,
        clase_actual,
        unidad_actual
    )

    tabla = ft.DataTable(
        border=ft.border.all(1, ft.Colors.GREY_400),
        heading_row_color=ft.Colors.BLUE_100,
        columns=[
            ft.DataColumn(ft.Text("Alumno")),
            ft.DataColumn(ft.Text("Calificación Final")),
            ft.DataColumn(ft.Text("Estado")),
        ],
        rows=[
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(r["alumno"])),

                ft.DataCell(
                    ft.Text(str(r["calificacion_final"]))
                ),

                ft.DataCell(
                    ft.Text(
                        r["estado"],
                        color=ft.Colors.GREEN
                        if r["estado"] == "Aprobado"
                        else ft.Colors.RED
                    )
                ),
            ]) for r in resultados
        ]
    )

    return ft.View(
        route="/evaluacion",
        appbar=ft.AppBar(
            title=ft.Text("Evaluación"),
            bgcolor=ft.Colors.BLUE_900,
            color=ft.Colors.WHITE,
            actions=[
                ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    tooltip="Volver a unidades",
                    on_click=lambda _: page.go("/unidades")
                ),
                ft.IconButton(
                    ft.Icons.WEB_STORIES,
                    tooltip="Clases",
                    on_click=lambda _: page.go("/clases")
                ),
                ft.IconButton(
                    ft.Icons.PERSON,
                    tooltip="Perfil",
                    on_click=lambda _: page.go("/perfil")
                ),
            ],
        ),
        controls=[tabla]
    )