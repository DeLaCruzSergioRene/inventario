import flet as ft
from datos.logica import listar, pedir_producto, actualizar_stock
from estilos import btn_success, btn_danger, card, ACCENT, SUCCESS, DANGER

# Vista principal para realizar pedidos y gestionar stock
def vista_pedidos(page):
    productos = ft.Column(horizontal_alignment="center", spacing=10)
    proveedores_dropdown = ft.Dropdown(
        label="Seleccionar Proveedor",
        width=300,
        border_radius=10,
        options=[]
    )

    def mostrar_mensaje(texto, exito=True):
        page.snack_bar = ft.SnackBar(ft.Text(texto), bgcolor=SUCCESS if exito else DANGER)
        page.snack_bar.open = True
        page.update()

    def cargar_proveedores():
        provs = listar("prov")
        proveedores_dropdown.options = [ft.dropdown.Option(p[1]) for p in provs]
        try:
            if proveedores_dropdown.page:
                proveedores_dropdown.update()
        except RuntimeError:
            pass

    def refresh(e=None):
        cargar_proveedores()
        items = []
        for p in listar("prod"):
            cantidad = ft.TextField(
                value="1",
                width=110,
                text_align=ft.TextAlign.CENTER,
                keyboard_type=ft.KeyboardType.NUMBER,
                label="Cantidad",
                dense=True,
                border_radius=10
            )
            campo_agregar = ft.TextField(
                value="1",
                width=90,
                text_align=ft.TextAlign.CENTER,
                keyboard_type=ft.KeyboardType.NUMBER,
                label="Añadir",
                dense=True,
                border_radius=8
            )

            def order_producto(e, id_prod=p[0], nombre=p[1], field=cantidad):
                if not field.value or not field.value.isdigit() or int(field.value) <= 0:
                    mostrar_mensaje("Ingrese una cantidad válida.", False)
                else:
                    qty = int(field.value)
                    if pedir_producto(id_prod, qty):
                        mostrar_mensaje(f"✓ Pedido: {qty} x {nombre}")
                    else:
                        mostrar_mensaje("Stock insuficiente.", False)
                refresh()

            def agregar_stock(e, id_prod=p[0], nombre=p[1], field=campo_agregar):
                if not field.value or not field.value.isdigit() or int(field.value) <= 0:
                    mostrar_mensaje("Cantidad inválida.", False)
                else:
                    qty = int(field.value)
                    if actualizar_stock(id_prod, qty):
                        mostrar_mensaje(f"✓ +{qty} stock a {nombre}")
                    else:
                        mostrar_mensaje("Error al actualizar.", False)
                refresh()

            items.append(
                ft.Container(
                    content=card(
                        ft.Column([
                            ft.Row([
                                ft.Text(p[1], size=16, weight="bold", color="#2196F3", expand=True),
                                ft.Container(
                                    bgcolor=ACCENT,
                                    padding=ft.padding.symmetric(8, 4),
                                    border_radius=8,
                                    content=ft.Text(f"Stock: {p[2]}", color="white", size=13, weight="bold")
                                )
                            ], alignment="spaceBetween"),
                            ft.Row([
                                cantidad,
                                btn_success("PEDIR", on_click=order_producto),
                                ft.IconButton(ft.icons.Icons.ADD, icon_color="#4CAF50",
                                    on_click=agregar_stock, tooltip="Aumentar stock")
                            ], spacing=5, wrap=False),
                            ft.Row([campo_agregar], spacing=5)
                        ], spacing=8)
                    ),
                    width=520
                )
            )

        if not items:
            items = [ft.Text("No hay productos cargados.", color="grey", italic=True)]
        productos.controls = items
        try:
            productos.update()
        except RuntimeError:
            pass

    refresh()
    return ft.Column(
        [
            ft.Text("PEDIDOS", size=28, weight="bold", color="#2196F3"),
            ft.Text("Realiza pedidos y gestiona el stock.", size=14, color="black54"),
            ft.Divider(height=15, color="transparent"),
            ft.Container(
                bgcolor="#F5F5F5",
                padding=12,
                border_radius=10,
                content=proveedores_dropdown
            ),
            ft.Divider(height=15, color="transparent"),
            productos
        ],
        horizontal_alignment="center",
        scroll="auto"
    )
