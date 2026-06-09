import flet as ft

def AsistenciaView(page, asistencia_controller, participantes_controller):

    clase = page.user_data.get("clase_actual")
    unidad_actual = page.user_data.get("unidad_actual")

    alumnos = ft.Dropdown(
        label="Selecciona un alumno",
        width=400,
        options=[
            ft.dropdown.Option(
                key=str(p["id_alumno"]),
                text=p["nombre"]
            )
            for p in participantes_controller.obtener_alumnos(
                clase["id_clase"]
            )
        ]
    )

    inasistencia = ft.TextField(label="Número de faltas",width=200,value="0")

    campo_asistencias_maximas = ft.TextField(label="Asistencias máximas",width=200,value="20")

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Alumno")),
            ft.DataColumn(ft.Text("Faltas")),
            ft.DataColumn(ft.Text("Asistencia Máxima")),
        ],
        rows=[]
    )

    def cargar_asistencias():

        resultados = asistencia_controller.obtener_asistencia(
            unidad_actual["id_unidad"]
        )

        tabla.rows.clear()

        for r in resultados:

            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(str(r.get("nombre", "")))
                        ),
                        ft.DataCell(
                            ft.Text(str(r.get("faltas", 0)))
                        ),
                        ft.DataCell(
                            ft.Text(
                                str(
                                    r.get(
                                        "asistencias_maximas",
                                        0
                                    )
                                )
                            )
                        ),
                    ]
                )
            )

        page.update()

    def guardar_asistencia(e):

        if not alumnos.value:

            page.snack_bar = ft.SnackBar(content=ft.Text("Selecciona un alumno"),bgcolor=ft.Colors.RED, color=ft.Colors.WHITE)

            page.snack_bar.open = True
            page.update()
            return

        try:

            id_alumno = int(alumnos.value)
            id_unidad = unidad_actual["id_unidad"]

            faltas = int(inasistencia.value or 0)

            asistencias_maximas = int(campo_asistencias_maximas.value or 0)

            success, message = (asistencia_controller.guardar_asistencia(id_alumno,id_unidad,faltas,asistencias_maximas))

            page.snack_bar = ft.SnackBar(content=ft.Text(message),bgcolor=( ft.Colors.GREEN if success else ft.Colors.RED))

            page.snack_bar.open = True

            if success:
                cargar_asistencias()

            page.update()

        except ValueError:

            page.snack_bar = ft.SnackBar(content=ft.Text("Ingresa valores numéricos válidos"),bgcolor=ft.Colors.RED)

            page.snack_bar.open = True
            page.update()

    guardar_btn = ft.ElevatedButton("Guardar faltas", on_click=guardar_asistencia, width=150, bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE)

    cargar_asistencias()

    return ft.View(
        route="/asistencia",
        appbar=ft.AppBar(
            title=ft.Text("Asistencia"),
            bgcolor=ft.Colors.BLUE_900,
            color="white",
            actions=[
                ft.IconButton(ft.Icons.CLEAR_ALL,on_click=lambda _: page.go(f"/unidades/{clase.get('id_clase', '')}"),tooltip="Volver a unidades"),
                ft.IconButton(ft.Icons.GROUPS_3,icon_size=25,on_click=lambda _: page.go("/participantes"),tooltip="Ver participantes"),
                ft.IconButton(ft.Icons.WEB_STORIES,icon_size=25,on_click=lambda _: page.go("/clases"),tooltip="Volver a clases"),
                ft.IconButton(ft.Icons.PERSON,icon_size=25,on_click=lambda _: page.go("/perfil"),tooltip="Ver perfil"),
            ],
        ),
        controls=[
            ft.Row(
                [
                    alumnos,
                    inasistencia,
                    campo_asistencias_maximas,
                    guardar_btn
                ],
                spacing=20
            ),
            ft.Divider(),
            ft.Row([tabla], alignment=ft.MainAxisAlignment.CENTER)
        ]
    )