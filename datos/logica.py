from datos.db import conectar
db = conectar()

def guardar(tab, val):
    cols = "nom, tel" if tab == "prov" else "nom, cant"
    db.execute(f"INSERT INTO {tab} ({cols}) VALUES (?, ?)", val)
    db.commit()

def listar(tab):
    return db.execute(f"SELECT * FROM {tab}").fetchall()

def borrar(tab, id_reg):
    db.execute(f"DELETE FROM {tab} WHERE id = ?", (id_reg,))
    db.commit()

def pedir_producto(id_prod, cantidad):
    if cantidad <= 0:
        return False
    fila = db.execute("SELECT cant FROM prod WHERE id = ?", (id_prod,)).fetchone()
    if not fila or fila[0] < cantidad:
        return False
    db.execute("UPDATE prod SET cant = ? WHERE id = ?", (fila[0] - cantidad, id_prod))
    db.commit()
    return True
