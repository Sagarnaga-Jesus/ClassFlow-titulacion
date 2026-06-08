import flet as ft
import asyncio

def EvaluacionView(page, evaluacion_controller, exportar_controller):

    clase = page.user_data.get("clase_actual")
    unidad_actual = page.user_data.get("unidad_actual")
    creds = page.user_data.get("creds")

    if not clase or not unidad_actual:
        page.snack_bar = ft.SnackBar(
            content=ft.Text("No hay clase o unidad seleccionada"),
            bgcolor=ft.Colors.RED
        )
        page.snack_bar.open = True
        page.update()

        return ft.View(
            route="/evaluacion",
            controls=[ft.Text("No hay datos disponibles")]
        )
        
    
    vista = ft.View(
        route="/evaluacion",
        appbar=ft.AppBar(
            title=ft.Text("Evaluación"),
            bgcolor=ft.Colors.BLUE_900,
            color=ft.Colors.WHITE,
            actions=[
                ft.IconButton(ft.Icons.ARROW_BACK,on_click=lambda _:page.go(f"/unidades/{clase.get("id_clase","")}")),
                ft.IconButton(ft.Icons.GROUPS_3, icon_size=25, on_click=lambda _: page.go("/participantes"), tooltip="Ver participantes"),
                ft.IconButton(ft.Icons.WEB_STORIES, icon_size=25, on_click=lambda _: page.go("/clases"), tooltip="Volver a clases"),
                ft.IconButton(ft.Icons.PERSON, icon_size=25, on_click=lambda _: page.go("/perfil"), tooltip="Ver perfil"),
                ],
        ),
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Procesando información...",
                            size=20,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.ProgressRing(
                            width=50,
                            height=50,
                            stroke_width=5
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                expand=True,
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    async def calcular_y_mostrar():
        try:
            await asyncio.sleep(0.1)

            resultados = await asyncio.to_thread(
                evaluacion_controller.calcular_por_unidad,
                creds,
                clase,
                unidad_actual
            )
            def exportar(e):
                archivo, msg = exportar_controller.exportar_evaluaciones(resultados)
            
                if archivo:
                    page.show_dialog(ft.SnackBar(ft.Text(msg), bgcolor="green"))
                else:
                    page.show_dialog(ft.SnackBar(ft.Text(msg), bgcolor="red"))
        

            tabla = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Alumno")),
                    ft.DataColumn(ft.Text("Examen")),
                    ft.DataColumn(ft.Text("Proyecto")),
                    ft.DataColumn(ft.Text("Actividades")),
                    ft.DataColumn(ft.Text("Extra")),
                    ft.DataColumn(ft.Text("Asistencia")),
                    ft.DataColumn(ft.Text("Final")),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(r.get("alumno", "")))),
                            ft.DataCell(ft.Text(str(r.get("examen", 0)))),
                            ft.DataCell(ft.Text(str(r.get("proyecto", 0)))),
                            ft.DataCell(ft.Text(str(r.get("actividades", 0)))),
                            ft.DataCell(ft.Text(str(r.get("extra", 0)))),
                            ft.DataCell(ft.Text(str(r.get("asistencia", 0)))),
                            ft.DataCell(ft.Text(str(r.get("calificacion_final", 0)))),
                        ]
                    )
                    for r in resultados
                ]
            )

            vista.controls.clear()

            vista.controls.extend([
                ft.Container(
                    content=([ft.Text(
                        f"Clase: {clase['nombre']} - Unidad: {unidad_actual['nombre']}",
                        size=18,
                        weight=ft.FontWeight.BOLD
                    ),ft.ElevatedButton("Exportar a Excel", on_click=exportar, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE),]),
                    padding=10
                ),
                ft.Column(
                    [
                        ft.Row(
                            [tabla, ft.ElevatedButton("Exportar a Excel", on_click=exportar, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE),],
                            scroll=ft.ScrollMode.AUTO
                        )
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True
                )
            ])

            page.update()

        except Exception as e:
            vista.controls.clear()

            vista.controls.append(
                ft.Container(
                    content=ft.Text(
                        f"Error al calcular evaluaciones:\n{str(e)}",
                        color=ft.Colors.RED
                    ),
                    padding=20
                )
            )

            page.update()

    page.run_task(calcular_y_mostrar)

    return vista