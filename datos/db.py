import sqlite3
def conectar():
    con = sqlite3.connect("datos.db", check_same_thread=False)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS prov (id INTEGER PRIMARY KEY, nom TEXT, tel TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS prod (id INTEGER PRIMARY KEY, nom TEXT, cant INT)")
    con.commit()
    return con