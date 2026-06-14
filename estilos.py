import flet as ft

# Paleta de colores moderna y consistente para toda la app
BG = ft.Colors.BLUE_GREY_50
PRIMARY = "#2196F3"
SUCCESS = "#4CAF50"
WARNING = "#FF9800"
DANGER = "#F44336"
DARK = "#212121"
LIGHT = "#F5F5F5"
ACCENT = "#00BCD4"

# Botón azul principal para acciones importantes
def btn_primary(texto, on_click=None):
    return ft.ElevatedButton(texto, on_click=on_click, bgcolor=PRIMARY, color="white", 
        elevation=2, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)))

# Botón verde para acciones positivas (pedir, confirmar)
def btn_success(texto, on_click=None):
    return ft.ElevatedButton(texto, on_click=on_click, bgcolor=SUCCESS, color="white",
        elevation=2, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)))

# Botón rojo de texto para eliminar registros
def btn_danger(texto, on_click=None):
    return ft.TextButton(texto, on_click=on_click, style=ft.ButtonStyle(color=DANGER, 
        shape=ft.RoundedRectangleBorder(radius=8)))

# Contenedor reutilizable con estilo moderno para mostrar elementos
def card(content, width=520):
    return ft.Container(bgcolor=LIGHT, padding=6, border_radius=12, width=width,
        shadow=ft.BoxShadow(blur_radius=4, spread_radius=0, color="#00000015"),
            content=content)