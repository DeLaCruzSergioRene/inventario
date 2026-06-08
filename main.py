import flet as ft
from vistas.pedidos import vista_pedidos
from vistas.ui_prod import vista_prod
from vistas.ui_prov import vista_prov
from estilos import PRIMARY, DARK

def main(page: ft.Page):
    page.title = "Gestión de Inventario"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#FAFAFA" 
    
    # Contenedor principal que muestra la vista actualmente seleccionada
    panel = ft.Container(content=vista_prod(page), padding=20, expand=True)

    # Funciones para cambiar entre vistas al hacer clic en los botones de navegación
    def ir_prod(e):
        panel.content = vista_prod(page)
        page.update()

    def ir_prov(e):
        panel.content = vista_prov(page)
        page.update()

    def ir_pedidos(e):
        panel.content = vista_pedidos(page)
        page.update()

    # Barra de navegación superior con botones para cambiar de vista
    nav = ft.Container(
        content=ft.Row([
            ft.TextButton("📦 PRODUCTOS", on_click=ir_prod, style=ft.ButtonStyle(color=DARK)),
            ft.TextButton("👥 PROVEEDORES", on_click=ir_prov, style=ft.ButtonStyle(color=DARK)),
            ft.TextButton("📋 PEDIDOS", on_click=ir_pedidos, style=ft.ButtonStyle(color=DARK)),
        ], alignment=ft.MainAxisAlignment.CENTER),
        bgcolor="white", border_radius=12, margin=10,
        shadow=ft.BoxShadow(blur_radius=5, spread_radius=1, color="#00000010")
    )

    page.add(nav, panel)

ft.run(main)