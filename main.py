import flet as ft
from vistas.pedidos import vista_pedidos
from vistas.resumen import vista_resumen
from vistas.ui_prod import vista_prod
from vistas.ui_prov import vista_prov
from estilos import PRIMARY, DARK

def main(page: ft.Page):
    page.title = "Gestión de Inventario"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#F4F7FB"
    page.padding = 18
    page.theme_mode = ft.ThemeMode.LIGHT

    # Contenedor principal que muestra la vista actualmente seleccionada
    panel = ft.Container(
        content=vista_prod(page),
        padding=20,
        expand=True,
        border_radius=18,
        bgcolor="white",
        shadow=ft.BoxShadow(blur_radius=12, spread_radius=1, color="#00000018"),
    )

    # Funciones para cambiar entre vistas al hacer clic en los botones de navegación
    def ir_prod(e):
        panel.content = vista_prod(page)
        page.update()

    def ir_prov(e):
        panel.content = vista_prov(page)
        page.update()

    def ir_pedidos(e):
        panel.content = vista_pedidos(page, ir_resumen)
        page.update()

    def ir_resumen(e):
        panel.content = vista_resumen(page, ir_pedidos)
        page.update()

    # Barra de navegación superior con botones para cambiar de vista
    nav = ft.Container(
        content=ft.Column([
            ft.Text("Gestor de inventario", size=22, weight="bold", color=DARK),
            ft.Text("Productos, proveedores y pedidos en un solo lugar.", size=13, color="black54"),
            ft.Row([
                ft.TextButton("📦 PRODUCTOS", on_click=ir_prod, style=ft.ButtonStyle(color=DARK)),
                ft.TextButton("👥 PROVEEDORES", on_click=ir_prov, style=ft.ButtonStyle(color=DARK)),
                ft.TextButton("📋 PEDIDOS", on_click=ir_pedidos, style=ft.ButtonStyle(color=DARK)),
                ft.TextButton("📊 RESUMEN", on_click=ir_resumen, style=ft.ButtonStyle(color=DARK)),
            ], alignment=ft.MainAxisAlignment.CENTER, wrap=True),
        ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor="white",
        border_radius=18,
        margin=10,
        padding=16,
        shadow=ft.BoxShadow(blur_radius=10, spread_radius=1, color="#00000015"),
    )
    page.add(nav, panel)

ft.run(main)