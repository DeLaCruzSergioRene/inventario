import flet as ft
from datos.logica import formatear_fecha_local, listar_pedidos, borrar_pedido
from estilos import card, btn_danger, PRIMARY, SUCCESS, DANGER, BG


def vista_compras(page, volver=None):
    lista = ft.Column(spacing=10)

    def mostrar_mensaje(texto, exito=True):
        page.snack_bar = ft.SnackBar(ft.Text(texto), bgcolor=SUCCESS if exito else DANGER)
        page.snack_bar.open = True
        page.update()

    def borrar_directo(id_reg, e=None):
        res = borrar_pedido(id_reg)
        if res:
            mostrar_mensaje("Pedido eliminado.")
        else:
            mostrar_mensaje("No se pudo eliminar el pedido.", False)
        refrescar()
        page.update()

    def refrescar(e=None):
        items = []
        for pedido in listar_pedidos():
            # pedido = (id, prod_id, prod_nom, prov_id, prov_nom, cant, tipo, precio_unitario, costo_total, fecha)
            if pedido[6] not in ("stock", "pedido"):
                continue

            tipo_label = "Compra" if pedido[6] == "stock" else "Pedido"
            precio_unitario = float(pedido[7] or 0)
            costo_total = float(pedido[8] or 0)

            items.append(
                card(
                    ft.Row([
                        ft.Column([
                            ft.Text(f"{pedido[2]}", size=15, weight="bold", color=PRIMARY),
                            ft.Text(f"Tipo: {tipo_label} | Cantidad: {pedido[5]} | Proveedor: {pedido[4]}", size=12, color="black54"),
                            ft.Row([
                                ft.Text(f"Costo total: ${costo_total:,.2f}", size=12, color=SUCCESS, weight="bold"),
                                ft.Text(f"Precio unitario: ${precio_unitario:,.2f}", size=12, color=DANGER),
                            ], spacing=20),
                            ft.Text(f"Fecha: {formatear_fecha_local(pedido[9])}", size=11, color="black54"),
                        ], spacing=4, expand=True),
                        btn_danger("✕", on_click=lambda e, id=pedido[0]: borrar_directo(id))
                    ], alignment="spaceBetween", vertical_alignment="center"),
                    width=520,
                )
            )

        if not items:
            items = [ft.Text("Aún no hay compras registradas.", color="grey", italic=True)]

        lista.controls = items
        try:
            lista.update()
            page.update()
        except RuntimeError:
            pass

    refrescar()

    return ft.Container(
        expand=True,
        padding=10,
        bgcolor=BG,
        content=ft.Column([
            ft.Row([
                ft.Text("Compras", size=28, weight="bold", color=PRIMARY),
                ft.Text("Aquí verás qué productos se han comprado o reabastecido.", size=13, color="black54"),
            ], alignment="center", wrap=True),
            ft.Divider(height=10, color="transparent"),
            ft.Text("Historial de compras", size=16, weight="bold", color=SUCCESS),
            ft.Container(
                content=lista,
                alignment=ft.Alignment(0, 0),
                width=600,
            ),
        ], spacing=10, scroll="auto", horizontal_alignment=ft.CrossAxisAlignment.CENTER),
    )
