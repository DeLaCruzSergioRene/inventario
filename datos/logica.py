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