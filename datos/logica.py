from datetime import datetime, timezone

from datos.db import conectar

db = conectar()


def ahora_local():
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")


def formatear_fecha_local(fecha):
    if not fecha:
        return ""
    try:
        dt = datetime.fromisoformat(str(fecha).replace("Z", "+00:00"))
    except ValueError:
        return str(fecha)

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.now().astimezone().tzinfo)

    return dt.astimezone().strftime("%Y-%m-%d %H:%M:%S")

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
    print(f"logica.borrar llamado tab={tab} id={id_reg}")
    cur = db.cursor()
    before = db.total_changes
    cur.execute(f"DELETE FROM {tab} WHERE id = ?", (id_reg,))
    db.commit()
    after = db.total_changes
    affected = after - before
    print(f"logica.borrar: filas afectadas={affected} para id={id_reg} en {tab}")
    return affected > 0

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
def guardar_producto(nombre, cantidad, precio=0):
    nombre = nombre.strip()
    cantidad = int(cantidad)
    precio = float(precio or 0)
    db.execute("INSERT INTO prod (nom, cant, precio) VALUES (?, ?, ?)", (nombre, cantidad, precio))
    db.commit()
    return True

def listar_productos():
    return listar("prod")

def borrar_producto(id_reg):
    return borrar("prod", id_reg)

def actualizar_producto(id_reg, nombre, cantidad, precio=0):
    db.execute("UPDATE prod SET nom = ?, cant = ?, precio = ? WHERE id = ?", (nombre.strip(), int(cantidad), float(precio or 0), id_reg))
    db.commit()
    return True

def obtener_producto(id_reg):
    return obtener("prod", id_reg)


def guardar_usuario(nombre, email, clave):
    email = email.strip().lower()
    nombre = nombre.strip()
    if not nombre or not email or not clave:
        return False
    if obtener_usuario_por_email(email):
        return False
    db.execute(
        "INSERT INTO usuarios (nombre, email, clave, fecha) VALUES (?, ?, ?, ?)",
        (nombre, email, clave, ahora_local()),
    )
    db.commit()
    return True

def obtener_usuario_por_email(email):
    email = email.strip().lower()
    return db.execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()

def verificar_usuario(email, clave):
    usuario = obtener_usuario_por_email(email)
    return usuario is not None and usuario[3] == clave


def registrar_pedido(prod_id, prod_nom, prov_id, prov_nom, cantidad, tipo, precio_unitario=0, costo_total=None):
    if cantidad <= 0:
        return False
    if costo_total is None:
        costo_total = float(cantidad or 0) * float(precio_unitario or 0)
    db.execute(
        "INSERT INTO pedidos (prod_id, prod_nom, prov_id, prov_nom, cant, tipo, precio_unitario, costo_total, fecha) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (prod_id, prod_nom.strip(), prov_id, prov_nom.strip(), cantidad, tipo, float(precio_unitario or 0), float(costo_total or 0), ahora_local())
    )
    db.commit()
    return True


def listar_pedidos(tipo=None):
    base_sql = (
        "SELECT id, prod_id, prod_nom, prov_id, prov_nom, cant, tipo, "
        "precio_unitario, costo_total, fecha FROM pedidos"
    )
    if tipo:
        return db.execute(f"{base_sql} WHERE tipo = ? ORDER BY id DESC", (tipo,)).fetchall()
    return db.execute(f"{base_sql} ORDER BY id DESC").fetchall()

def borrar_pedido(id_reg):
    return borrar("pedidos", id_reg)


def contar_movimientos(tipo):
    fila = db.execute("SELECT COALESCE(SUM(cant), 0) FROM pedidos WHERE tipo = ?", (tipo,)).fetchone()
    return int(fila[0]) if fila else 0


def contar_entradas():
    return contar_movimientos("stock")


def contar_salidas():
    return contar_movimientos("pedido")

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
