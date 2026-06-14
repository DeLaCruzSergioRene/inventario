import re
import flet as ft
from datos.logica import guardar_usuario, obtener_usuario_por_email
from estilos import DANGER, PRIMARY, SUCCESS, card

def vista_registro(page: ft.Page, on_success=None, on_back=None):
    nombre = ft.TextField(label="Nombre completo", width=320, border_radius=10)
    email = ft.TextField(label="Correo electrónico", width=320, border_radius=10)
    clave = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=320, border_radius=10)
    mensaje = ft.Text("", size=12, color=SUCCESS)

    def validar_email(valor: str) -> bool:
        return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor))

    def crear_cuenta(e=None):
        mensaje.value = ""
        nombre_txt = nombre.value.strip()
        email_txt = email.value.strip().lower()
        clave_txt = clave.value.strip()

        if not nombre_txt:
            mensaje.value = "Ingresa tu nombre completo."
            mensaje.color = DANGER
        elif not validar_email(email_txt):
            mensaje.value = "Ingresa un correo válido."
            mensaje.color = DANGER
        elif len(clave_txt) < 8:
            mensaje.value = "La contraseña debe tener al menos 8 caracteres."
            mensaje.color = DANGER
        elif obtener_usuario_por_email(email_txt):
            mensaje.value = "Ese correo ya está registrado."
            mensaje.color = DANGER
        else:
            if guardar_usuario(nombre_txt, email_txt, clave_txt):
                mensaje.value = "Cuenta creada correctamente."
                mensaje.color = SUCCESS
                page.update()
                if on_success:
                    on_success()
                return
            mensaje.value = "No se puede registrar el mismo correo dos veces."
            mensaje.color = DANGER

        page.update()

    return ft.Container(
        expand=True,
        alignment=ft.Alignment.CENTER,
        content=ft.Stack(
            [
                ft.Container(
                    expand=True,
                    opacity=0.32,
                    image=ft.DecorationImage(src="imagenes/registro.png", fit="cover"),
                    bgcolor="#0F172A",
                ),
                ft.Container(expand=True, bgcolor="rgba(7, 25, 16, 0.35)"),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Registro", size=24, weight="bold", color=PRIMARY),
                            ft.Text("Crea tu cuenta para entrar al sistema.", size=13, color="black54"),
                            nombre,
                            email,
                            clave,
                            mensaje,
                            ft.Row(
                                [
                                    ft.Button("Crear cuenta", on_click=crear_cuenta, width=150, style=ft.ButtonStyle(color="white", bgcolor="#4CAF50")),
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
                    bgcolor="rgba(247, 255, 249, 0.94)",
                    shadow=ft.BoxShadow(blur_radius=12, spread_radius=1, color="#00000018"),
                    width=440,
                    alignment=ft.Alignment.CENTER,
                ),
            ],
            expand=True,
            alignment=ft.Alignment.CENTER,
        ),
    )
