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

    loading_view = ft.View(
        route="/evaluacion",
        controls=[
            ft.Column(
                [
                    ft.Text("Calculando calificaciones...", size=20),
                    ft.ProgressRing(width=50, height=50, stroke_width=5),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        ]
    )
    page.go("/evaluacion")
    page.views.append(loading_view)
    page.update()

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
            ft.DataColumn(ft.Text("Examen")),
            ft.DataColumn(ft.Text("Proyecto")),
            ft.DataColumn(ft.Text("Lista")),
            ft.DataColumn(ft.Text("Actividades")),
            ft.DataColumn(ft.Text("Extra")),
            ft.DataColumn(ft.Text("Calificación Final")),
        ],
        rows=[
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(r["alumno"])),
                ft.DataCell(ft.Text(str(r["examen"]))),
                ft.DataCell(ft.Text(str(r["proyecto"]))),
                ft.DataCell(ft.Text(str(r["lista"]))),
                ft.DataCell(ft.Text(str(r["actividades"]))),
                ft.DataCell(ft.Text(str(r["extra"]))),
                ft.DataCell(ft.Text(str(r["calificacion_final"]))),
            ]) for r in resultados
        ]
    )

    return ft.View(
        route="/evaluacion",
        appbar=ft.AppBar(
            title=ft.Text("Evaluación"),
            bgcolor=ft.Colors.BLUE_900,
            color=ft.Colors.WHITE,
        ),
        controls=[
            ft.Container(
                content=ft.Text(
                    f"Clase: {clase_actual['nombre']} - Unidad: {unidad_actual['nombre']}",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),
                padding=10
            ),
            ft.Row(tabla, alignment=ft.MainAxisAlignment.CENTER)
            
            ]
    )
