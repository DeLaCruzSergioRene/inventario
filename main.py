import flet as ft
from vistas.menu import vista_menu
from vistas.sesion import vista_sesion
from vistas.registro import vista_registro

def main(page: ft.Page):
    page.title = "Gestión de Inventario"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#F4F7FB"
    page.padding = 18
    page.theme_mode = ft.ThemeMode.LIGHT

    def mostrar_inicio():
        page.clean()
        page.add(vista_inicio())

    def mostrar_menu(e=None):
        page.clean()
        page.add(vista_menu(page))

    def vista_inicio():
        return ft.Stack(
            [
                ft.Container(
                    expand=True,
                    image=ft.DecorationImage(
                        src="datos/almacen.png",
                        fit="cover",
                    ),
                    bgcolor="#0F172A",
                ),
                ft.Container(expand=True, bgcolor="rgba(15, 23, 42, 0.55)"),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Gestor de inventario", size=30, weight="bold", color="white"),
                            ft.Text("Inicia sesión o crea una cuenta para entrar al sistema.", size=14, color="#E5E7EB"),
                            ft.Divider(height=10, color="transparent"),
                            ft.Button("Iniciar sesión", on_click=lambda e: mostrar_login(), width=260, style=ft.ButtonStyle(color="white", bgcolor="#2196F3")),
                            ft.Button("Registrarse", on_click=lambda e: mostrar_registro(), width=260, style=ft.ButtonStyle(color="white", bgcolor="#4CAF50")),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    padding=24,
                    border_radius=18,
                    bgcolor="rgba(255,255,255,0.96)",
                    shadow=ft.BoxShadow(blur_radius=14, spread_radius=1, color="#00000025"),
                    width=420,
                    alignment=ft.Alignment.CENTER,
                ),
            ],
            expand=True,
            alignment=ft.Alignment.CENTER,
        )

    def mostrar_login():
        page.clean()
        page.add(vista_sesion(page, on_success=mostrar_menu, on_back=mostrar_inicio))

    def mostrar_registro():
        page.clean()
        page.add(vista_registro(page, on_success=mostrar_menu, on_back=mostrar_inicio))

    mostrar_inicio()

ft.run(main)