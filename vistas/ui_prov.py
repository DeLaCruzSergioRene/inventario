import flet as ft
from datos.logica import guardar, listar, borrar
from estilos import btn_primary, btn_danger, card, PRIMARY, ACCENT

# Vista para registrar y gestionar proveedores
def vista_prov():
    n = ft.TextField(label="Nombre del Proveedor", width=300, border_radius=10)
    t = ft.TextField(label="Teléfono", width=300, border_radius=10)
    # Columna que muestra la lista de proveedores registrados
    col = ft.Column(horizontal_alignment="center", spacing=10)

    # Actualiza la lista visual de proveedores en la pantalla
    def refresh(e=None):
        items = []
        # Itera sobre todos los proveedores en la BD y crea tarjetas para cada uno
        for p in listar("prov"):
            def remove(id_reg):
                borrar("prov", id_reg)
                refresh()

            items.append(
                card(
                    ft.Row([
                        ft.Container(
                            bgcolor=ACCENT,
                            padding=ft.padding.symmetric(10, 8),
                            border_radius=50,
                            content=ft.Text(f"{p[1][0].upper()}", color="white", weight="bold", size=14)
                        ),
                        ft.Column([
                            ft.Text(p[1], weight="bold", size=14, color=PRIMARY),
                            ft.Text(f"📞 {p[2]}", size=12, color="black54")
                        ], spacing=2, expand=True),
                        btn_danger("✕", on_click=lambda e, id=p[0]: remove(id))
                    ], alignment="spaceBetween", vertical_alignment="center"),
                    width=450
                )
            )
        col.controls = items
        if col.page: col.update()

    # Registra un nuevo proveedor en la base de datos
    def add(e):
        # Valida que tanto el nombre como el teléfono estén completos
        if n.value and t.value:
            guardar("prov", (n.value, t.value))
            n.value, t.value = "", ""
            refresh()

    col.on_mount = refresh
    return ft.Column([
        ft.Text("PROVEEDORES", size=28, weight="bold", color=PRIMARY),
        ft.Text("Gestiona tus proveedores y contactos.", color="black54", size=14),
        ft.Divider(height=15, color="transparent"),
        card(
            ft.Column([n, t, btn_primary("REGISTRAR PROVEEDOR", on_click=add)], spacing=10),
            width=350
        ),
        ft.Divider(height=20, color="transparent"),
        col
    ], horizontal_alignment="center", scroll="auto")
