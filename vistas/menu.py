import flet as ft
from vistas.pedidos import vista_pedidos
from vistas.resumen import vista_resumen
from vistas.ui_prod import vista_prod
from vistas.ui_prov import vista_prov
from vistas.compras import vista_compras
from estilos import DARK


def vista_menu(page: ft.Page, on_logout=None):
    panel = ft.Container(
        content=vista_prod(page),
        padding=20,
        expand=True,
        border_radius=18,
        bgcolor="white",
        shadow=ft.BoxShadow(blur_radius=12, spread_radius=1, color="#00000018"),
    )

    def ir_prod(e):
        panel.content = vista_prod(page)
        panel.update()
        page.update()

    def ir_prov(e):
        panel.content = vista_prov(page)
        panel.update()
        page.update()

    def ir_pedidos(e):
        panel.content = vista_pedidos(page, ir_resumen)
        panel.update()
        page.update()

    def ir_resumen(e):
        panel.content = vista_resumen(page, ir_pedidos)
        panel.update()
        page.update()

    def ir_compras(e):
        panel.content = vista_compras(page, ir_pedidos)
        panel.update()
        page.update()

    nav = ft.Container(
        width=980,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Menú principal", size=22, weight="bold", color=DARK),
                        ft.Text("Productos, proveedores, pedidos y resumen desde aquí.", size=13, color="black54"),
                        ft.TextButton(
                            "🔒 Cerrar sesión",
                            on_click=on_logout,
                            style=ft.ButtonStyle(color=DARK),
                        ) if on_logout else ft.Container(),
                    ],
                    alignment="spaceBetween",
                    wrap=True,
                ),
                ft.Row(
                    [
                        ft.TextButton("📦 Productos", on_click=ir_prod, style=ft.ButtonStyle(color=DARK)),
                        ft.TextButton("👥 Proveedores", on_click=ir_prov, style=ft.ButtonStyle(color=DARK)),
                        ft.TextButton("📋 Pedidos", on_click=ir_pedidos, style=ft.ButtonStyle(color=DARK)),
                        ft.TextButton("🛒 Compras", on_click=ir_compras, style=ft.ButtonStyle(color=DARK)),
                        ft.TextButton("📊 Resumen", on_click=ir_resumen, style=ft.ButtonStyle(color=DARK)),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    wrap=True,
                ),
            ],
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor="white",
        border_radius=18,
        margin=10,
        padding=16,
        shadow=ft.BoxShadow(blur_radius=10, spread_radius=1, color="#00000015"),
    )

    return ft.Column(
        [nav, panel],
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )
