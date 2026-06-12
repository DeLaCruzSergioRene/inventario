from datos.db import conectar

db = conectar()

def obtener_presupuesto():
    fila = db.execute("SELECT monto FROM presupuesto WHERE id = 1").fetchone()
    return float(fila[0]) if fila else 0.0

def guardar_presupuesto(monto):
    monto = max(0.0, float(monto or 0))
    db.execute(
        "INSERT INTO presupuesto (id, monto) VALUES (1, ?) "
        "ON CONFLICT(id) DO UPDATE SET monto = excluded.monto",
        (monto,),
    )
    db.commit()
    return True

def consumir_presupuesto(monto):
    monto = float(monto or 0)
    if monto <= 0:
        return True
    actual = obtener_presupuesto()
    if actual < monto:
        return False
    return guardar_presupuesto(actual - monto)

def costo_total(cantidad, precio_unitario):
    return float(cantidad or 0) * float(precio_unitario or 0)

def presupuesto_suficiente(cantidad, precio_unitario):
    return costo_total(cantidad, precio_unitario) <= obtener_presupuesto()
