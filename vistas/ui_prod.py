import flet as ft
from datos.logica import guardar, listar

def vista_prod():
    n = ft.TextField(label="Producto")
    c = ft.TextField(label="Cantidad")
    col = ft.Column()

    def refresh(e=None):
        col.controls = [ft.Text(f"📦 {p[1]} | Stock: {p[2]}") for p in listar("prod")]
        if col.page: col.update()

    def add(e):
        if n.value and c.value:
            guardar("prod", (n.value, int(c.value)))
            n.value, c.value = "", ""
            refresh()

    col.on_mount = refresh
    return ft.Column([ft.Text("INVENTARIO"), n, c, ft.ElevatedButton("OK", on_click=add), col])