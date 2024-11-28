import sqlite3

def validar_usuario(usuario_id):
    with sqlite3.connect('script_para_crear_la_base_de_datos.sql') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM usuarios WHERE id_discord = ?", (usuario_id,))
        return cursor.fetchone() is not None
    