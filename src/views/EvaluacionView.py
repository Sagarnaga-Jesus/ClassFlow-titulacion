import flet as ft
from controllers.ApartadosController import EvaluacionController

def EvaluacionView(page, alumnos, id_unidad):
    controller = EvaluacionController()

    # 👉 AppBar
    appbar = ft.AppBar(
        title=ft.Text("Evaluación de Alumnos"),
        bgcolor=ft.Colors.BLUE_900,
        color="white",
        actions=[
            ft.IconButton(ft.Icons.ARROW_BACK,on_click=lambda _:page.go(f"/unidades/{id_unidad}")),
            ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/clases")),
            ft.IconButton(ft.Icons.PERSON, on_click=lambda _: page.go("/perfil")),
        ],
    )

    # 👉 Construir filas dinámicas
    rows = []
    aprobados = 0
    reprobados = 0
    suma_totales = 0

    for alumno in alumnos:
        resultado = controller.calcular_evaluacion(id_unidad, alumno["id_alumno"])
        total = resultado["total"]
        suma_totales += total
        if total >= 70:
            aprobados += 1
        else:
            reprobados += 1

        rows.append(
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(alumno["nombre"])),
                ft.DataCell(ft.Text(str(resultado.get("examen",0)))),
                ft.DataCell(ft.Text(str(resultado.get("proyecto",0)))),
                ft.DataCell(ft.Text(str(resultado.get("actividad",0)))),
                ft.DataCell(ft.Text(f"{total}", color="green" if total>=70 else "red")),
            ])
        )

    promedio = round(suma_totales / len(alumnos), 2) if alumnos else 0

    # 👉 Tarjetas resumen
    resumen = ft.Row(
        controls=[
            ft.Card(content=ft.Container(bgcolor=ft.Colors.BLUE_200,padding=10,
                content=ft.Column([ft.Text("Promedio General", weight="bold"), ft.Text(str(promedio), size=20, weight="bold")]))),
            ft.Card(content=ft.Container(bgcolor=ft.Colors.GREEN_200,padding=10,
                content=ft.Column([ft.Text("Aprobados", weight="bold"), ft.Text(str(aprobados), size=20, weight="bold")]))),
            ft.Card(content=ft.Container(bgcolor=ft.Colors.RED_200,padding=10,
                content=ft.Column([ft.Text("Reprobados", weight="bold"), ft.Text(str(reprobados), size=20, weight="bold")]))),
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND
    )

    # 👉 Tabla
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Alumno")),
            ft.DataColumn(ft.Text("Examen")),
            ft.DataColumn(ft.Text("Proyecto")),
            ft.DataColumn(ft.Text("Actividades")),
            ft.DataColumn(ft.Text("Total")),
        ],
        rows=rows
    )

    return ft.View(route="/evaluacion", appbar=appbar, controls=[resumen, tabla])
