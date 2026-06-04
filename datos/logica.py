from datos.db import conectar

db = conectar()

# Inserta un nuevo registro en la tabla especificada (proveedores o productos)
def guardar(tab, val):
    if tab == "prov":
        db.execute("INSERT INTO prov (nom, tel) VALUES (?, ?)", (val[0].strip(), val[1].strip()))
    else:
        db.execute("INSERT INTO prod (nom, cant) VALUES (?, ?)", (val[0].strip(), int(val[1])))
    db.commit()

# Obtiene todos los registros de una tabla (prov o prod)
def listar(tab):
    return db.execute(f"SELECT * FROM {tab}").fetchall()

# Elimina un registro por su ID de la tabla especificada
def borrar(tab, id_reg):
    db.execute(f"DELETE FROM {tab} WHERE id = ?", (id_reg,))
    db.commit()

# Actualiza un registro existente en la tabla especificada
def actualizar(tab, id_reg, valores):
    if tab == "prov":
        db.execute("UPDATE prov SET nom = ?, tel = ? WHERE id = ?", (*valores, id_reg))
    else:
        db.execute("UPDATE prod SET nom = ?, cant = ? WHERE id = ?", (*valores, id_reg))
    db.commit()

# Obtiene un registro por ID
def obtener(tab, id_reg):
    return db.execute(f"SELECT * FROM {tab} WHERE id = ?", (id_reg,)).fetchone()

# Proveedores
def guardar_proveedor(nombre, telefono):
    return guardar("prov", (nombre, telefono))

def listar_proveedores():
    return listar("prov")

def borrar_proveedor(id_reg):
    return borrar("prov", id_reg)

def actualizar_proveedor(id_reg, nombre, telefono):
    return actualizar("prov", id_reg, (nombre.strip(), telefono.strip()))

def obtener_proveedor(id_reg):
    return obtener("prov", id_reg)

# Productos
def guardar_producto(nombre, cantidad):
    return guardar("prod", (nombre, cantidad))

def listar_productos():
    return listar("prod")

def borrar_producto(id_reg):
    return borrar("prod", id_reg)

def actualizar_producto(id_reg, nombre, cantidad):
    return actualizar("prod", id_reg, (nombre.strip(), int(cantidad)))

def obtener_producto(id_reg):
    return obtener("prod", id_reg)

# Valida stock disponible y resta cantidad al producto si hay suficiente
def pedir_producto(id_prod, cantidad):
    if cantidad <= 0:
        return False
    fila = db.execute("SELECT cant FROM prod WHERE id = ?", (id_prod,)).fetchone()
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
