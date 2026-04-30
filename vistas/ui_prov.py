import flet as ft
from datos.logica import guardar, listar

def vista_prov():
    n = ft.TextField(label="Nombre")
    t = ft.TextField(label="Teléfono")
    col = ft.Column()

    def refresh(e=None):
        col.controls = [ft.Text(f"👤 {p[1]} - 📞 {p[2]}") for p in listar("prov")]
        if col.page: col.update()

    def add(e):
        if n.value and t.value:
            guardar("prov", (n.value, t.value))
            n.value, t.value = "", ""
            refresh()

    col.on_mount = refresh
    return ft.Column([ft.Text("PROVEEDORES"), n, t, ft.ElevatedButton("OK", on_click=add), col])