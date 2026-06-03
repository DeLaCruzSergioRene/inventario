from datos.db import conectar
db = conectar()  

# Inserta un nuevo registro en la tabla especificada (proveedores o productos)
def guardar(tab, val):
    cols = "nom, tel" if tab == "prov" else "nom, cant"
    db.execute(f"INSERT INTO {tab} ({cols}) VALUES (?, ?)", val)
    db.commit()

# Obtiene todos los registros de una tabla (prov o prod)
def listar(tab):
    return db.execute(f"SELECT * FROM {tab}").fetchall()

# Elimina un registro por su ID de la tabla especificada
def borrar(tab, id_reg):
    db.execute(f"DELETE FROM {tab} WHERE id = ?", (id_reg,))
    db.commit()

# Valida stock disponible y resta cantidad al producto si hay suficiente
def pedir_producto(id_prod, cantidad):
    if cantidad <= 0:
        return False
    fila = db.execute("SELECT cant FROM prod WHERE id = ?", (id_prod,)).fetchone()
    # Verifica si existe el producto y si hay stock suficiente
    if not fila or fila[0] < cantidad:
        return False
    db.execute("UPDATE prod SET cant = ? WHERE id = ?", (fila[0] - cantidad, id_prod))
    db.commit()
    return True

# Suma unidades al stock de un producto cuando llega nueva mercancía
def actualizar_stock(id_prod, cantidad_adicional):
    if cantidad_adicional <= 0:
        return False
    fila = db.execute("SELECT cant FROM prod WHERE id = ?", (id_prod,)).fetchone()
    if not fila:
        return False
    nuevo_stock = fila[0] + cantidad_adicional
    db.execute("UPDATE prod SET cant = ? WHERE id = ?", (nuevo_stock, id_prod))
    db.commit()
    return True
