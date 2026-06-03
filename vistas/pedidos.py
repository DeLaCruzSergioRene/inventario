import flet as ft
from datos.logica import listar, pedir_producto, actualizar_stock
from estilos import btn_success, btn_danger, card, ACCENT

# Vista principal para realizar pedidos y gestionar stock
def vista_pedidos():
    # Etiqueta para mostrar mensajes de éxito o error
    mensaje = ft.Text("", color="red")
    # Columna que contiene la lista de productos disponibles
    productos = ft.Column(horizontal_alignment="center", spacing=10)
    
    # Dropdown para seleccionar de qué proveedor hacer el pedido
    proveedores_dropdown = ft.Dropdown(
        label="Seleccionar Proveedor",
        width=300,
        border_radius=10,
        options=[]
    )
    
    # Obtiene todos los proveedores registrados y los carga en el dropdown
    def cargar_proveedores():
        provs = listar("prov")
        # Crea opciones en el dropdown con el nombre de cada proveedor
        proveedores_dropdown.options = [ft.dropdown.Option(p[1]) for p in provs]
        try:
            if proveedores_dropdown.page:
                proveedores_dropdown.update()
        except RuntimeError:
            pass

    # Actualiza la lista de productos cada vez que hay un cambio
    def refresh(e=None):
        cargar_proveedores()  # Recarga los proveedores en el dropdown
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
                if not field.value or not field.value.isdigit():
                    mensaje.value = "Ingrese una cantidad válida."
                else:
                    qty = int(field.value)
                    if pedir_producto(id_prod, qty):
                        mensaje.value = f"✓ Pedido: {qty} x {nombre}"
                    else:
                        mensaje.value = "Stock insuficiente."
                refresh()
                try:
                    productos.update()
                except RuntimeError:
                    pass

            # Función para añadir más unidades al stock de un producto
            def agregar_stock(e, id_prod=p[0], nombre=p[1], field=campo_agregar):
                # Valida que la entrada sea un número válido
                if not field.value or not field.value.isdigit():
                    mensaje.value = "Cantidad inválida."
                else:
                    qty = int(field.value)
                    if actualizar_stock(id_prod, qty):
                        mensaje.value = f"✓ +{qty} stock a {nombre}"
                    else:
                        mensaje.value = "Error al actualizar."
                refresh()
                try:
                    productos.update()
                except RuntimeError:
                    pass

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
            mensaje,
            ft.Divider(height=15, color="transparent"),
            productos
        ],
        horizontal_alignment="center",
        scroll="auto"
    )
