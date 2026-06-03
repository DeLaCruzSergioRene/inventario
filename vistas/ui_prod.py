import flet as ft
from datos.logica import guardar, listar, borrar
from estilos import btn_primary, btn_danger, card, PRIMARY, ACCENT

# Vista para gestionar el inventario de productos
def vista_prod():
    # Campo de texto para ingresar el nombre del producto
    n = ft.TextField(label="Producto", width=300, border_radius=10)
    # Campo de texto para ingresar la cantidad inicial del producto
    c = ft.TextField(label="Cantidad", width=300, border_radius=10, keyboard_type=ft.KeyboardType.NUMBER)
    # Columna que muestra la lista de productos registrados
    col = ft.Column(horizontal_alignment="center", spacing=10)

    # Actualiza la lista visual de productos en la pantalla
    def refresh(e=None):
        items = []
        # Itera sobre todos los productos registrados en la BD
        for p in listar("prod"):
            def remove(id_reg):
                borrar("prod", id_reg)
                refresh()

            items.append(
                card(
                    ft.Row([
                        ft.Container(
                            bgcolor=ACCENT,
                            padding=ft.padding.symmetric(8, 6),
                            border_radius=50,
                            content=ft.Text(p[1][0].upper(), color="white", weight="bold")
                        ),
                        ft.Column([
                            ft.Text(p[1], weight="bold", size=14, color=PRIMARY),
                            ft.Text(f"📦 {p[2]} unidades", size=11, color="black54")
                        ], spacing=1, expand=True),
                        btn_danger("✕", on_click=lambda e, id=p[0]: remove(id))
                    ], alignment="spaceBetween", vertical_alignment="center"),
                    width=450
                )
            )
        col.controls = items
        if col.page: col.update()

    # Agrega un nuevo producto a la base de datos
    def add(e):
        # Valida que los campos no estén vacíos y que la cantidad sea un número
        if n.value and c.value and c.value.isdigit():
            guardar("prod", (n.value, c.value))
            n.value, c.value = "", ""
            refresh()

    col.on_mount = refresh
    return ft.Column([
        ft.Text("INVENTARIO", size=28, weight="bold", color=PRIMARY),
        ft.Text("Registra productos y gestiona el stock.", color="black54", size=14),
        ft.Divider(height=15, color="transparent"),
        card(
            ft.Column([n, c, btn_primary("GUARDAR PRODUCTO", on_click=add)], spacing=10),
            width=350
        ),
        ft.Divider(height=20, color="transparent"),
        col
    ], horizontal_alignment="center", scroll="auto")
