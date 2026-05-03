import flet as ft
from vistas.ui_prod import vista_prod
from vistas.ui_prov import vista_prov

def main(page: ft.Page):
    page.title = "Gestión"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    panel = ft.Container(content=vista_prod(), padding=20)

    def ir_prod(e):
        panel.content = vista_prod()
        page.update()

    def ir_prov(e):
        panel.content = vista_prov()
        page.update()

    nav = ft.Container(
        content=ft.Row([
            ft.TextButton("PRODUCTOS", on_click=ir_prod, icon="inventory"),
            ft.TextButton("PROVEEDORES", on_click=ir_prov, icon="people"),
        ], alignment=ft.MainAxisAlignment.CENTER),
        bgcolor=ft.Colors.WHITE, border_radius=15, margin=10
    )

    page.add(nav, panel)

ft.app(target=main)