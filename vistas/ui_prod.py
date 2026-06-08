import flet as ft
from datos.logica import guardar_producto, listar_productos, borrar_producto, actualizar_producto, obtener_producto
from estilos import btn_primary, btn_danger, btn_success, card, PRIMARY, ACCENT, SUCCESS, DANGER

# Vista para gestionar el inventario de productos
def vista_prod(page):
    nombre = ft.TextField(label="Producto", width=300, border_radius=10)
    cantidad = ft.TextField(label="Cantidad", width=300, border_radius=10, keyboard_type=ft.KeyboardType.NUMBER)
    col = ft.Column(horizontal_alignment="center", spacing=10)
    estado_edicion = {"id": None}

    def mostrar_mensaje(texto, exito=True):
        page.snack_bar = ft.SnackBar(ft.Text(texto), bgcolor=SUCCESS if exito else DANGER)
        page.snack_bar.open = True
        page.update()

    def cancelar_edicion(e=None):
        estado_edicion["id"] = None
        nombre.value = ""
        cantidad.value = ""
        btn_guardar.text = "REGISTRAR PRODUCTO"
        btn_cancelar.visible = False
        page.update()

    def cargar_edicion(id_reg):
        producto = obtener_producto(id_reg)
        if producto:
            estado_edicion["id"] = id_reg
            nombre.value = producto[1]
            cantidad.value = str(producto[2])
            btn_guardar.text = "ACTUALIZAR PRODUCTO"
            btn_cancelar.visible = True
            page.update()

    def guardar_o_actualizar(e=None):
        nom = nombre.value.strip()
        cant = cantidad.value.strip()
        if not nom or not cant or not cant.isdigit() or int(cant) <= 0:
            mostrar_mensaje("Ingrese nombre y cantidad válidos.", False)
            return
        if estado_edicion["id"] is None:
            guardar_producto(nom, cant)
            mostrar_mensaje("Producto registrado.")
        else:
            actualizar_producto(estado_edicion["id"], nom, cant)
            mostrar_mensaje("Producto actualizado.")
        cancelar_edicion()
        refresh()

    btn_cancelar = ft.TextButton("CANCELAR", visible=False, on_click=cancelar_edicion)
    btn_guardar = btn_primary("REGISTRAR PRODUCTO", on_click=guardar_o_actualizar)

    def confirmar_borrar(id_reg):
        print(f"confirmar_borrar llamado con id={id_reg}")
        page.snack_bar = ft.SnackBar(ft.Text(f"Debug: abrir dialogo borrar {id_reg}"), bgcolor=SUCCESS)
        page.snack_bar.open = True
        page.update()
        def cerrar(e=None):
            page.dialog = None            
            refresh()            
            page.update()

        def confirmar(e=None):
            print(f"confirmar ejecutar borrar id={id_reg}")
            page.snack_bar = ft.SnackBar(ft.Text(f"Debug: confirmando borrar {id_reg}"), bgcolor=SUCCESS)
            page.snack_bar.open = True
            page.update()
            res = borrar_producto(id_reg)
            print(f"borrar_producto devolvió: {res}")
            if res:
                refresh()
                mostrar_mensaje("Producto eliminado.")
            else:
                mostrar_mensaje("No se pudo eliminar el producto.", False)
            cerrar()

        # Mantener la función para compatibilidad con otros usos pero
        # no mostrar diálogo cuando se usa la X.
        # Para borrar directamente usa la función interna `borrar_directo`.
        pass

    def borrar_directo(id_reg, e=None):
        print(f"borrar_directo llamado con id={id_reg}")
        res = borrar_producto(id_reg)
        print(f"borrar_producto devolvió: {res}")
        if res:
            mostrar_mensaje("Producto eliminado.")
        else:
            mostrar_mensaje("No se pudo eliminar el producto.", False)
        refresh()
        page.update()

    def refresh(e=None):
        items = []
        for p in listar_productos():
            items.append(
                card(
                    ft.Column([
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
                            ft.Row([
                                btn_success("EDITAR", on_click=lambda e, id=p[0]: cargar_edicion(id)),
                                btn_danger("✕", on_click=lambda e, id=p[0]: borrar_directo(id))
                            ], spacing=5)
                        ], alignment="spaceBetween", vertical_alignment="center")
                    ]),
                    width=450
                )
            )
        col.controls = items
        if col.page:
            col.update()

    col.on_mount = refresh
    return ft.Column([
        ft.Text("INVENTARIO", size=28, weight="bold", color=PRIMARY),
        ft.Text("Registra productos y gestiona el stock.", color="black54", size=14),
        ft.Divider(height=15, color="transparent"),
        card(
            ft.Column([nombre, cantidad, ft.Row([btn_guardar, btn_cancelar], spacing=10)], spacing=10),
            width=350
        ),
        ft.Divider(height=20, color="transparent"),
        col
    ], horizontal_alignment="center", scroll="auto")
