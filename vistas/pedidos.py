import flet as ft
from datos.logica import listar

def vista_pedidos():
    col = ft.Column(horizontal_alignment="center", spacing=10)

    def refresh(e=None):
        items = []
        for p in listar("prod"):
            items.append(
                ft.Container(
                    bgcolor=ft.Colors.BLUE_GREY_50,
                    padding=12,
                    border_radius=12,
                    width=420,
                    content=ft.Row(
                        [
                            ft.Text(p[1], size=16, weight="bold", color="blue", expand=True),
                            ft.Text(f"Stock: {p[2]}", size=15, color="black")
                        ],
                        alignment="spaceBetween"
                    )
                )
            )
        if not items:
            items = [ft.Text("No hay productos cargados.", color="grey", italic=True)]
        col.controls = items
        if col.page:
            col.update()

    col.on_mount = refresh
    return ft.Column(
        [
            ft.Text("PEDIDOS", size=28, weight="bold", color="blue"),
            ft.Text("Stock actual de los productos registrados", size=15, color="black54"),
            ft.Divider(height=20, color="transparent"),
            col
        ],
        horizontal_alignment="center",
        scroll="auto"
    )
