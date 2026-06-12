import sqlite3


def conectar():
    con = sqlite3.connect("datos.db", check_same_thread=False)
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS prov (id INTEGER PRIMARY KEY, nom TEXT, tel TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS prod (id INTEGER PRIMARY KEY, nom TEXT, cant INT, precio REAL DEFAULT 0)")

    columnas_prod = {fila[1] for fila in cur.execute("PRAGMA table_info(prod)").fetchall()}
    if "precio" not in columnas_prod:
        cur.execute("ALTER TABLE prod ADD COLUMN precio REAL DEFAULT 0")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS presupuesto (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            monto REAL DEFAULT 0
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prod_id INTEGER,
            prod_nom TEXT,
            prov_id INTEGER,
            prov_nom TEXT,
            cant INTEGER,
            tipo TEXT,
            precio_unitario REAL DEFAULT 0,
            costo_total REAL DEFAULT 0,
            fecha TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    columnas_pedidos = {fila[1] for fila in cur.execute("PRAGMA table_info(pedidos)").fetchall()}
    if "precio_unitario" not in columnas_pedidos:
        cur.execute("ALTER TABLE pedidos ADD COLUMN precio_unitario REAL DEFAULT 0")
    if "costo_total" not in columnas_pedidos:
        cur.execute("ALTER TABLE pedidos ADD COLUMN costo_total REAL DEFAULT 0")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            clave TEXT NOT NULL,
            fecha TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    con.commit()
    return con