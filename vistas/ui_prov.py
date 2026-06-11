import flet as ft
from datos.logica import guardar_proveedor, listar_proveedores, borrar_proveedor, actualizar_proveedor, obtener_proveedor
from estilos import btn_primary, btn_danger, btn_success, card, PRIMARY, ACCENT, SUCCESS, DANGER

# Vista para registrar y gestionar proveedores
def vista_prov(page):
    nombre = ft.TextField(label="Nombre del Proveedor", width=300, border_radius=10)
    telefono = ft.TextField(label="Teléfono", width=300, border_radius=10)
    busqueda = ft.TextField(label="Buscar proveedor", width=300, border_radius=10, on_change=lambda e: refresh())
    resumen = ft.Text("", size=12, color=PRIMARY)
    col = ft.Column(horizontal_alignment="center", spacing=10)
    estado_edicion = {"id": None}

    def mostrar_mensaje(texto, exito=True):
        page.snack_bar = ft.SnackBar(ft.Text(texto), bgcolor=SUCCESS if exito else DANGER)
        page.snack_bar.open = True
        page.update()

    def cancelar_edicion(e=None):
        estado_edicion["id"] = None
        nombre.value = ""
        telefono.value = ""
        btn_guardar.text = "REGISTRAR PROVEEDOR"
        btn_cancelar.visible = False
        page.update()

    def cargar_edicion(id_reg):
        proveedor = obtener_proveedor(id_reg)
        if proveedor:
            estado_edicion["id"] = id_reg
            nombre.value = proveedor[1]
            telefono.value = proveedor[2]
            btn_guardar.text = "ACTUALIZAR PROVEEDOR"
            btn_cancelar.visible = True
            page.update()

    def guardar_o_actualizar(e=None):
        nom = nombre.value.strip()
        tel = telefono.value.strip()
        if not nom or not tel:
            mostrar_mensaje("Complete todos los campos.", False)
            return
        if estado_edicion["id"] is None:
            guardar_proveedor(nom, tel)
            mostrar_mensaje("Proveedor registrado.")
        else:
            actualizar_proveedor(estado_edicion["id"], nom, tel)
            mostrar_mensaje("Proveedor actualizado.")
        cancelar_edicion()
        refresh()

    btn_cancelar = ft.TextButton("CANCELAR", visible=False, on_click=cancelar_edicion)
    btn_guardar = btn_primary("REGISTRAR PROVEEDOR", on_click=guardar_o_actualizar)

    def confirmar_borrar(id_reg):
        print(f"confirmar_borrar prov llamado con id={id_reg}")
        page.snack_bar = ft.SnackBar(ft.Text(f"Debug: abrir dialogo borrar prov {id_reg}"), bgcolor=SUCCESS)
        page.snack_bar.open = True
        page.update()
        def cerrar(e=None):
            page.dialog = None
            refresh()
            page.update()

        def confirmar(e=None):
            print(f"confirmar prov ejecutar borrar id={id_reg}")
            page.snack_bar = ft.SnackBar(ft.Text(f"Debug: confirmando borrar prov {id_reg}"), bgcolor=SUCCESS)
            page.snack_bar.open = True
            page.update()
            res = borrar_proveedor(id_reg)
            print(f"borrar_proveedor devolvió: {res}")
            if res:
                refresh()
                mostrar_mensaje("Proveedor eliminado.")
            else:
                mostrar_mensaje("No se pudo eliminar el proveedor.", False)
            cerrar()

        # Mantener la función para compatibilidad con otros usos pero
        # no mostrar diálogo cuando se usa la X.
        pass

    def borrar_directo(id_reg, e=None):
        print(f"borrar_directo prov llamado con id={id_reg}")
        res = borrar_proveedor(id_reg)
        print(f"borrar_proveedor devolvió: {res}")
        if res:
            mostrar_mensaje("Proveedor eliminado.")
        else:
            mostrar_mensaje("No se pudo eliminar el proveedor.", False)
        refresh()
        page.update()

    def refresh(e=None):
        proveedores = listar_proveedores()
        texto = busqueda.value.strip().lower()
        filtrados = [p for p in proveedores if texto in p[1].lower() or texto in p[2].lower()]

        resumen.value = f"Mostrando {len(filtrados)} proveedor(es) de {len(proveedores)} registrados."

        items = []
        for p in filtrados:
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
                        ft.Row([
                            btn_success("EDITAR", on_click=lambda e, id=p[0]: cargar_edicion(id)),
                            btn_danger("✕", on_click=lambda e, id=p[0]: borrar_directo(id))
                        ], spacing=5)
                    ], alignment="spaceBetween", vertical_alignment="center"),
                    width=450
                )
            )
        if not items:
            items = [ft.Text("No hay proveedores que coincidan con la búsqueda.", color="grey", italic=True)]
        col.controls = items
        if col.page:
            col.update()

    col.on_mount = refresh
    return ft.Column([
        ft.Row(
            [
                ft.Text("Proveedores", size=28, weight="bold", color=PRIMARY),
                ft.Text("Gestiona tus proveedores y contactos.", size=13, color="black54"),
            ],
            alignment="spaceBetween",
            wrap=True,
        ),
        ft.Divider(height=15, color="transparent"),
        card(
            ft.Column([nombre, telefono, ft.Row([btn_guardar, btn_cancelar], spacing=10)], spacing=10),
            width=350
        ),
        ft.Divider(height=10, color="transparent"),
        busqueda,
        resumen,
        ft.Divider(height=10, color="transparent"),
        col
    ], horizontal_alignment="center", scroll="auto")
