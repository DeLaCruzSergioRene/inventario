import re
import flet as ft
from datos.logica import verificar_usuario
from estilos import DANGER, PRIMARY, SUCCESS, card

def vista_sesion(page: ft.Page, on_success=None, on_back=None):
    email = ft.TextField(label="Correo electrónico", width=320, border_radius=10)
    clave = ft.TextField(label="Contraseña", password=True, width=320, border_radius=10)
    mensaje = ft.Text("", size=12, color=SUCCESS)

    def validar_email(valor: str) -> bool:
        return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor))

    def entrar(e=None):
        mensaje.value = ""
        email_txt = email.value.strip().lower()
        clave_txt = clave.value.strip()

        if not email_txt or not clave_txt:
            mensaje.value = "Completa ambos campos para continuar."
            mensaje.color = DANGER
        elif not validar_email(email_txt):
            mensaje.value = "Correo inválido."
            mensaje.color = DANGER
        elif not verificar_usuario(email_txt, clave_txt):
            mensaje.value = "Correo o contraseña incorrectos."
            mensaje.color = DANGER
        else:
            mensaje.value = "Inicio de sesión correcto."
            mensaje.color = SUCCESS
            page.update()
            if on_success:
                on_success()
            return

        page.update()

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Inicio de sesión", size=24, weight="bold", color=PRIMARY),
                ft.Text("Ingresa tus datos para entrar al menú.", size=13, color="black54"),
                email,
                clave,
                mensaje,
                ft.Row(
                    [
                        ft.Button("Entrar", on_click=entrar, width=140, style=ft.ButtonStyle(color="white", bgcolor="#2196F3")),
                        ft.TextButton("Volver", on_click=lambda e: on_back() if on_back else None),
                    ],
                    spacing=10,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        padding=24,
        border_radius=18,
        bgcolor="white",
        shadow=ft.BoxShadow(blur_radius=10, spread_radius=1, color="#00000015"),
        width=420,
    )
