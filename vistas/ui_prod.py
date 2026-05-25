import flet as ft
from datos.logica import guardar, listar, borrar

def vista_prod():
    n = ft.TextField(label="Producto", width=300, border_radius=10)
    c = ft.TextField(label="Cantidad", width=300, border_radius=10)
    col = ft.Column(horizontal_alignment="center", spacing=10)

    def refresh(e=None):
        items = []
        for p in listar("prod"):
            items.append(
                ft.Container(
                    bgcolor=ft.Colors.BLUE_GREY_50, padding=12, border_radius=12, width=420,
                    content=ft.Row([
                        ft.Text(f"✅ {p[1]}", color="black", weight="bold", expand=True),
                        ft.Text(f"Cant: {p[2]}", color="black"),
                        ft.TextButton("BORRAR", on_click=lambda e, id=p[0]: remove(id))
                    ])
                )
            )
        col.controls = items
        if col.page: col.update()

    def remove(id_reg):
        borrar("prod", id_reg)
        refresh()

    def add(e):
        if n.value and c.value:
            guardar("prod", (n.value, c.value))
            n.value, c.value = "", ""; refresh()

    col.on_mount = refresh
    return ft.Column([
        ft.Text("INVENTARIO", size=25, weight="bold", color="blue"),
        ft.Text("Registra aquí los productos y su stock", color="black54"),
        n, c,
        ft.ElevatedButton("GUARDAR", on_click=add, bgcolor=ft.Colors.BLUE),
        ft.Divider(height=20, color="transparent"),
        col
    ], horizontal_alignment="center", scroll="auto")