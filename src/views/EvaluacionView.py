import flet as ft

def EvaluacionView(page, evaluacion_controller):
    clase_actual = page.user_data.get("clase_actual")
    unidad_actual = page.user_data.get("unidad_actual")
    creds = page.user_data.get("creds")

    if not clase_actual or not unidad_actual:
        page.show_snack_bar(ft.SnackBar(ft.Text("No hay clase o unidad seleccionada"), bgcolor="red"))
        return

    # Llamamos al controller para calcular resultados al vuelo
    resultados = evaluacion_controller.calcular_por_unidad(
        creds,
        clase_actual,
        unidad_actual
    )

    # Construimos tabla de resultados
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Alumno")),
            ft.DataColumn(ft.Text("Calificación Final")),
            ft.DataColumn(ft.Text("Estado")),
        ],
        rows=[
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(r["alumno"])),
                ft.DataCell(ft.Text(str(r["calificacion_final"]))),
                ft.DataCell(ft.Text(
                    r["estado"],
                    color="green" if r["estado"] == "Aprobado" else "red"
                ))
            ]) for r in resultados
        ]
    )

    return ft.View(
        route="/evaluacion",
        appbar=ft.AppBar(
            title=ft.Text("Evaluación"),
            bgcolor=ft.Colors.BLUE_900,
            color="white",
            actions=[
                ft.IconButton(ft.Icons.ARROW_BACK, icon_size=25, on_click=lambda _: page.go("/unidades"), tooltip="Volver a unidades"),
                ft.IconButton(ft.Icons.WEB_STORIES, icon_size=25, on_click=lambda _: page.go("/clases"), tooltip="Volver a clases"),
                ft.IconButton(ft.Icons.PERSON, icon_size=25, on_click=lambda _: page.go("/perfil"), tooltip="Ver perfil"),
            ],
        ),
        controls=[tabla]
    )
