import flet as ft
from datos.logica import guardar, listar, borrar

def vista_prov():
    n = ft.TextField(label="Nombre del Proveedor", width=300, border_radius=10)
    t = ft.TextField(label="Teléfono", width=300, border_radius=10)
    col = ft.Column(horizontal_alignment="center", spacing=10)

    def refresh(e=None):
        items = []
        for p in listar("prov"):
            items.append(
                ft.Container(
                    bgcolor="white", padding=15, border_radius=10, width=400,
                    content=ft.Row([
                        ft.Text(f"✅ {p[1]}", weight="bold", size=16, color="black", expand=True),
                        ft.Text(f"Tel: {p[2]}", color="black"),
                        # Botón de texto simple para borrar
                        ft.TextButton("ELIMINAR", on_click=lambda e, id=p[0]: remove(id))
                    ], alignment="spaceBetween")
                )
            )
        col.controls = items
        if col.page: col.update()

    def remove(id_reg):
        borrar("prov", id_reg)
        refresh()

    def add(e):
        if n.value and t.value:
            guardar("prov", (n.value, t.value))
            n.value, t.value = "", ""
            refresh()

    col.on_mount = refresh
    return ft.Column([
        ft.Text("PROVEEDORES", size=28, weight="bold", color="blue"),
        n, t,
        ft.ElevatedButton("REGISTRAR", on_click=add),
        ft.Divider(height=20, color="transparent"),
        col
    ], horizontal_alignment="center", scroll="auto")