import sqlite3
def conectar():
    con = sqlite3.connect("datos.db", check_same_thread=False)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS prov (id INTEGER PRIMARY KEY, nom TEXT, tel TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS prod (id INTEGER PRIMARY KEY, nom TEXT, cant INT)")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prod_id INTEGER,
            prod_nom TEXT,
            prov_id INTEGER,
            prov_nom TEXT,
            cant INTEGER,
            tipo TEXT,
            fecha TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    con.commit()
    return con