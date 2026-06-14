import flet as ft
from datos.logica import listar, pedir_producto, actualizar_stock, registrar_pedido
from datos.presupuesto import obtener_presupuesto, guardar_presupuesto, consumir_presupuesto, costo_total, presupuesto_suficiente
from estilos import btn_primary, btn_success, btn_danger, card, ACCENT, SUCCESS, DANGER

# Vista principal para realizar pedidos y gestionar stock

def vista_pedidos(page, ir_resumen=None):
    productos = ft.Column(horizontal_alignment="center", spacing=10)
    buscador = ft.TextField(
        label="Buscar producto",
        hint_text="Filtra por nombre",
        width=320,
        border_radius=10,
        on_change=None
    )
    resumen_stock = ft.Row(spacing=10, wrap=True)
    alerta_stock = ft.Text("", size=12, color="black54")
    presupuesto_info = ft.Text("", size=12, color="#4CAF50")
    presupuesto_input = ft.TextField(
        label="Presupuesto disponible",
        value="0.00",
        width=220,
        border_radius=10,
        keyboard_type=ft.KeyboardType.NUMBER,
        hint_text="Ej. 5000"
    )
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
        proveedores_dropdown.options = [ft.dropdown.Option(key=str(p[0]), text=p[1]) for p in provs]
        try:
            if proveedores_dropdown.page:
                proveedores_dropdown.update()
        except RuntimeError:
            pass

    def obtener_proveedor_seleccionado():
        prov_id = proveedores_dropdown.value
        if not prov_id:
            return None, None
        for p in listar("prov"):
            if str(p[0]) == str(prov_id):
                return p[0], p[1]
        return None, None

    def actualizar_presupuesto(e=None):
        try:
            nuevo = float((presupuesto_input.value or "0").replace(",", "."))
        except ValueError:
            mostrar_mensaje("Ingrese un presupuesto válido.", False)
            return
        guardar_presupuesto(max(0.0, nuevo))
        presupuesto_input.value = f"{obtener_presupuesto():.2f}"
        presupuesto_info.value = f"Presupuesto disponible: ${obtener_presupuesto():,.2f}"
        presupuesto_info.color = SUCCESS
        mostrar_mensaje("Presupuesto actualizado.")
        try:
            presupuesto_info.update()
            presupuesto_input.update()
            page.update()
        except RuntimeError:
            pass

    def refresh(e=None):
        cargar_proveedores()
        presupuesto_input.value = f"{obtener_presupuesto():.2f}"
        presupuesto_info.value = f"Presupuesto disponible: ${obtener_presupuesto():,.2f}"
        presupuesto_info.color = SUCCESS
        todos = listar("prod")
        texto = (buscador.value or "").strip().lower()
        stock_total = [p for p in todos if not texto or texto in p[1].lower()]
        total_productos = len(stock_total)
        total_unidades = sum(p[2] for p in stock_total)
        stock_bajo = [p for p in stock_total if p[2] < 5]

        resumen_stock.controls = [
            card(ft.Column([ft.Text("Productos", size=11, color="black54"), ft.Text(str(total_productos), size=24, weight="bold", color="#2196F3")]), width=170),
            card(ft.Column([ft.Text("Unidades", size=11, color="black54"), ft.Text(str(total_unidades), size=24, weight="bold", color="#4CAF50")]), width=170),
            card(ft.Column([ft.Text("Stock bajo", size=11, color="black54"), ft.Text(str(len(stock_bajo)), size=24, weight="bold", color=DANGER)]), width=170),
        ]
        alerta_stock.value = f"⚠️ {len(stock_bajo)} producto(s) necesitan reposición." if stock_bajo else "✅ No hay alertas de stock bajo."
        alerta_stock.color = DANGER if stock_bajo else SUCCESS

        items = []
        for p in stock_total:
            aviso_proveedor = ft.Text("", size=12, color=DANGER, visible=False)
            cantidad = ft.TextField(
                value="1",
                width=110,
                text_align=ft.TextAlign.CENTER,
                keyboard_type=ft.KeyboardType.NUMBER,
                label="Cantidad",
                dense=True,
                border_radius=10
            )
            def order_producto(e, id_prod=p[0], nombre=p[1], field=cantidad):
                try:
                    qty = int((field.value or "").strip())
                except ValueError:
                    aviso_proveedor.value = "⚠️ Ingresa una cantidad válida para continuar."
                    aviso_proveedor.visible = True
                    aviso_proveedor.update()
                    mostrar_mensaje("Ingrese una cantidad válida.", False)
                    return

                if qty <= 0:
                    aviso_proveedor.value = "⚠️ La cantidad debe ser mayor que cero."
                    aviso_proveedor.visible = True
                    aviso_proveedor.update()
                    mostrar_mensaje("Ingrese una cantidad válida.", False)
                    return

                prov_id, prov_nom = obtener_proveedor_seleccionado()
                if not prov_id or not prov_nom:
                    aviso_proveedor.value = "⚠️ Selecciona un proveedor para poder pedir este producto."
                    aviso_proveedor.visible = True
                    aviso_proveedor.update()
                    mostrar_mensaje("Seleccione un proveedor para asociar el pedido.", False)
                    return

                precio_unitario = float(p[3] if len(p) > 3 else 0)
                venta_total = qty * precio_unitario

                if pedir_producto(id_prod, qty):
                    aviso_proveedor.value = ""
                    aviso_proveedor.visible = False
                    aviso_proveedor.update()
                    guardar_presupuesto(obtener_presupuesto() + venta_total)
                    registrar_pedido(id_prod, nombre, prov_id, prov_nom, qty, "pedido", precio_unitario, venta_total)
                    mostrar_mensaje(f"✓ Venta registrada: {qty} x {nombre} · Ingreso: ${venta_total:,.2f}")
                else:
                    aviso_proveedor.value = "⚠️ No hay stock suficiente para esta cantidad."
                    aviso_proveedor.visible = True
                    aviso_proveedor.update()
                    mostrar_mensaje("Stock insuficiente.", False)
                    return
                refresh()

            def agregar_stock(e, id_prod=p[0], nombre=p[1], field=cantidad):
                try:
                    qty = int((field.value or "").strip())
                except ValueError:
                    aviso_proveedor.value = "⚠️ Ingresa una cantidad válida para continuar."
                    aviso_proveedor.visible = True
                    aviso_proveedor.update()
                    mostrar_mensaje("Cantidad inválida.", False)
                    return

                if qty <= 0:
                    aviso_proveedor.value = "⚠️ La cantidad debe ser mayor que cero."
                    aviso_proveedor.visible = True
                    aviso_proveedor.update()
                    mostrar_mensaje("Cantidad inválida.", False)
                    return

                prov_id, prov_nom = obtener_proveedor_seleccionado()
                if not prov_id or not prov_nom:
                    aviso_proveedor.value = "⚠️ Selecciona un proveedor para poder añadir este producto."
                    aviso_proveedor.visible = True
                    aviso_proveedor.update()
                    mostrar_mensaje("Seleccione un proveedor para asociar el movimiento.", False)
                    return

                precio_unitario = float(p[3] if len(p) > 3 else 0)
                costo = costo_total(qty, precio_unitario)
                presupuesto_actual = obtener_presupuesto()

                if costo > presupuesto_actual:
                    aviso_proveedor.value = f"⚠️ No hay presupuesto suficiente para añadir {qty} unidad(es). Faltan ${costo - presupuesto_actual:,.2f}."
                    aviso_proveedor.visible = True
                    aviso_proveedor.update()
                    mostrar_mensaje(f"No hay presupuesto suficiente para agregar {qty} unidad(es). Faltan ${costo - presupuesto_actual:,.2f}", False)
                    return

                if actualizar_stock(id_prod, qty):
                    aviso_proveedor.value = ""
                    aviso_proveedor.visible = False
                    aviso_proveedor.update()
                    if not consumir_presupuesto(costo):
                        mostrar_mensaje("No hay presupuesto suficiente para comprar esta cantidad.", False)
                        return
                    registrar_pedido(id_prod, nombre, prov_id, prov_nom, qty, "stock", precio_unitario, costo)
                    mostrar_mensaje(f"✓ Compra registrada: {qty} x {nombre} · Costo: ${costo:,.2f}")
                else:
                    mostrar_mensaje("Error al actualizar.", False)
                    return
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
                                btn_success("AÑADIR", on_click=agregar_stock)
                            ], spacing=5, wrap=False),
                            aviso_proveedor,
                        ], spacing=8)
                    ),
                    width=520
                )
            )

        if not items:
            items = [ft.Text("No hay productos cargados.", color="grey", italic=True)]
        productos.controls = items
        try:
            resumen_stock.update()
            alerta_stock.update()
            productos.update()
            page.update()
        except RuntimeError:
            pass

    buscador.on_change = refresh
    refresh()
    return ft.Column(
        [
            ft.Row(
                [
                    ft.Text("Pedidos", size=28, weight="bold", color="#2196F3"),
                    ft.Text("Busca productos, registra pedidos y revisa el stock actualizado.", size=13, color="black54"),
                ],
                alignment="spaceBetween",
                wrap=True,
            ),
            ft.Divider(height=15, color="transparent"),
            ft.Container(
                bgcolor="#F5F5F5",
                padding=12,
                border_radius=10,
                content=proveedores_dropdown
            ),
            ft.Divider(height=10, color="transparent"),
            ft.Container(
                bgcolor="#F5F5F5",
                padding=12,
                border_radius=10,
                content=ft.Column([
                    ft.Text("Presupuesto de compras", size=15, weight="bold", color="#2196F3"),
                    ft.Text("Define el dinero disponible para pedir o reabastecer stock.", size=12, color="black54"),
                    ft.Row([presupuesto_input, btn_primary("Guardar presupuesto", on_click=actualizar_presupuesto)], spacing=10, wrap=True),
                    presupuesto_info,
                ], spacing=6)
            ),
            ft.Divider(height=10, color="transparent"),
            ft.Row(
                [
                    buscador,
                    btn_primary("Ver resumen total", on_click=ir_resumen) if ir_resumen else ft.Container(),
                ],
                spacing=10,
                wrap=True,
                alignment="start",
            ),
            ft.Text("Resumen de stock", size=16, weight="bold", color="#2196F3"),
            resumen_stock,
            alerta_stock,
            ft.Divider(height=10, color="transparent"),
            productos
        ],
        horizontal_alignment="center",
        scroll="auto"
    )
