import flet as ft
from datos.logica import guardar, listar, borrar

def vista_prod():
    n = ft.TextField(label="Producto", width=300)
    c = ft.TextField(label="Cantidad", width=300)
    col = ft.Column(horizontal_alignment="center")

    def refresh(e=None):
        items = []
        for p in listar("prod"):
            items.append(
                ft.Container(
                    bgcolor="white", padding=10, border_radius=10, width=400,
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
        borrar("prod", id_reg); refresh()

    def add(e):
        if n.value and c.value:
            guardar("prod", (n.value, c.value))
            n.value, c.value = "", ""; refresh()

    col.on_mount = refresh
    return ft.Column([
        ft.Text("INVENTARIO", size=25, weight="bold", color="blue"),
        n, c,
        ft.ElevatedButton("GUARDAR", on_click=add),
        col
    ], horizontal_alignment="center", scroll="auto")