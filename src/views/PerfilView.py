import flet as ft

def PerfilView(page):

    page.title = "Perfil"
    clase = page.user_data.get("clase_actual")
    user = page.user_data.get("usuario", {})

    nombre = user.get("nombre", "Usuario")
    correo = user.get("correo", "")
    imagen = user.get("foto", "")

    foto = ft.CircleAvatar(foreground_image_src=imagen,radius=60)

    return ft.View(
        route="/perfil",

        bgcolor=ft.Colors.BLUE_GREY_50,

        appbar=ft.AppBar(
            title=ft.Text("Mi Perfil",size=20, weight="bold"),

            bgcolor=ft.Colors.BLUE_900,
            color="white",

            actions=[
                ft.IconButton(ft.Icons.CLEAR_ALL,on_click=lambda _: page.go(f"/unidades/{clase.get('id_clase', '')}"),tooltip="Volver a unidades", icon_size=30),
                ft.IconButton(ft.Icons.WEB_STORIES,on_click=lambda _: page.go("/clases"),tooltip="Volver a clases", icon_size=30),
            ]
        ),

        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,

        controls=[

            ft.Container(
                alignment=ft.Alignment(0, 0),

                content=ft.Card(
                    elevation=15,
                    shape=ft.RoundedRectangleBorder(radius=20),

                    content=ft.Container(
                        width=400,
                        padding=30,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20,
                            controls=[

                                foto,

                                ft.Text(nombre,size=28,weight="bold",color=ft.Colors.BLUE_900),

                                ft.Container(
                                    padding=15,border_radius=15,bgcolor=ft.Colors.BLUE_GREY_100,
                                    content=ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.Icon(ft.Icons.EMAIL,color=ft.Colors.BLUE_700),
                                            ft.Text(correo,size=18)
                                        ]
                                    )
                                ),
                                ft.Divider(),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=15,
                                    controls=[
                                        ft.ElevatedButton("Cerrar sesión",icon=ft.Icons.LOGOUT,style=ft.ButtonStyle(bgcolor=ft.Colors.RED_400,color="white",shape=ft.RoundedRectangleBorder(radius=12),padding=20),on_click=lambda _: page.go("/"))
                                    ]
                                )
                            ]
                        )
                    )
                )
            )
        ]
    )