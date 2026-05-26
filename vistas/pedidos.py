import flet as ft
from datos.logica import listar, pedir_producto

def vista_pedidos():
    mensaje = ft.Text("", color="red")
    productos = ft.Column(horizontal_alignment="center", spacing=10)

    def refresh(e=None):
        items = []
        for p in listar("prod"):
            cantidad = ft.TextField(
                value="1",
                width=100,
                text_align=ft.TextAlign.CENTER,
                keyboard_type=ft.KeyboardType.NUMBER,
                label="Cantidad",
                dense=True,
                border_radius=10
            )

            def order_producto(e, id_prod=p[0], nombre=p[1], field=cantidad):
                if not field.value or not field.value.isdigit():
                    mensaje.value = "Ingrese una cantidad válida."
                else:
                    qty = int(field.value)
                    if pedir_producto(id_prod, qty):
                        mensaje.value = f"Pedido realizado: {qty} x {nombre}."
                    else:
                        mensaje.value = "Stock insuficiente o cantidad inválida."
                refresh()
                try:
                    productos.update()
                except RuntimeError:
                    pass

            items.append(
                ft.Container(
                    bgcolor=ft.Colors.BLUE_GREY_50,
                    padding=12,
                    border_radius=12,
                    width=520,
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(p[1], size=16, weight="bold", color="blue", expand=True),
                                    ft.Text(f"Stock: {p[2]}", size=15, color="black")
                                ],
                                alignment="spaceBetween"
                            ),
                            ft.Row(
                                [
                                    cantidad,
                                    ft.ElevatedButton("PEDIR", on_click=order_producto, bgcolor=ft.Colors.GREEN),
                                ],
                                alignment="spaceBetween"
                            )
                        ]
                    )
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
            ft.Text("PEDIDOS", size=28, weight="bold", color="blue"),
            ft.Text("Selecciona un producto y pide la cantidad deseada.", size=15, color="black54"),
            mensaje,
            ft.Divider(height=20, color="transparent"),
            productos
        ],
        horizontal_alignment="center",
        scroll="auto"
    )
