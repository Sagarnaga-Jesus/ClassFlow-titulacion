import flet as ft
import requests, random, smtplib
from email.mime.text import MIMEText

def OlvidadoView(page, auth_controller):  
        
    correo= ft.TextField(label="Correo",autofocus=True, icon=ft.Icons.PERSON, width=400 )
    txt_codigo = ft.TextField(label="Código",visible=False)
    
    
    def enviar_codigo(e):
        
        if not correo.value:
            page.show_dialog(ft.SnackBar(ft.Text("Por favor ingrese el correo"),bgcolor="red"))
            return
        
        existe, msg = auth_controller.existe(correo.value)
        
        if existe:
            codigo = random.randint(100000,999999)
            page.codigo = codigo
            remitente = "23308060610335@cetis61.edu.mx"
            password = "kraf vtjr arsu gcxz"
            correo.value
            
            mensaje = MIMEText(f"Tu codigo es: {codigo}")
            mensaje["subject"] = "Recuperar password"
            mensaje["From"] = remitente
            mensaje["To"] = correo.value
            
            servidor = smtplib.SMTP("smtp.gmail.com", 587)
            servidor.starttls()
            
            servidor.login(remitente, password)
            
            servidor.sendmail(
                remitente,
                correo.value,
                mensaje.as_string()
            )
            servidor.quit()
            page.show_dialog(ft.SnackBar(ft.Text("Codigo enviado con existo"),bgcolor="green"))
            txt_codigo.visible = True
            verificar.visible = True
            txt1.visible = True
            page.update()
            
        else:
            page.show_dialog(ft.SnackBar(ft.Text(msg),bgcolor="red"))
            return
            
    
    def verifica(e):
        codigo = getattr(page, "codigo")
        if txt_codigo.value == str(codigo):
            nueva.visible=True
            cambia_nueva.visible = True
            txt.visible = True
            page.update()
        else:
            page.show_dialog(ft.SnackBar(ft.Text("Codigo incorecto"),bgcolor="red"))
    
    def cambiar():
        listo,msg = auth_controller.cambiar(nueva.value,correo.value)
        if listo:
            page.show_dialog(ft.SnackBar(ft.Text(msg),bgcolor="green"))
            page.go("/")
        else:
            page.show_dialog(ft.SnackBar(ft.Text(msg),bgcolor="red"))
            page.go("/olvidado")
    
    def ver_contra():
        nueva.password = not nueva.password
        nueva.update()
        
    def regresar():
        page.go("/")
        
    reversa = ( ft.ElevatedButton("Regresar a login",color=ft.Colors.RED ,on_click=regresar))
    
    verificar = ft.ElevatedButton("Verificar",visible=False,on_click=verifica)
    cambia_nueva = ft.ElevatedButton("Cambiar contraseña",visible=False,on_click=cambiar)
    nueva=(ft.TextField(label="Contraseña nueva",visible=False,suffix=ft.IconButton(icon=ft.Icons.VISIBILITY, on_click=ver_contra) ,password=True, autofocus=True, icon=ft.Icons.PASSWORD))
    enviar= ft.ElevatedButton("Crear codigo", on_click=enviar_codigo, width=350, bgcolor="cyan", color = "black", icon=(ft.Icon(ft.Icons.MAIL, color=ft.Colors.WHITE, size=25)))
    txt = ft.Text("Ingrese su nueva contraseña", size=14, weight="bold", color="blue", visible=False)
    txt1 = ft.Text("Capture el codigo que resivio", size=14, weight="bold", color="blue", visible=False)
    
    return ft.View(
        route="/",
        vertical_alignment=ft.MainAxisAlignment.CENTER, 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        appbar=ft.AppBar(
            title=ft.Text("Login"),
            bgcolor=ft.Colors.BLUE_GREY_900,
            color="white",
        ),
        controls=[
            ft.Column(
                [
                    ft.Text("Cambio de contraseña", size=24, weight="bold"),
                    ft.Text("Nota: ingresa el correo que tienes registrado en la aplicacion", size=14, weight="bold", color="red"),
                    correo,
                    enviar,
                    reversa,
                    txt1,
                    txt_codigo,
                    verificar,
                    txt,
                    nueva,
                    cambia_nueva
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                tight=True 
            )
        ]
    )
    