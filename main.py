import flet as ft
from vistas.ui_prod import vista_prod
from vistas.ui_prov import vista_prov

def main(page: ft.Page):
    page.title = "Sistema"
    panel = ft.Container(content=vista_prod(), expand=True)

    def ir_prod(e):
        panel.content = vista_prod()
        page.update()

    def ir_prov(e):
        panel.content = vista_prov()
        page.update()

    nav = ft.Row([
        ft.ElevatedButton("Productos", on_click=ir_prod),
        ft.ElevatedButton("Proveedores", on_click=ir_prov),
    ])

    page.add(nav, panel)

if __name__ == "__main__":
    ft.app(target=main)