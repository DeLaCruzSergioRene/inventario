import flet as ft
from datos.logica import contar_entradas, contar_salidas, listar_productos, listar_proveedores
from estilos import btn_primary, card, PRIMARY, SUCCESS, DANGER, ACCENT, BG
# Vista adicional para ver el total registrado con scroll y búsqueda rápida

def vista_resumen(page, volver=None):
    productos = listar_productos()
    proveedores = listar_proveedores()

    resumen_texto = ft.Text("", size=13, color="black54")
    lista = ft.Row(spacing=10, run_spacing=10, wrap=True, alignment="start")

    def actualizar_lista(e=None):
        texto = (buscador.value or "").strip().lower()

        items = []
        productos_filtrados = []
        proveedores_filtrados = []

        for p in productos:
            if texto and texto not in p[1].lower():
                continue
            productos_filtrados.append(p)
            items.append(
                ft.Container(
                    content=card(
                        ft.Column([
                            ft.Text(p[1], size=16, weight="bold", color=PRIMARY),
                            ft.Text(f"Stock actual: {p[2]} unidades", size=13, color="black54"),
                            ft.Text("Tipo: Producto", size=12, color=ACCENT),
                        ], spacing=4),
                        width=470,
                    ),
                    margin=ft.margin.only(bottom=6),
                )
            )

        for prov in proveedores:
            nombre = prov[1].lower()
            telefono = str(prov[2]).lower()
            if texto and texto not in nombre and texto not in telefono:
                continue
            proveedores_filtrados.append(prov)
            items.append(
                ft.Container(
                    content=card(
                        ft.Column([
                            ft.Text(prov[1], size=16, weight="bold", color=SUCCESS),
                            ft.Text(f"Teléfono: {prov[2]}", size=13, color="black54"),
                            ft.Text("Tipo: Proveedor", size=12, color=SUCCESS),
                        ], spacing=4),
                        width=470,
                    ),
                    margin=ft.margin.only(bottom=6),
                )
            )

        if not items:
            items = [ft.Text("No hay registros que coincidan con la búsqueda.", color="grey", italic=True)]

        lista.controls = items
        total_visible = len(productos_filtrados) + len(proveedores_filtrados)
        resumen_texto.value = (
            f"Mostrando {total_visible} registro(s) de {len(productos)} producto(s) y {len(proveedores)} proveedor(es)."
        )
        try:
            lista.update()
            resumen_texto.update()
            page.update()
        except RuntimeError:
            pass

    buscador = ft.TextField(
        label="Buscar registros",
        hint_text="Producto o proveedor",
        width=340,
        border_radius=10,
        on_change=actualizar_lista,
    )

    total_unidades = sum(p[2] for p in productos)
    stock_bajo = sum(1 for p in productos if p[2] < 5)
    entradas = contar_entradas()
    salidas = contar_salidas()

    actualizar_lista()

    return ft.Container(
        expand=True,
        padding=5,
        bgcolor=BG,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Resumen total", size=28, weight="bold", color=PRIMARY),
                        ft.Text("Productos y proveedores registrados con scroll para ver todo.", size=13, color="black54"),
                    ],
                    alignment="spaceBetween",
                    wrap=True,
                ),
                ft.Row(
                    [
                        buscador,
                        btn_primary("Volver a pedidos", on_click=lambda e: volver(e) if volver else None) if volver else ft.Container(),
                    ],
                    spacing=10,
                    wrap=True,
                    alignment="start",
                ),
                ft.Row(
                    [
                        card(ft.Column([ft.Text("Productos", size=11, color="black54"), ft.Text(str(len(productos)), size=24, weight="bold", color=PRIMARY)]), width=150),
                        card(ft.Column([ft.Text("Proveedores", size=11, color="black54"), ft.Text(str(len(proveedores)), size=24, weight="bold", color=SUCCESS)]), width=150),
                        card(ft.Column([ft.Text("Unidades", size=11, color="black54"), ft.Text(str(total_unidades), size=24, weight="bold", color=ACCENT)]), width=150),
                        card(ft.Column([ft.Text("Entradas", size=11, color="black54"), ft.Text(str(entradas), size=24, weight="bold", color=SUCCESS)]), width=150),
                        card(ft.Column([ft.Text("Salidas", size=11, color="black54"), ft.Text(str(salidas), size=24, weight="bold", color=DANGER)]), width=150),
                        card(ft.Column([ft.Text("Stock bajo", size=11, color="black54"), ft.Text(str(stock_bajo), size=24, weight="bold", color=DANGER)]), width=150),
                    ],
                    spacing=10,
                    wrap=True,
                ),
                resumen_texto,
                ft.Container(
                    expand=True,
                    height=500,
                    border_radius=12,
                    bgcolor="#FFFFFF",
                    padding=10,
                    shadow=ft.BoxShadow(blur_radius=4, spread_radius=0, color="#00000010"),
                    content=ft.Column([lista], spacing=10, scroll="auto"),
                ),
            ],
            spacing=12,
            expand=True,
            scroll="auto",
        ),
    )
